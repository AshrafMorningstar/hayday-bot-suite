class PromptTemplates {
  static getReadmePrompt(projectName, language, ecosystem, files, existingDescription) {
    return `Generate a clean, modern, professional GitHub README.md for the following project:
Project Name: ${projectName}
Primary Language: ${language}
Ecosystem: ${ecosystem}
Key Files: ${files.slice(0, 15).join(', ')}
Description / Context: ${existingDescription || 'A project developed with ' + language}

Requirements:
1. Project title with a catchy subtitle.
2. Features list (3-5 concise bullet points based on the files).
3. Tech Stack section.
4. Quick Start / Installation guide using the appropriate package manager.
5. Usage example.
6. License section (MIT).
Return ONLY the raw Markdown content.`;
  }

  static getGitignoreTemplate(language) {
    const common = `.DS_Store\nThumbs.db\n*.log\n.env\n.env.*\n`;
    switch ((language || '').toLowerCase()) {
      case 'javascript / typescript':
      case 'node.js':
        return `${common}node_modules/\ndist/\nbuild/\n.cache/\ncoverage/\n`;
      case 'python':
        return `${common}__pycache__/\n*.py[cod]\n*$py.class\nvenv/\n.venv/\nenv/\nbuild/\ndist/\n*.egg-info/\n`;
      case 'rust':
        return `${common}target/\n**/*.rs.bk\nCargo.lock\n`;
      case 'go':
        return `${common}bin/\n*.exe\n*.test\nvendor/\n`;
      case 'java':
      case 'java / kotlin':
        return `${common}target/\n*.class\n.gradle/\nbuild/\n*.jar\n*.war\n`;
      case 'c / c++':
      case 'c / c++ / make':
        return `${common}build/\nbin/\n*.o\n*.obj\n*.exe\nCMakeCache.txt\nCMakeFiles/\n`;
      default:
        return `${common}build/\ndist/\nbin/\n`;
    }
  }

  static getLicenseTemplate(projectName, licenseType = 'MIT', year = new Date().getFullYear(), author = 'RepoForge') {
    if (licenseType === 'MIT') {
      return `MIT License

Copyright (c) ${year} ${author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.`;
    }
    return `Copyright (c) ${year} ${author}. All rights reserved.`;
  }
}

module.exports = PromptTemplates;
