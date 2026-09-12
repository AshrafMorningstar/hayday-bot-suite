const BaseAdapter = require('./base-adapter');

class BitbucketAdapter extends BaseAdapter {
  constructor() {
    super('Bitbucket');
  }

  getTokenWizardUrl() {
    return 'https://bitbucket.org/account/settings/app-passwords/';
  }

  getAuthHeader(token) {
    const trimmed = token.trim();
    if (trimmed.includes(':')) {
      // username:app_password format
      const b64 = Buffer.from(trimmed).toString('base64');
      return `Basic ${b64}`;
    }
    return `Bearer ${trimmed}`;
  }

  async testToken(token) {
    if (!token) return { valid: false, error: 'No token provided' };
    try {
      const res = await fetch('https://api.bitbucket.org/2.0/user', {
        headers: {
          'Authorization': this.getAuthHeader(token),
          'Accept': 'application/json'
        }
      });

      if (!res.ok) {
        return { valid: false, error: `Bitbucket API error: ${res.status} ${res.statusText}` };
      }

      const data = await res.json();
      return {
        valid: true,
        user: {
          username: data.username,
          name: data.display_name || data.username,
          avatar: data.links?.avatar?.href,
          profileUrl: data.links?.html?.href
        }
      };
    } catch (err) {
      return { valid: false, error: err.message };
    }
  }

  async createRepository(token, options) {
    const { name, description = '', isPrivate = false } = options;
    const sanitizedSlug = name.toLowerCase().replace(/[^a-z0-9._-]/g, '-');

    try {
      const userRes = await this.testToken(token);
      if (!userRes.valid) return { success: false, error: userRes.error };

      const workspace = userRes.user.username;
      const res = await fetch(`https://api.bitbucket.org/2.0/repositories/${workspace}/${sanitizedSlug}`, {
        method: 'POST',
        headers: {
          'Authorization': this.getAuthHeader(token),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          scm: 'git',
          name: name,
          description: description.slice(0, 350),
          is_private: !!isPrivate
        })
      });

      const data = await res.json();
      if (!res.ok) {
        return { success: false, error: data.error?.message || JSON.stringify(data) };
      }

      const cloneUrl = data.links?.clone?.find(c => c.name === 'https')?.href || `https://bitbucket.org/${workspace}/${sanitizedSlug}.git`;
      const sshUrl = data.links?.clone?.find(c => c.name === 'ssh')?.href || '';

      return {
        success: true,
        cloneUrl,
        sshUrl,
        webUrl: data.links?.html?.href,
        repo: data
      };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }
}

module.exports = BitbucketAdapter;
