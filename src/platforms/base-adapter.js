class BaseAdapter {
  constructor(name) {
    this.name = name;
  }

  getName() {
    return this.name;
  }

  /**
   * Returns a direct 1-click URL for user to generate a Personal Access Token
   * with necessary scopes pre-filled.
   */
  getTokenWizardUrl() {
    throw new Error('Not implemented');
  }

  /**
   * Tests token validity and returns user profile info.
   * @param {string} token 
   * @returns {Promise<{valid: boolean, user: object, error?: string}>}
   */
  async testToken(token) {
    throw new Error('Not implemented');
  }

  /**
   * Creates a new remote repository.
   * @param {string} token 
   * @param {object} options { name, description, isPrivate }
   * @returns {Promise<{success: boolean, cloneUrl: string, webUrl: string, repo: object}>}
   */
  async createRepository(token, options) {
    throw new Error('Not implemented');
  }

  /**
   * Fetches stats (stars, forks, views) if available.
   */
  async fetchStats(token, repoOwner, repoName) {
    return { stars: 0, forks: 0, views: 0 };
  }
}

module.exports = BaseAdapter;
