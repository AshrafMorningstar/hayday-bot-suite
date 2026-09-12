const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const GitHubAdapter = require('./github-adapter');
const GitLabAdapter = require('./gitlab-adapter');
const CodebergAdapter = require('./codeberg-adapter');
const BitbucketAdapter = require('./bitbucket-adapter');
const SourceForgeAdapter = require('./sourceforge-adapter');
const PrivacyGuard = require('../core/privacy-guard');

class ForgeManager {
  constructor() {
    this.configDir = path.join(os.homedir(), '.repoforge');
    this.configFile = path.join(this.configDir, 'config.json');

    this.adapters = {
      github: new GitHubAdapter(),
      gitlab: new GitLabAdapter(),
      codeberg: new CodebergAdapter(),
      bitbucket: new BitbucketAdapter(),
      sourceforge: new SourceForgeAdapter()
    };

    this.initStorage();
  }

  initStorage() {
    if (!fs.existsSync(this.configDir)) {
      try {
        fs.mkdirSync(this.configDir, { recursive: true });
      } catch (_) {}
    }
    if (!fs.existsSync(this.configFile)) {
      try {
        fs.writeFileSync(this.configFile, JSON.stringify({
          tokens: {},
          settings: { defaultPlatforms: ['github'], checkSecrets: true }
        }, null, 2));
      } catch (_) {}
    }
  }

  getConfig() {
    try {
      return JSON.parse(fs.readFileSync(this.configFile, 'utf8'));
    } catch (_) {
      return { tokens: {}, settings: {} };
    }
  }

  saveConfig(config) {
    try {
      fs.writeFileSync(this.configFile, JSON.stringify(config, null, 2));
    } catch (_) {}
  }

  getGhCliToken() {
    try {
      const token = execSync('gh auth token', { stdio: ['pipe', 'pipe', 'ignore'] }).toString().trim();
      if (token && token.startsWith('gh')) {
        return token;
      }
    } catch (_) {}
    return null;
  }

  getPlatformInfo() {
    const config = this.getConfig();
    const tokens = config.tokens || {};
    const ghCliToken = this.getGhCliToken();
    const githubConfigured = !!tokens.github || !!ghCliToken;

    return [
      {
        id: 'github',
        name: 'GitHub',
        icon: 'github',
        configured: githubConfigured,
        isGhCli: !tokens.github && !!ghCliToken,
        wizardUrl: this.adapters.github.getTokenWizardUrl(),
        scopeDesc: githubConfigured ? (tokens.github ? 'Custom API Token configured' : 'Auto-detected from local GitHub CLI (gh)') : 'repo, read:user'
      },
      {
        id: 'gitlab',
        name: 'GitLab',
        icon: 'gitlab',
        configured: !!tokens.gitlab,
        wizardUrl: this.adapters.gitlab.getTokenWizardUrl(),
        scopeDesc: 'api, read_user, write_repository'
      },
      {
        id: 'codeberg',
        name: 'Codeberg (Forgejo/Gitea)',
        icon: 'codeberg',
        configured: !!tokens.codeberg,
        wizardUrl: this.adapters.codeberg.getTokenWizardUrl(),
        scopeDesc: 'Applications / Personal Access Token'
      },
      {
        id: 'bitbucket',
        name: 'Bitbucket',
        icon: 'bitbucket',
        configured: !!tokens.bitbucket,
        wizardUrl: this.adapters.bitbucket.getTokenWizardUrl(),
        scopeDesc: 'App Password: username:app_password'
      },
      {
        id: 'sourceforge',
        name: 'SourceForge',
        icon: 'sourceforge',
        configured: !!tokens.sourceforge,
        wizardUrl: this.adapters.sourceforge.getTokenWizardUrl(),
        scopeDesc: 'API Key or Username'
      }
    ];
  }

  async testPlatformToken(platformId, token) {
    const adapter = this.adapters[platformId];
    if (!adapter) throw new Error(`Unknown platform: ${platformId}`);

    const res = await adapter.testToken(token);
    if (res.valid) {
      const config = this.getConfig();
      config.tokens = config.tokens || {};
      config.tokens[platformId] = token.trim();
      this.saveConfig(config);
    }
    return res;
  }

  saveToken(platformId, token) {
    const config = this.getConfig();
    config.tokens = config.tokens || {};
    config.tokens[platformId] = token.trim();
    this.saveConfig(config);
  }

  /**
   * Automatically initializes git repo (if needed), verifies privacy guard,
   * creates remote repositories on target platforms, and pushes branches.
   */
  async publishProject(projectPath, options = {}) {
    const {
      platforms = ['github'],
      isPrivate = false,
      commitMessage = 'Initial release via RepoForge',
      skipPrivacyCheck = false
    } = options;

    const resolvedPath = path.resolve(projectPath);
    if (!fs.existsSync(resolvedPath)) {
      throw new Error(`Project directory not found: ${resolvedPath}`);
    }

    // 1. Run Privacy Guard
    if (!skipPrivacyCheck) {
      const audit = PrivacyGuard.audit(resolvedPath);
      if (!audit.safe) {
        return {
          success: false,
          haltedByPrivacyGuard: true,
          findings: audit.findings,
          message: `Privacy Guard detected ${audit.findings.length} sensitive secret(s) or file(s). Publication halted for safety.`
        };
      }
    }

    // 2. Ensure git repository is initialized
    const gitDir = path.join(resolvedPath, '.git');
    if (!fs.existsSync(gitDir)) {
      execSync('git init', { cwd: resolvedPath, stdio: 'ignore' });
      execSync('git branch -M main', { cwd: resolvedPath, stdio: 'ignore' });
    }

    // Ensure at least one commit
    try {
      execSync('git rev-parse HEAD', { cwd: resolvedPath, stdio: ['pipe', 'pipe', 'ignore'] });
    } catch (_) {
      // No commits yet
      execSync('git add -A', { cwd: resolvedPath, stdio: 'ignore' });
      execSync(`git commit -m "${commitMessage.replace(/"/g, '\\"')}"`, { cwd: resolvedPath, stdio: 'ignore' });
    }

    const currentBranch = execSync('git rev-parse --abbrev-ref HEAD', { cwd: resolvedPath }).toString().trim() || 'main';
    const projectName = path.basename(resolvedPath);
    const config = this.getConfig();
    const results = {};

    for (const pid of platforms) {
      const adapter = this.adapters[pid];
      if (!adapter) {
        results[pid] = { success: false, error: `Unsupported platform: ${pid}` };
        continue;
      }

      let token = config.tokens?.[pid];
      if (!token && pid === 'github') {
        token = this.getGhCliToken();
      }
      if (!token) {
        results[pid] = { success: false, error: `No token configured for ${adapter.getName()}. Use Token Assistant first.` };
        continue;
      }

      try {
        const repoRes = await adapter.createRepository(token, {
          name: projectName,
          description: options.description || `Autonomous repository managed by RepoForge`,
          isPrivate
        });

        if (!repoRes.success && !repoRes.cloneUrl) {
          results[pid] = { success: false, error: repoRes.error };
          continue;
        }

        const remoteName = pid === 'github' ? 'origin' : pid;
        const cloneUrl = repoRes.cloneUrl;

        // Add or update git remote
        try {
          execSync(`git remote remove ${remoteName}`, { cwd: resolvedPath, stdio: 'ignore' });
        } catch (_) {}

        execSync(`git remote add ${remoteName} "${cloneUrl}"`, { cwd: resolvedPath, stdio: 'ignore' });

        // Authenticated push URL
        let pushUrl = cloneUrl;
        if (pid === 'github') {
          pushUrl = cloneUrl.replace('https://', `https://${token}@`);
        } else if (pid === 'gitlab') {
          pushUrl = cloneUrl.replace('https://', `https://oauth2:${token}@`);
        } else if (pid === 'codeberg') {
          pushUrl = cloneUrl.replace('https://', `https://${token}@`);
        }

        try {
          execSync(`git push -u "${pushUrl}" ${currentBranch}`, {
            cwd: resolvedPath,
            stdio: ['pipe', 'pipe', 'pipe']
          });
          results[pid] = {
            success: true,
            webUrl: repoRes.webUrl,
            cloneUrl: repoRes.cloneUrl,
            remoteName
          };
        } catch (pushErr) {
          results[pid] = {
            success: false,
            error: `Created remote repository, but push failed: ${pushErr.message}`
          };
        }
      } catch (err) {
        results[pid] = { success: false, error: err.message };
      }
    }

    return {
      success: Object.values(results).some(r => r.success),
      results
    };
  }
}

module.exports = ForgeManager;
