const BaseAdapter = require('./base-adapter');

class CodebergAdapter extends BaseAdapter {
  constructor(baseUrl = 'https://codeberg.org') {
    super('Codeberg');
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  getTokenWizardUrl() {
    return `${this.baseUrl}/user/settings/applications`;
  }

  async testToken(token) {
    if (!token) return { valid: false, error: 'No token provided' };
    try {
      const res = await fetch(`${this.baseUrl}/api/v1/user`, {
        headers: {
          'Authorization': `token ${token.trim()}`,
          'User-Agent': 'RepoForge-App',
          'Accept': 'application/json'
        }
      });

      if (!res.ok) {
        return { valid: false, error: `Codeberg/Forgejo API error: ${res.status} ${res.statusText}` };
      }

      const data = await res.json();
      return {
        valid: true,
        user: {
          username: data.username,
          name: data.full_name || data.username,
          avatar: data.avatar_url,
          profileUrl: `${this.baseUrl}/${data.username}`
        }
      };
    } catch (err) {
      return { valid: false, error: err.message };
    }
  }

  async createRepository(token, options) {
    const { name, description = '', isPrivate = false } = options;
    const sanitizedName = name.replace(/[^a-zA-Z0-9._-]/g, '-');

    try {
      const res = await fetch(`${this.baseUrl}/api/v1/user/repos`, {
        method: 'POST',
        headers: {
          'Authorization': `token ${token.trim()}`,
          'Content-Type': 'application/json',
          'User-Agent': 'RepoForge-App'
        },
        body: JSON.stringify({
          name: sanitizedName,
          description: description.slice(0, 350),
          private: !!isPrivate,
          auto_init: false
        })
      });

      const data = await res.json();
      if (!res.ok) {
        return { success: false, error: data.message || JSON.stringify(data) };
      }

      return {
        success: true,
        cloneUrl: data.clone_url,
        sshUrl: data.ssh_url,
        webUrl: data.html_url,
        repo: data
      };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }
}

module.exports = CodebergAdapter;
