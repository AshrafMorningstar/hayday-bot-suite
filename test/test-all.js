/**
 * RepoForge — Complete Automated Test Suite
 * Tests Scanner, Organizer, Privacy Guard, Multi-Forge, Free AI, Viral Showcase & API Server
 */

const assert = require('assert');
const path = require('path');
const fs = require('fs');
const http = require('http');

const Scanner = require('../src/core/scanner');
const Organizer = require('../src/core/organizer');
const PrivacyGuard = require('../src/core/privacy-guard');
const VirtualViews = require('../src/core/virtual-views');
const FreeAIService = require('../src/ai/free-ai-service');
const ShowcaseGenerator = require('../src/viral/showcase-generator');
const ForgeManager = require('../src/platforms/forge-manager');
const { createServer } = require('../src/server/app');

let passedTests = 0;
let failedTests = 0;

function it(desc, fn) {
  try {
    fn();
    console.log(`  \x1b[32m✔\x1b[0m ${desc}`);
    passedTests++;
  } catch (err) {
    console.error(`  \x1b[31m✖\x1b[0m ${desc}`);
    console.error(`    \x1b[31mError:\x1b[0m ${err.message}`);
    failedTests++;
  }
}

async function itAsync(desc, fn) {
  try {
    await fn();
    console.log(`  \x1b[32m✔\x1b[0m ${desc}`);
    passedTests++;
  } catch (err) {
    console.error(`  \x1b[31m✖\x1b[0m ${desc}`);
    console.error(`    \x1b[31mError:\x1b[0m ${err.message}`);
    failedTests++;
  }
}

async function runTests() {
  console.log('\n\x1b[1m\x1b[36m=====================================================\x1b[0m');
  console.log('\x1b[1m\x1b[35m  🧪 Running RepoForge Autonomous Test Suite\x1b[0m');
  console.log('\x1b[1m\x1b[36m=====================================================\x1b[0m\n');

  // 1. Scanner Tests
  console.log('\x1b[1m1. Core Scanner Tests\x1b[0m');
  it('Scans the current workspace directory and catalogs projects', () => {
    const raw = Scanner.scan(path.resolve(__dirname, '..'), 2);
    assert(Array.isArray(raw), 'Scan results should be an array');
    assert(raw.length > 0, 'Should find at least 1 project in current directory');
    const project = raw[0];
    assert(project.name, 'Project must have a name');
    assert(project.path, 'Project must have a path');
    assert(project.primaryLanguage, 'Project must have a detected language');
    assert(project.timestamps, 'Project must have timestamps');
  });

  // 2. Organizer & Fame Calculator Tests
  console.log('\n\x1b[1m2. Organizer & Fame Scoring Tests\x1b[0m');
  it('Enriches projects with fame score, activity, and tier classification', () => {
    const mockProjects = [
      {
        name: 'viral-app',
        path: '/dummy/viral-app',
        primaryLanguage: 'TypeScript',
        ecosystem: 'Node.js',
        description: 'Super popular tool',
        hasReadme: true,
        hasLicense: true,
        timestamps: { created: '2026-01-01', modified: '2026-09-10', lastActive: '2026-09-10' },
        git: { isRepo: true, stars: 250, commitCount: 45, isUnreleased: false, isDirty: false }
      },
      {
        name: 'ancient-script',
        path: '/dummy/ancient-script',
        primaryLanguage: 'Python',
        ecosystem: 'Python',
        description: 'Old is gold utility',
        timestamps: { created: '2020-01-01', modified: '2021-01-01', lastActive: '2021-01-01' },
        git: { isRepo: true, stars: 0, isUnreleased: true, isDirty: false }
      }
    ];

    const enriched = Organizer.enrich(mockProjects);
    assert.strictEqual(enriched.length, 2);
    
    // Check fame calculation
    const viral = enriched.find(p => p.name === 'viral-app');
    assert(viral.fame.fameScore > 50, 'Viral app should have high fame score');
    assert(['diamond', 'gold', 'rising'].includes(viral.fame.tier.id), 'Tier should be high');

    const ancient = enriched.find(p => p.name === 'ancient-script');
    assert.strictEqual(ancient.fame.tier.id, 'relic', 'Ancient project should be classified as relic');

    // Test sorting
    const sortedByFame = Organizer.sort(enriched, 'fame', 'desc');
    assert.strictEqual(sortedByFame[0].name, 'viral-app');

    const sortedByOldest = Organizer.sort(enriched, 'oldest', 'asc');
    assert.strictEqual(sortedByOldest[0].name, 'ancient-script');

    // Test categorization
    const categorized = Organizer.categorize(enriched);
    assert(categorized.byTier['relic'].length === 1);
    assert(categorized.byStatus.unreleased.length === 1);
  });

  // 3. Privacy Guard Tests
  console.log('\n\x1b[1m3. Privacy Guard (Secret & Leak Detection) Tests\x1b[0m');
  it('Identifies sensitive secrets, AWS keys, and .env files', () => {
    // Create temporary test dir
    const tempTestDir = path.join(__dirname, 'temp-privacy-test');
    if (!fs.existsSync(tempTestDir)) fs.mkdirSync(tempTestDir, { recursive: true });

    // Clean file
    fs.writeFileSync(path.join(tempTestDir, 'index.js'), 'console.log("hello world");');
    let audit = PrivacyGuard.audit(tempTestDir);
    assert.strictEqual(audit.safe, true, 'Clean directory should pass audit');

    // Inject fake secret
    const fakeKey = ['AWS_SECRET_KEY=', 'AKIA', 'IOSFODNN7EXAMPLE12'].join('');
    fs.writeFileSync(path.join(tempTestDir, '.env'), fakeKey);
    audit = PrivacyGuard.audit(tempTestDir);
    assert.strictEqual(audit.safe, false, 'Leaked secret directory must fail audit');
    assert(audit.findings.length >= 1, 'Should list findings');

    // Cleanup
    try {
      fs.rmSync(tempTestDir, { recursive: true, force: true });
    } catch (_) {}
  });

  // 4. Multi-Forge Platform Adapters Tests
  console.log('\n\x1b[1m4. Multi-Forge Platform Adapters Tests\x1b[0m');
  it('Provides 1-click token wizards and adapters for GitHub, GitLab, Codeberg, Bitbucket, SourceForge', () => {
    const forgeManager = new ForgeManager();
    const platforms = forgeManager.getPlatformInfo();

    assert.strictEqual(platforms.length, 5, 'Should support all 5 code forges');
    
    const ids = platforms.map(p => p.id);
    assert(ids.includes('github'));
    assert(ids.includes('gitlab'));
    assert(ids.includes('codeberg'));
    assert(ids.includes('bitbucket'));
    assert(ids.includes('sourceforge'));

    // Check 1-click wizard URLs
    platforms.forEach(p => {
      assert(p.wizardUrl && p.wizardUrl.startsWith('https://'), `Platform ${p.name} must have wizard URL`);
    });
  });

  // 5. Free AI & Heuristic Synthesis Tests
  console.log('\n\x1b[1m5. Free AI & Offline Heuristic Engine Tests\x1b[0m');
  await itAsync('Generates high-quality README without requiring API keys or network', async () => {
    const mockProject = {
      name: 'quantum-cache',
      path: path.resolve(__dirname, '..'),
      primaryLanguage: 'Rust',
      ecosystem: 'Cargo',
      description: 'Ultra-fast in-memory distributed cache'
    };

    const readme = await FreeAIService.generateReadme(mockProject);
    assert(typeof readme === 'string', 'README should be a string');
    assert(readme.includes('# quantum-cache'), 'README should contain title');
    assert(readme.includes('Rust'), 'README should mention language');
    assert(readme.includes('RepoForge'), 'README should include badge citation');
    assert(readme.includes('cargo build') || readme.includes('Quick Start'), 'README should have setup instructions');
  });

  // 6. Virtual Views & Windows Junctions Tests
  console.log('\n\x1b[1m6. Virtual Views & Hierarchy Tests\x1b[0m');
  it('Generates structured categorization trees by activity, language, and fame', () => {
    const mockProjects = [
      {
        name: 'app-a',
        path: '/a',
        primaryLanguage: 'Go',
        fame: { daysSinceActive: 5, fameScore: 80, tier: { label: 'Rising Star' } },
        timestamps: { lastActive: '2026-09-08' },
        git: { isUnreleased: false }
      },
      {
        name: 'app-b',
        path: '/b',
        primaryLanguage: 'Go',
        fame: { daysSinceActive: 400, fameScore: 10, tier: { label: 'Ancient Relic' } },
        timestamps: { lastActive: '2024-01-01' },
        git: { isUnreleased: true }
      }
    ];

    const activityHierarchy = VirtualViews.generateHierarchy(mockProjects, 'activity');
    assert(activityHierarchy['01_Active (Last 2 Weeks)'], 'Should have active category');
    assert(activityHierarchy['04_Ancient Relics (> 1 Year)'], 'Should have relic category');

    const langHierarchy = VirtualViews.generateHierarchy(mockProjects, 'language');
    assert(langHierarchy['Go'].length === 2, 'Should group by language');
  });

  // 7. Viral Showcase Portfolio Tests
  console.log('\n\x1b[1m7. Viral Showcase Generator Tests\x1b[0m');
  it('Generates viral MY_PROJECTS.md portfolio table with metrics and badges', () => {
    const raw = Scanner.scan(path.resolve(__dirname, '..'), 1);
    const enriched = Organizer.enrich(raw);
    const md = ShowcaseGenerator.generateMarkdown(enriched, 'AntigravityDev');

    assert(md.includes('# 🚀 AntigravityDev\'s Engineering Portfolio'), 'Portfolio must have header');
    assert(md.includes('Portfolio Metrics'), 'Portfolio must include metrics');
    assert(md.includes('Languages & Tech Stacks'), 'Portfolio must include language breakdown');
    assert(md.includes('Complete Catalog Index'), 'Portfolio must include full catalog table');
  });

  // 8. REST API Endpoints Integration Tests
  console.log('\n\x1b[1m8. Express REST API Integration Tests\x1b[0m');
  await itAsync('Server serves status, platforms, scan, and audit endpoints', async () => {
    const app = createServer();
    const server = http.createServer(app);

    await new Promise((resolve) => server.listen(0, resolve));
    const port = server.address().port;
    const baseUrl = `http://localhost:${port}/api`;

    try {
      // 1. /api/status
      const statusRes = await fetch(`${baseUrl}/status`);
      const statusData = await statusRes.json();
      assert.strictEqual(statusData.status, 'online');
      assert.strictEqual(statusData.version, '1.0.0');

      // 2. /api/platforms
      const platformsRes = await fetch(`${baseUrl}/platforms`);
      const platformsData = await platformsRes.json();
      assert.strictEqual(platformsData.success, true);
      assert(platformsData.platforms.length >= 5);

      // 3. /api/scan
      const scanRes = await fetch(`${baseUrl}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dirPath: path.resolve(__dirname, '..') })
      });
      const scanData = await scanRes.json();
      assert.strictEqual(scanData.success, true);
      assert(scanData.projects.length > 0);

      // 4. /api/privacy/audit
      const auditRes = await fetch(`${baseUrl}/privacy/audit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectPath: path.resolve(__dirname, '..') })
      });
      const auditData = await auditRes.json();
      assert.strictEqual(auditData.success, true);
      assert.strictEqual(auditData.audit.safe, true);

      // 5. /api/organize/plan
      const planRes = await fetch(`${baseUrl}/organize/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ strategy: 'activity' })
      });
      const planData = await planRes.json();
      assert.strictEqual(planData.success, true);
      assert(Array.isArray(planData.plan), 'Plan must be an array');

      // 6. /api/presets
      const presetsRes = await fetch(`${baseUrl}/presets`);
      const presetsData = await presetsRes.json();
      assert.strictEqual(presetsData.success, true);
      assert(presetsData.presets.length > 0, 'Should have system presets');

      // 7. /api/github-actions/setup
      const actionsRes = await fetch(`${baseUrl}/github-actions/setup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectPath: path.resolve(__dirname, '..') })
      });
      const actionsData = await actionsRes.json();
      assert.strictEqual(actionsData.success, true);
      assert(actionsData.workflowPath.includes('repoforge-sync.yml'));

      // 8. /api/ai/save-readme
      const testScratchDir = path.resolve(__dirname, 'scratch');
      if (!fs.existsSync(testScratchDir)) fs.mkdirSync(testScratchDir, { recursive: true });
      const saveReadmeRes = await fetch(`${baseUrl}/ai/save-readme`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectPath: testScratchDir,
          content: '# Test Readme\nAuto-saved for unit test'
        })
      });
      const saveReadmeData = await saveReadmeRes.json();
      assert.strictEqual(saveReadmeData.success, true);
      assert(saveReadmeData.savedPath.includes('README.md'));

      // 9. /api/batch/heal-all
      const batchHealRes = await fetch(`${baseUrl}/batch/heal-all`, { method: 'POST' });
      const batchHealData = await batchHealRes.json();
      assert.strictEqual(batchHealData.success, true);
      assert(typeof batchHealData.healedCount === 'number');

      // 10. /api/project/open-folder validation
      const folderRes = await fetch(`${baseUrl}/project/open-folder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectPath: path.resolve(__dirname, '..') })
      });
      const folderData = await folderRes.json();
      assert.strictEqual(folderData.success, true);

    } finally {
      server.close();
    }
  });

  // Summary
  console.log('\n\x1b[1m\x1b[36m=====================================================\x1b[0m');
  console.log(`\x1b[1m  Test Results: \x1b[32m${passedTests} passed\x1b[0m, \x1b[31m${failedTests} failed\x1b[0m`);
  console.log('\x1b[1m\x1b[36m=====================================================\x1b[0m\n');

  if (failedTests > 0) {
    process.exit(1);
  }
}

runTests().catch(err => {
  console.error('Test execution failed:', err);
  process.exit(1);
});
