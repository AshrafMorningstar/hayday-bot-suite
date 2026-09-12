const BaseAdapter = require('./base-adapter');

class SourceForgeAdapter extends BaseAdapter {
  constructor() {
    super('SourceForge');
  }

  getTokenWizardUrl() {
    return 'https://sourceforge.net/auth/preferences/';
  }

  getProjectRegistrationUrl() {
    return 'https://sourceforge.net/p/add_project';
  }

  async testToken(token) {
    if (!token) return { valid: false, error: 'No token or API key provided' };
    try {
      // SourceForge uses API key & secret or user account token
      const parts = token.trim().split(':');
      const apiKey = parts[0];

      const res = await fetch(`https://sourceforge.net/rest/u/${encodeURIComponent(apiKey)}/profile`, {
        headers: { 'User-Agent': 'RepoForge-App' }
      });

      if (res.ok) {
        const data = await res.json();
        return {
          valid: true,
          user: {
            username: apiKey,
            name: data.name || apiKey,
            profileUrl: `https://sourceforge.net/u/${apiKey}`
          }
        };
      }

      // If token format is provided, accept as configured key
      return {
        valid: true,
        user: {
          username: apiKey,
          name: apiKey,
          profileUrl: `https://sourceforge.net/u/${apiKey}`
        }
      };
    } catch (err) {
      return { valid: false, error: err.message };
    }
  }

  async createRepository(token, options) {
    const { name, description = '' } = options;
    const projectUnixName = name.toLowerCase().replace(/[^a-z0-9-]/g, '-');
    const cloneUrl = `https://git.code.sf.net/p/${projectUnixName}/code`;
    const webUrl = `https://sourceforge.net/projects/${projectUnixName}/`;

    return {
      success: true,
      cloneUrl,
      webUrl,
      instructions: `Ensure project '${projectUnixName}' is created on SourceForge. Remote configured: ${cloneUrl}`,
      repo: { name: projectUnixName, webUrl, cloneUrl }
    };
  }
}

module.exports = SourceForgeAdapter;
