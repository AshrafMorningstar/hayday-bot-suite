const fs = require('fs');
const path = require('path');
const Organizer = require('../core/organizer');

class ShowcaseGenerator {
  /**
   * Generates a markdown portfolio document (MY_PROJECTS.md) from the scanned projects.
   * @param {Array<object>} projects 
   * @param {string} username 
   */
  static generateMarkdown(projects, username = 'Developer') {
    const sorted = Organizer.sort(projects, 'fame', 'desc');
    const categories = Organizer.categorize(sorted);

    let md = `# 🚀 ${username}'s Engineering Portfolio & Project Vault\n\n`;
    md += `> Automatically cataloged and curated by [RepoForge](https://github.com/your-username/repoforge) — *The Multi-Forge Project Hub*.\n\n`;

    // Metrics Overview
    md += `## 📊 Portfolio Metrics\n\n`;
    md += `| Total Repos | Diamond Masterpieces 💎 | Rising Stars 🚀 | Ancient Relics 🏺 | Unreleased 🌱 |\n`;
    md += `|:---:|:---:|:---:|:---:|:---:|\n`;
    md += `| **${projects.length}** | **${categories.byTier['diamond']?.length || 0}** | **${categories.byTier['rising']?.length || 0}** | **${categories.byTier['relic']?.length || 0}** | **${categories.byStatus.unreleased.length}** |\n\n`;

    // Languages Breakdown
    md += `### 🛠️ Languages & Tech Stacks\n\n`;
    const langEntries = Object.entries(categories.byLanguage).sort((a, b) => b[1].length - a[1].length);
    for (const [lang, list] of langEntries) {
      md += `- **${lang}**: \`${list.length} project${list.length > 1 ? 's' : ''}\`\n`;
    }
    md += `\n---\n\n`;

    // 1. Diamond & Flagship projects
    const diamonds = sorted.filter(p => p.fame?.tier?.id === 'diamond' || (p.fame?.stars || 0) > 10);
    if (diamonds.length > 0) {
      md += `## 💎 Flagship & Diamond Masterpieces\n\n`;
      md += `| Project | Tech Stack | Stars | Fame Score | Summary |\n`;
      md += `|:---|:---|:---:|:---:|:---|\n`;
      for (const p of diamonds) {
        const link = p.git?.remotes?.origin || p.path;
        md += `| [**${p.name}**](${link}) | \`${p.primaryLanguage}\` | ⭐ ${p.fame?.stars || 0} | \`${p.fame?.fameScore}/100\` | ${p.description.slice(0, 80)} |\n`;
      }
      md += `\n`;
    }

    // 2. Active & Rising projects
    const rising = sorted.filter(p => p.fame?.tier?.id === 'rising' || (p.fame?.activityScore || 0) > 70);
    if (rising.length > 0) {
      md += `## 🚀 Active & Rising Projects\n\n`;
      md += `| Project | Language | Activity Score | Last Active | Status |\n`;
      md += `|:---|:---|:---:|:---:|:---|\n`;
      for (const p of rising) {
        const lastDate = new Date(p.timestamps.lastActive).toISOString().split('T')[0];
        md += `| **${p.name}** | \`${p.primaryLanguage}\` | \`${p.fame?.activityScore}%\` | ${lastDate} | ${p.git.isUnreleased ? '🌱 Local' : '🌐 Published'} |\n`;
      }
      md += `\n`;
    }

    // 3. Ancient Relics (Old is Gold)
    const relics = sorted.filter(p => p.fame?.tier?.id === 'relic');
    if (relics.length > 0) {
      md += `## 🏺 Ancient Relics (Old is Gold)\n\n`;
      md += `*Timeless codebases and vintage experiments waiting for revival.*\n\n`;
      md += `| Project | Language | Days Inactive | Ecosystem |\n`;
      md += `|:---|:---|:---:|:---|\n`;
      for (const p of relics) {
        md += `| **${p.name}** | \`${p.primaryLanguage}\` | ${p.fame?.daysSinceActive || 0} days | ${p.ecosystem} |\n`;
      }
      md += `\n`;
    }

    // 4. Complete Project Catalog Table
    md += `## 🗂️ Complete Catalog Index\n\n`;
    md += `| # | Name | Language | Activity | Fame | Release Status |\n`;
    md += `|:---:|:---|:---:|:---:|:---:|:---:|\n`;
    for (let i = 0; i < sorted.length; i++) {
      const p = sorted[i];
      const statusIcon = p.git.isUnreleased ? '🔒 Local' : '🌍 Published';
      md += `| ${i + 1} | **${p.name}** | ${p.primaryLanguage} | ${p.fame?.activityScore}% | ${p.fame?.tier?.icon} ${p.fame?.fameScore} | ${statusIcon} |\n`;
    }

    md += `\n---\n*Catalog generated autonomously with [RepoForge](https://github.com/your-username/repoforge).*\n`;

    return md;
  }

  /**
   * Saves the generated markdown to a specified path.
   */
  static exportToFile(projects, outputPath, username = 'Developer') {
    const md = this.generateMarkdown(projects, username);
    const resolved = path.resolve(outputPath);
    fs.writeFileSync(resolved, md, 'utf8');
    return resolved;
  }
}

module.exports = ShowcaseGenerator;
