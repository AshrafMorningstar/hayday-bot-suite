const BaseAdapter = require('./base-adapter');

class GitLabAdapter extends BaseAdapter {
  constructor(baseUrl = 'https://gitlab.com') {
    super('GitLab');
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  getTokenWizardUrl() {
    return `${this.baseUrl}/-/user_settings/personal_access_tokens?name=RepoForge&scopes=api,read_user,write_repository`;
  }

  async testToken(token) {
    if (!token) return { valid: false, error: 'No token provided' };
    try {
      const res = await fetch(`${this.baseUrl}/api/v4/user`, {
        headers: {
          'PRIVATE-TOKEN': token.trim(),
          'User-Agent': 'RepoForge-App'
        }
      });

      if (!res.ok) {
        return { valid: false, error: `GitLab API error: ${res.status} ${res.statusText}` };
      }

      const data = await res.json();
      return {
        valid: true,
        user: {
          username: data.username,
          name: data.name || data.username,
          avatar: data.avatar_url,
          profileUrl: data.web_url
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
      const res = await fetch(`${this.baseUrl}/api/v4/projects`, {
        method: 'POST',
        headers: {
          'PRIVATE-TOKEN': token.trim(),
          'Content-Type': 'application/json',
          'User-Agent': 'RepoForge-App'
        },
        body: JSON.stringify({
          name: sanitizedName,
          path: sanitizedName,
          description: description.slice(0, 350),
          visibility: isPrivate ? 'private' : 'public',
          initialize_with_readme: false
        })
      });

      const data = await res.json();
      if (!res.ok) {
        return { success: false, error: data.message || JSON.stringify(data) };
      }

      return {
        success: true,
        cloneUrl: data.http_url_to_repo,
        sshUrl: data.ssh_url_to_repo,
        webUrl: data.web_url,
        repo: data
      };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }
}

module.exports = GitLabAdapter;
