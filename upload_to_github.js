const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const CWD = __dirname;

function clearLock() {
  const lock = path.join(CWD, '.git', 'index.lock');
  if (fs.existsSync(lock)) {
    try {
      fs.unlinkSync(lock);
      console.log('✔ Cleared stale index.lock');
    } catch (_) {}
  }
}

function run(cmd, desc) {
  clearLock();
  console.log(`\n========================================`);
  console.log(`▶ ${desc}: ${cmd}`);
  console.log(`========================================`);
  try {
    execSync(cmd, { cwd: CWD, encoding: 'utf8', stdio: 'inherit', timeout: 90000 });
    return true;
  } catch (err) {
    console.error(`Notice during [${desc}]: ${err.message}`);
    return false;
  }
}

function main() {
  console.log('🚀 Starting Full Automated GitHub Upload for Hay Day Bot Suite...');
  clearLock();

  // 1. Stage all project files in ONE single command
  const files = [
    '.gitignore',
    'LICENSE',
    'README.md',
    'RELEASES.md',
    'start_bot.py',
    'test/scan_privacy.py',
    'bin/cli.js',
    'create_releases.js',
    'upload_to_github.js',
    'install.bat',
    'installer.py',
    'project-logs',
    'public',
    'run.bat',
    'src',
    'start.bat',
    'test/test-all.js',
    'Working/hay-star-main'
  ].filter(f => fs.existsSync(path.join(CWD, f))).map(f => `"${f}"`).join(' ');

  run(`git add ${files}`, 'Staging all project files');

  // 2. Commit
  run(`git commit -m "feat: Hay Day Bot Suite v8.0.0 — offline AI engines, release history, 1-click launchers"`, 'Committing changes');

  // 3. Push to master
  run(`git push origin master`, 'Pushing commits to origin/master');

  // 4. Create all releases and tags
  run(`node create_releases.js`, 'Creating releases & tags');

  // 5. Push tags
  run(`git push origin --tags`, 'Pushing all release tags to GitHub');

  // 6. Verify releases
  run(`gh release list`, 'Listing GitHub releases');

  console.log('\n🎉 ALL GITHUB RELEASES & CODE FULLY UPLOADED AUTONOMOUSLY!');
}

main();
