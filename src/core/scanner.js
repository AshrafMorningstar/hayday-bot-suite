const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const IGNORED_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'out', 'target',
  'venv', '.venv', 'env', '.env_dir', '__pycache__', '.pytest_cache',
  'bin', 'obj', '.next', '.nuxt', '.cache', 'coverage', '.idea', '.vscode',
  '_organized_projects', '_organized_views', '_organized', '_test_org'
]);

const ECOSYSTEM_MANIFESTS = [
  { file: 'package.json', language: 'JavaScript / TypeScript', ecosystem: 'Node.js' },
  { file: 'Cargo.toml', language: 'Rust', ecosystem: 'Cargo' },
  { file: 'pyproject.toml', language: 'Python', ecosystem: 'Python (Poetry/Flit)' },
  { file: 'requirements.txt', language: 'Python', ecosystem: 'Python (pip)' },
  { file: 'setup.py', language: 'Python', ecosystem: 'Python' },
  { file: 'go.mod', language: 'Go', ecosystem: 'Go Modules' },
  { file: 'pom.xml', language: 'Java', ecosystem: 'Maven' },
  { file: 'build.gradle', language: 'Java / Kotlin', ecosystem: 'Gradle' },
  { file: 'CMakeLists.txt', language: 'C / C++', ecosystem: 'CMake' },
  { file: 'Makefile', language: 'C / C++ / Make', ecosystem: 'Make' },
  { file: 'composer.json', language: 'PHP', ecosystem: 'Composer' },
  { file: 'Gemfile', language: 'Ruby', ecosystem: 'RubyGems' },
  { file: 'pubspec.yaml', language: 'Dart / Flutter', ecosystem: 'Flutter' },
  { file: 'index.html', language: 'HTML / Web', ecosystem: 'Web Frontend' }
];

class Scanner {
  /**
   * Recursively scans rootDir to find all project directories.
   * @param {string} rootDir 
   * @param {number} maxDepth 
   * @returns {Array<object>} List of project objects
   */
  static scan(rootDir, maxDepth = 4) {
    const resolvedRoot = path.resolve(rootDir);
    if (!fs.existsSync(resolvedRoot)) {
      throw new Error(`Directory does not exist: ${resolvedRoot}`);
    }

    const projects = [];
    const visited = new Set();

    function traverse(currentDir, depth) {
      if (depth > maxDepth || visited.has(currentDir)) return;
      visited.add(currentDir);

      let entries;
      try {
        entries = fs.readdirSync(currentDir, { withFileTypes: true });
      } catch (err) {
        return; // permission denied or broken symlink
      }

      // Filter out symlinks/junctions to avoid scanning organized folders or circular links
      const fileNames = entries.filter(e => e.isFile()).map(e => e.name);
      const subdirs = entries.filter(e => {
        if (!e.isDirectory()) return false;
        if (typeof e.isSymbolicLink === 'function' && e.isSymbolicLink()) return false;
        const lower = e.name.toLowerCase();
        if (IGNORED_DIRS.has(lower) || lower.startsWith('.') || lower.startsWith('_')) return false;
        return true;
      });

      // Check if current directory is a project root
      const isProject = Scanner.isProjectRoot(currentDir, fileNames, entries);
      if (isProject) {
        try {
          const meta = Scanner.analyzeProject(currentDir, fileNames, entries);
          projects.push(meta);
        } catch (e) {
          // ignore corrupted project analysis
        }

        // Don't traverse deep inside a project unless it's a monorepo
        const isMonorepo = fileNames.includes('pnpm-workspace.yaml') || 
                           subdirs.some(d => d.name === 'packages' || d.name === 'apps');
        if (!isMonorepo) {
          return;
        }
      }

      for (const subdir of subdirs) {
        traverse(path.join(currentDir, subdir.name), depth + 1);
      }
    }

    traverse(resolvedRoot, 0);
    return projects;
  }

  static isProjectRoot(dirPath, fileNames, entries) {
    if (entries.some(e => e.isDirectory() && e.name === '.git')) {
      return true;
    }
    return ECOSYSTEM_MANIFESTS.some(m => fileNames.includes(m.file));
  }

  static analyzeProject(projectDir, fileNames, entries) {
    const dirName = path.basename(projectDir);
    let name = dirName;
    let description = '';
    let primaryLanguage = 'Unknown';
    let ecosystem = 'Generic';
    let version = '0.1.0';

    // Check manifests
    for (const m of ECOSYSTEM_MANIFESTS) {
      if (fileNames.includes(m.file)) {
        primaryLanguage = m.language;
        ecosystem = m.ecosystem;
        const filePath = path.join(projectDir, m.file);
        try {
          if (m.file === 'package.json') {
            const pkg = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            if (pkg.name) name = pkg.name;
            if (pkg.description) description = pkg.description;
            if (pkg.version) version = pkg.version;
            if (fileNames.includes('tsconfig.json')) {
              primaryLanguage = 'TypeScript';
            } else {
              primaryLanguage = 'JavaScript';
            }
          } else if (m.file === 'Cargo.toml') {
            const cargo = fs.readFileSync(filePath, 'utf8');
            const nameMatch = cargo.match(/name\s*=\s*"(.*?)"/);
            const descMatch = cargo.match(/description\s*=\s*"(.*?)"/);
            if (nameMatch) name = nameMatch[1];
            if (descMatch) description = descMatch[1];
          } else if (m.file === 'pyproject.toml') {
            const toml = fs.readFileSync(filePath, 'utf8');
            const nameMatch = toml.match(/name\s*=\s*"(.*?)"/);
            const descMatch = toml.match(/description\s*=\s*"(.*?)"/);
            if (nameMatch) name = nameMatch[1];
            if (descMatch) description = descMatch[1];
          }
        } catch (_) {}
        break;
      }
    }

    // Git inspection
    const hasGit = entries.some(e => e.isDirectory() && e.name === '.git');
    let gitInfo = {
      isRepo: hasGit,
      branch: 'main',
      remotes: {},
      lastCommitDate: null,
      lastCommitMessage: '',
      commitCount: 0,
      isClean: true,
      hasRemote: false,
      isUnreleased: true,
      isPrivate: false,
      stars: 0,
      forks: 0,
      views: 0
    };

    if (hasGit) {
      try {
        const branch = execSync('git rev-parse --abbrev-ref HEAD', { cwd: projectDir, stdio: ['pipe', 'pipe', 'ignore'] }).toString().trim();
        gitInfo.branch = branch;

        const remotesRaw = execSync('git remote -v', { cwd: projectDir, stdio: ['pipe', 'pipe', 'ignore'] }).toString().trim();
        if (remotesRaw) {
          const lines = remotesRaw.split('\n');
          for (const line of lines) {
            const parts = line.split(/\s+/);
            if (parts.length >= 2) {
              const remoteName = parts[0];
              const remoteUrl = parts[1];
              gitInfo.remotes[remoteName] = remoteUrl;
              gitInfo.hasRemote = true;
              gitInfo.isUnreleased = false;
            }
          }
        }

        const lastCommit = execSync('git log -1 --format="%cd|%s|%an"', { cwd: projectDir, stdio: ['pipe', 'pipe', 'ignore'] }).toString().trim();
        if (lastCommit) {
          const [cDate, cMsg] = lastCommit.split('|');
          gitInfo.lastCommitDate = new Date(cDate).toISOString();
          gitInfo.lastCommitMessage = cMsg;
        }

        const count = execSync('git rev-list --count HEAD', { cwd: projectDir, stdio: ['pipe', 'pipe', 'ignore'] }).toString().trim();
        gitInfo.commitCount = parseInt(count, 10) || 0;

        const status = execSync('git status --porcelain', { cwd: projectDir, stdio: ['pipe', 'pipe', 'ignore'] }).toString().trim();
        gitInfo.isClean = status.length === 0;
      } catch (err) {
        // Fallback if git is not initialized or error occurred
      }
    }

    // Filesystem metrics
    const stats = fs.statSync(projectDir);
    const mtime = stats.mtime.toISOString();
    const atime = stats.atime.toISOString();
    const ctime = stats.ctime.toISOString();

    const hasReadme = fileNames.some(f => f.toLowerCase().startsWith('readme'));
    const hasLicense = fileNames.some(f => f.toLowerCase().startsWith('license'));
    const hasGitignore = fileNames.includes('.gitignore');

    let readmeSnippet = '';
    if (hasReadme) {
      const readmeFile = fileNames.find(f => f.toLowerCase().startsWith('readme'));
      try {
        const content = fs.readFileSync(path.join(projectDir, readmeFile), 'utf8');
        readmeSnippet = content.slice(0, 300).replace(/\r?\n/g, ' ').trim();
      } catch (_) {}
    }

    return {
      id: Buffer.from(projectDir).toString('base64').replace(/=/g, ''),
      name,
      path: projectDir,
      description: description || readmeSnippet.slice(0, 140) || 'No description provided.',
      primaryLanguage,
      ecosystem,
      version,
      hasReadme,
      hasLicense,
      hasGitignore,
      readmeSnippet,
      git: gitInfo,
      timestamps: {
        modified: mtime,
        accessed: atime,
        created: ctime,
        lastActive: gitInfo.lastCommitDate || mtime
      }
    };
  }

  static getSystemPresets() {
    const os = require('os');
    const homedir = os.homedir();
    const presets = [
      { name: 'Current Workspace', path: process.cwd() },
      { name: 'User Home Directory', path: homedir },
      { name: 'Documents', path: path.join(homedir, 'Documents') },
      { name: 'Projects / Code', path: path.join(homedir, 'Projects') },
      { name: 'Desktop', path: path.join(homedir, 'Desktop') }
    ];
    if (process.platform === 'win32') {
      ['M:', 'D:', 'E:', 'C:'].forEach(drive => {
        try {
          if (fs.existsSync(drive + '\\')) {
            presets.push({ name: `Drive ${drive}`, path: drive + '\\' });
          }
        } catch (_) {}
      });
    }
    return presets.filter(p => {
      try { return fs.existsSync(p.path); } catch (_) { return false; }
    });
  }
}

module.exports = Scanner;
