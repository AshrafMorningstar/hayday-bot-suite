const BaseAdapter = require('./base-adapter');

class GitHubAdapter extends BaseAdapter {
  constructor() {
    super('GitHub');
  }

  getTokenWizardUrl() {
    return 'https://github.com/settings/tokens/new?description=RepoForge%20Manager&scopes=repo,read:user';
  }

  async testToken(token) {
    if (!token) return { valid: false, error: 'No token provided' };
    try {
      const res = await fetch('https://api.github.com/user', {
        headers: {
          'Authorization': `Bearer ${token.trim()}`,
          'User-Agent': 'RepoForge-App',
          'Accept': 'application/vnd.github.v3+json'
        }
      });

      if (!res.ok) {
        return { valid: false, error: `GitHub API error: ${res.status} ${res.statusText}` };
      }

      const data = await res.json();
      return {
        valid: true,
        user: {
          username: data.login,
          name: data.name || data.login,
          avatar: data.avatar_url,
          profileUrl: data.html_url,
          publicRepos: data.public_repos,
          totalPrivateRepos: data.total_private_repos || 0
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
      const res = await fetch('https://api.github.com/user/repos', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.trim()}`,
          'User-Agent': 'RepoForge-App',
          'Content-Type': 'application/json',
          'Accept': 'application/vnd.github.v3+json'
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
        // Repo might already exist
        if (data.errors && data.errors.some(e => e.message?.includes('already exists'))) {
          // Fetch existing repo
          const userRes = await this.testToken(token);
          if (userRes.valid) {
            const getRes = await fetch(`https://api.github.com/repos/${userRes.user.username}/${sanitizedName}`, {
              headers: { 'Authorization': `Bearer ${token.trim()}`, 'User-Agent': 'RepoForge-App' }
            });
            if (getRes.ok) {
              const existing = await getRes.json();
              return {
                success: true,
                alreadyExisted: true,
                cloneUrl: existing.clone_url,
                sshUrl: existing.ssh_url,
                webUrl: existing.html_url,
                repo: existing
              };
            }
          }
        }
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

  async fetchStats(token, owner, repo) {
    try {
      const res = await fetch(`https://api.github.com/repos/${owner}/${repo}`, {
        headers: {
          'Authorization': token ? `Bearer ${token.trim()}` : '',
          'User-Agent': 'RepoForge-App'
        }
      });
      if (!res.ok) return { stars: 0, forks: 0, views: 0 };
      const data = await res.json();

      let views = 0;
      if (token) {
        try {
          const vRes = await fetch(`https://api.github.com/repos/${owner}/${repo}/traffic/views`, {
            headers: { 'Authorization': `Bearer ${token.trim()}`, 'User-Agent': 'RepoForge-App' }
          });
          if (vRes.ok) {
            const vData = await vRes.json();
            views = vData.count || 0;
          }
        } catch (_) {}
      }

      return {
        stars: data.stargazers_count || 0,
        forks: data.forks_count || 0,
        views
      };
    } catch (_) {
      return { stars: 0, forks: 0, views: 0 };
    }
  }
}

module.exports = GitHubAdapter;
