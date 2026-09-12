class BadgeGenerator {
  /**
   * Generates markdown badges for a project based on its fame and mirrors.
   */
  static generateMarkdownBadges(project, mirrors = []) {
    const badges = [];

    // 1. RepoForge Verified Badge
    badges.push(`[![RepoForge](https://img.shields.io/badge/Cataloged%20by-RepoForge-8b5cf6.svg?style=flat-square)](https://github.com/)`);

    // 2. Fame Tier Badge
    if (project.fame?.tier) {
      const tier = project.fame.tier;
      const cleanLabel = encodeURIComponent(tier.label);
      const color = tier.id === 'diamond' ? '3b82f6' : tier.id === 'rising' ? '8b5cf6' : tier.id === 'relic' ? 'f59e0b' : '10b981';
      badges.push(`![Fame Tier](https://img.shields.io/badge/Status-${cleanLabel}-${color}.svg?style=flat-square)`);
    }

    // 3. Language Badge
    if (project.primaryLanguage && project.primaryLanguage !== 'Unknown') {
      const lang = encodeURIComponent(project.primaryLanguage);
      badges.push(`![Language](https://img.shields.io/badge/Language-${lang}-blue.svg?style=flat-square)`);
    }

    // 4. Multi-Forge Mirrors
    for (const m of mirrors) {
      if (m === 'gitlab') {
        badges.push(`[![GitLab](https://img.shields.io/badge/Mirror-GitLab-fc6d26.svg?style=flat-square&logo=gitlab)](https://gitlab.com)`);
      } else if (m === 'codeberg') {
        badges.push(`[![Codeberg](https://img.shields.io/badge/Mirror-Codeberg-2185d0.svg?style=flat-square&logo=codeberg)](https://codeberg.org)`);
      } else if (m === 'bitbucket') {
        badges.push(`[![Bitbucket](https://img.shields.io/badge/Mirror-Bitbucket-0052cc.svg?style=flat-square&logo=bitbucket)](https://bitbucket.org)`);
      }
    }

    return badges.join(' ');
  }

  /**
   * Returns a standalone SVG banner card for high-impact viral sharing.
   */
  static generateSvgCard(project) {
    const name = project.name || 'Project';
    const tier = project.fame?.tier?.label || 'Fresh Sprout';
    const score = project.fame?.fameScore || 0;
    const lang = project.primaryLanguage || 'Code';

    return `<svg xmlns="http://www.w3.org/2000/svg" width="480" height="120" viewBox="0 0 480 120">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e1b4b" />
    </linearGradient>
  </defs>
  <rect width="480" height="120" rx="12" fill="url(#bg)" stroke="#3b82f6" stroke-width="1.5" />
  <text x="24" y="38" fill="#f8fafc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto" font-size="18" font-weight="bold">${name}</text>
  <text x="24" y="65" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto" font-size="13">${lang} • Score: ${score}/100</text>
  <rect x="24" y="80" width="130" height="24" rx="12" fill="#3b82f6" fill-opacity="0.2" stroke="#3b82f6" stroke-width="1" />
  <text x="89" y="96" text-anchor="middle" fill="#60a5fa" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto" font-size="11" font-weight="600">${tier}</text>
  <text x="456" y="96" text-anchor="end" fill="#64748b" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto" font-size="10">RepoForge AI</text>
</svg>`;
  }
}

module.exports = BadgeGenerator;
