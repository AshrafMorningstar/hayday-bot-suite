const fs = require('fs');
const path = require('path');
const PromptTemplates = require('./prompt-templates');

class FreeAIService {
  /**
   * Checks if local Ollama is running on localhost:11434
   */
  static async checkOllama() {
    try {
      const res = await fetch('http://localhost:11434/api/tags', { signal: AbortSignal.timeout(1000) });
      if (res.ok) {
        const data = await res.json();
        return { available: true, models: data.models || [] };
      }
    } catch (_) {}
    return { available: false, models: [] };
  }

  /**
   * Generates a complete README for a project using offline heuristics or local Ollama.
   * @param {object} project 
   */
  static async generateReadme(project) {
    const projectDir = project.path;
    let files = [];
    try {
      files = fs.readdirSync(projectDir);
    } catch (_) {}

    // Check Ollama first
    const ollama = await this.checkOllama();
    if (ollama.available && ollama.models.length > 0) {
      const modelName = ollama.models[0].name;
      const prompt = PromptTemplates.getReadmePrompt(
        project.name,
        project.primaryLanguage,
        project.ecosystem,
        files,
        project.description
      );

      try {
        const res = await fetch('http://localhost:11434/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ model: modelName, prompt, stream: false })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.response) return data.response.trim();
        }
      } catch (_) {}
    }

    // High quality offline heuristic fallback (100% free, 0 network required)
    return this.synthesizeHeuristicReadme(project, files);
  }

  /**
   * Deterministic high-quality offline README generator
   */
  static synthesizeHeuristicReadme(project, files) {
    const name = project.name || 'Project';
    const lang = project.primaryLanguage || 'JavaScript';
    const eco = project.ecosystem || 'Generic';

    let installCmd = 'npm install';
    let runCmd = 'npm start';
    let buildCmd = 'npm run build';

    if (lang.includes('Python')) {
      installCmd = 'pip install -r requirements.txt';
      runCmd = 'python main.py';
    } else if (lang.includes('Rust')) {
      installCmd = 'cargo build';
      runCmd = 'cargo run';
    } else if (lang.includes('Go')) {
      installCmd = 'go mod download';
      runCmd = 'go run main.go';
    }

    const badgeUrl = `https://img.shields.io/badge/Language-${encodeURIComponent(lang)}-blue.svg`;
    const licenseBadge = `https://img.shields.io/badge/License-MIT-green.svg`;

    return `# ${name}

![${lang}](${badgeUrl}) ![License](${licenseBadge}) ![RepoForge](https://img.shields.io/badge/Organized%20with-RepoForge-purple.svg)

> ${project.description || `An open-source ${lang} project built with ${eco}.`}

---

## 🌟 Highlights & Features
- **Modern Architecture:** Built with clean ${lang} design patterns.
- **Lightweight & Modular:** Minimal footprint, optimized for efficiency.
- **Autonomous Ready:** Compatible with multi-forge publishing and automated workflows.

## 🛠️ Tech Stack
- **Primary Language:** ${lang}
- **Ecosystem:** ${eco}
- **Version:** ${project.version || '0.1.0'}

## 🚀 Quick Start

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/your-username/${name}.git
cd ${name}
\`\`\`

### 2. Install dependencies
\`\`\`bash
${installCmd}
\`\`\`

### 3. Run the project
\`\`\`bash
${runCmd}
\`\`\`

---

## 📄 License
This project is open-source software licensed under the [MIT License](LICENSE).

---
*Organized and cataloged automatically with [RepoForge](https://github.com/your-username/repoforge).*
`;
  }

  /**
   * Generates missing .gitignore and LICENSE files.
   */
  static applyStandardFiles(projectDir, language, authorName = 'RepoForge') {
    const gitignorePath = path.join(projectDir, '.gitignore');
    const licensePath = path.join(projectDir, 'LICENSE');
    const actionsTaken = [];

    if (!fs.existsSync(gitignorePath)) {
      const gitignore = PromptTemplates.getGitignoreTemplate(language);
      fs.writeFileSync(gitignorePath, gitignore, 'utf8');
      actionsTaken.push('.gitignore created');
    }

    if (!fs.existsSync(licensePath)) {
      const license = PromptTemplates.getLicenseTemplate(path.basename(projectDir), 'MIT', new Date().getFullYear(), authorName);
      fs.writeFileSync(licensePath, license, 'utf8');
      actionsTaken.push('LICENSE (MIT) created');
    }

    return actionsTaken;
  }
}

module.exports = FreeAIService;
