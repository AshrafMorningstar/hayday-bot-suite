class FameCalculator {
  /**
   * Computes fame score, fame tier, and activity metrics for a project.
   * @param {object} project 
   * @param {object} remoteStats Optional stars, forks, views
   */
  static calculate(project, remoteStats = {}) {
    const stars = remoteStats.stars !== undefined ? remoteStats.stars : (project.git?.stars || 0);
    const forks = remoteStats.forks !== undefined ? remoteStats.forks : (project.git?.forks || 0);
    const views = remoteStats.views !== undefined ? remoteStats.views : (project.git?.views || 0);
    const commits = project.git?.commitCount || 1;

    const now = new Date();
    const lastActiveDate = new Date(project.timestamps.lastActive);
    const daysSinceActive = Math.max(0, Math.floor((now - lastActiveDate) / (1000 * 60 * 60 * 24)));

    // 1. Fame score calculation (0 - 100)
    let fameScore = 0;
    fameScore += Math.min(stars * 2, 50);              // Up to 50 pts from stars
    fameScore += Math.min(forks * 4, 20);              // Up to 20 pts from forks
    fameScore += Math.min(Math.floor(views / 10), 15); // Up to 15 pts from views
    fameScore += Math.min(Math.floor(commits / 3), 15); // Up to 15 pts from commit history
    if (project.hasReadme) fameScore += 5;
    if (project.hasLicense) fameScore += 5;

    // Normalize
    fameScore = Math.min(100, Math.max(0, Math.round(fameScore)));

    // 2. Activity / Recency Score (0 - 100)
    // 0 days ago = 100 pts, 30 days = 80 pts, 180 days = 50 pts, 365+ days = <20 pts
    let activityScore = 100 - Math.min(100, Math.floor(daysSinceActive / 3.65));
    activityScore = Math.max(5, activityScore);

    // 3. Fame Tier classification
    let tier = {
      id: 'sprout',
      label: 'Fresh Sprout',
      icon: '🌱',
      color: '#10b981',
      description: 'Local prototype or young project awaiting takeoff.'
    };

    if (fameScore >= 75 || stars >= 50) {
      tier = {
        id: 'diamond',
        label: 'Diamond Masterpiece',
        icon: '💎',
        color: '#3b82f6',
        description: 'Highly acclaimed repository with prominent community fame.'
      };
    } else if (activityScore > 75 && commits >= 10) {
      tier = {
        id: 'rising',
        label: 'Rising Star',
        icon: '🚀',
        color: '#8b5cf6',
        description: 'Rapidly evolving codebase with high velocity.'
      };
    } else if (daysSinceActive > 365) {
      tier = {
        id: 'relic',
        label: 'Ancient Relic',
        icon: '🏺',
        color: '#f59e0b',
        description: 'Dormant treasure untouched for over a year. Ready for revival.'
      };
    } else if (commits > 25 || fameScore > 35) {
      tier = {
        id: 'workhorse',
        label: 'Steady Engine',
        icon: '⚙️',
        color: '#06b6d4',
        description: 'Reliable, well-maintained development component.'
      };
    }

    return {
      fameScore,
      activityScore,
      daysSinceActive,
      stars,
      forks,
      views,
      tier
    };
  }
}

module.exports = FameCalculator;
