const FameCalculator = require('../viral/fame-calculator');

class Organizer {
  /**
   * Enriches project list with fame & activity metrics and sorts/filters them.
   * @param {Array<object>} projects 
   * @param {object} remoteStatsMap Map of project path/id -> { stars, forks, views }
   * @returns {Array<object>}
   */
  static enrich(projects, remoteStatsMap = {}) {
    return projects.map(p => {
      const stats = remoteStatsMap[p.id] || remoteStatsMap[p.path] || {};
      const fame = FameCalculator.calculate(p, stats);
      return {
        ...p,
        fame
      };
    });
  }

  /**
   * Sorts projects by requested criteria.
   * @param {Array<object>} projects 
   * @param {'frequency'|'recent'|'oldest'|'fame'|'stars'|'views'|'language'|'name'} sortBy 
   * @param {'asc'|'desc'} order 
   */
  static sort(projects, sortBy = 'frequency', order = 'desc') {
    const list = [...projects];

    list.sort((a, b) => {
      let diff = 0;
      switch (sortBy) {
        case 'frequency':
        case 'activity':
          diff = (a.fame?.activityScore || 0) - (b.fame?.activityScore || 0);
          break;

        case 'recent':
        case 'date':
          diff = new Date(a.timestamps.lastActive) - new Date(b.timestamps.lastActive);
          break;

        case 'oldest':
          diff = new Date(a.timestamps.lastActive) - new Date(b.timestamps.lastActive);
          break;

        case 'fame':
          diff = (a.fame?.fameScore || 0) - (b.fame?.fameScore || 0);
          break;

        case 'stars':
          diff = (a.fame?.stars || 0) - (b.fame?.stars || 0);
          break;

        case 'views':
          diff = (a.fame?.views || 0) - (b.fame?.views || 0);
          break;

        case 'language':
          diff = (a.primaryLanguage || '').localeCompare(b.primaryLanguage || '');
          break;

        case 'name':
          diff = (a.name || '').localeCompare(b.name || '');
          break;

        default:
          diff = 0;
      }

      return order === 'desc' ? -diff : diff;
    });

    return list;
  }

  /**
   * Filters projects by query, language, status, or tier.
   */
  static filter(projects, criteria = {}) {
    return projects.filter(p => {
      if (criteria.query) {
        const q = criteria.query.toLowerCase();
        const matchName = p.name.toLowerCase().includes(q);
        const matchDesc = (p.description || '').toLowerCase().includes(q);
        const matchLang = (p.primaryLanguage || '').toLowerCase().includes(q);
        if (!matchName && !matchDesc && !matchLang) return false;
      }

      if (criteria.language && criteria.language !== 'all') {
        if (p.primaryLanguage !== criteria.language) return false;
      }

      if (criteria.tier && criteria.tier !== 'all') {
        if (p.fame?.tier?.id !== criteria.tier) return false;
      }

      if (criteria.status) {
        if (criteria.status === 'unreleased' && !p.git.isUnreleased) return false;
        if (criteria.status === 'published' && p.git.isUnreleased) return false;
        if (criteria.status === 'needs_readme' && p.hasReadme) return false;
        if (criteria.status === 'dirty' && p.git.isClean) return false;
      }

      return true;
    });
  }

  /**
   * Groups projects into multidimensional buckets.
   */
  static categorize(projects) {
    const byLanguage = {};
    const byTier = {};
    const byStatus = {
      unreleased: [],
      published: [],
      needsReadme: [],
      dirty: []
    };

    for (const p of projects) {
      // By Language
      const lang = p.primaryLanguage || 'Unknown';
      if (!byLanguage[lang]) byLanguage[lang] = [];
      byLanguage[lang].push(p);

      // By Tier
      const tierId = p.fame?.tier?.id || 'sprout';
      if (!byTier[tierId]) byTier[tierId] = [];
      byTier[tierId].push(p);

      // By Status
      if (p.git.isUnreleased) byStatus.unreleased.push(p);
      else byStatus.published.push(p);

      if (!p.hasReadme) byStatus.needsReadme.push(p);
      if (!p.git.isClean) byStatus.dirty.push(p);
    }

    return {
      total: projects.length,
      byLanguage,
      byTier,
      byStatus
    };
  }
}

module.exports = Organizer;
