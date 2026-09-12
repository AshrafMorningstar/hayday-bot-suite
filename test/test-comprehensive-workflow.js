const fs = require('fs');
const path = require('path');
const { startServer } = require('../src/server/app');

async function runComprehensiveTest() {
  console.log('=====================================================');
  console.log('  🧪 Running End-to-End Workflow & Endpoint Tests');
  console.log('=====================================================\n');

  const { server, port } = await startServer(4567);
  const baseUrl = `http://localhost:${port}`;

  try {
    // 1. Status & Presets
    console.log('1. Testing /api/status endpoint...');
    const statusRes = await fetch(`${baseUrl}/api/status`);
    const status = await statusRes.json();
    if (status.status !== 'online') throw new Error('API status not online');
    console.log(`   ✔ Status: Online, default dir: ${status.defaultScanDir}`);

    // 2. Scan Real Projects Directory
    console.log('\n2. Testing /api/scan on real projects...');
    const scanTarget = path.resolve(__dirname, '..');
    const scanRes = await fetch(`${baseUrl}/api/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dirPath: scanTarget })
    });
    const scanData = await scanRes.json();
    if (!scanData.success || scanData.projects.length === 0) {
      throw new Error(`Scan failed or returned 0 projects: ${JSON.stringify(scanData)}`);
    }
    console.log(`   ✔ Scanned ${scanData.total} project(s): ${scanData.projects.map(p => p.name).join(', ')}`);

    // 3. Organization Plan Preview
    console.log('\n3. Testing /api/organize/plan (preview calculation)...');
    const testOrganizedDir = path.join(path.dirname(scanTarget), '_test_organized');
    const planRes = await fetch(`${baseUrl}/api/organize/plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        destinationDir: testOrganizedDir,
        strategy: 'activity'
      })
    });
    const planData = await planRes.json();
    if (!planData.success || !Array.isArray(planData.plan)) {
      throw new Error(`Plan calculation failed: ${JSON.stringify(planData)}`);
    }
    console.log(`   ✔ Plan generated: ${planData.plan.length} items mapped`);
    for (const item of planData.plan) {
      console.log(`     • ${item.name} -> [${item.category}] -> ${item.targetPath}`);
    }

    // 4. Organization Execution (Junction mode)
    console.log('\n4. Testing /api/organize/execute (creating junctions)...');
    const execRes = await fetch(`${baseUrl}/api/organize/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        destinationDir: testOrganizedDir,
        strategy: 'activity',
        mode: 'junction'
      })
    });
    const execData = await execRes.json();
    if (!execData.success) {
      throw new Error(`Execution failed: ${JSON.stringify(execData)}`);
    }
    console.log(`   ✔ Organized ${execData.executedCount} projects successfully.`);

    // Verify folder was created
    if (!fs.existsSync(testOrganizedDir)) {
      throw new Error('Organized directory was not created on disk!');
    }
    console.log(`   ✔ Directory exists on disk: ${testOrganizedDir}`);

    // 5. Organization Rollback (Undo)
    console.log('\n5. Testing /api/organize/rollback (reversing organization)...');
    const undoRes = await fetch(`${baseUrl}/api/organize/rollback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ destinationDir: testOrganizedDir })
    });
    const undoData = await undoRes.json();
    if (!undoData.success) {
      throw new Error(`Rollback failed: ${JSON.stringify(undoData)}`);
    }
    console.log(`   ✔ Rollback successful: reversed ${undoData.reversedCount} folders.`);

    // Clean up test dir if empty
    try {
      if (fs.existsSync(testOrganizedDir)) {
        fs.rmSync(testOrganizedDir, { recursive: true, force: true });
      }
    } catch (_) {}

    // 6. AI README Generation & Save
    console.log('\n6. Testing /api/ai/readme & /api/ai/save-readme...');
    const targetProject = scanData.projects[0];
    const aiRes = await fetch(`${baseUrl}/api/ai/readme`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectPath: targetProject.path })
    });
    const aiData = await aiRes.json();
    if (!aiData.success || !aiData.readme) {
      throw new Error('AI README synthesis failed');
    }
    console.log(`   ✔ AI synthesized README (${aiData.readme.length} chars)`);

    const saveRes = await fetch(`${baseUrl}/api/ai/save-readme`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectPath: targetProject.path,
        content: aiData.readme
      })
    });
    const saveData = await saveRes.json();
    if (!saveData.success || !fs.existsSync(saveData.savedPath)) {
      throw new Error('Failed to save README to disk');
    }
    console.log(`   ✔ Saved README to disk: ${saveData.savedPath}`);

    // 7. Privacy Audit
    console.log('\n7. Testing /api/privacy/audit...');
    const auditRes = await fetch(`${baseUrl}/api/privacy/audit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectPath: targetProject.path })
    });
    const auditData = await auditRes.json();
    if (!auditData.success) throw new Error('Privacy audit failed');
    console.log(`   ✔ Privacy Audit: Safe=${auditData.audit.safe}, Findings=${auditData.audit.findings.length}`);

    // 8. Showcase Generation
    console.log('\n8. Testing /api/showcase/export...');
    const testShowcaseFile = path.join(scanTarget, 'TEST_SHOWCASE.md');
    const showcaseRes = await fetch(`${baseUrl}/api/showcase/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ outputPath: testShowcaseFile })
    });
    const showcaseData = await showcaseRes.json();
    if (!showcaseData.success || !fs.existsSync(testShowcaseFile)) {
      throw new Error('Showcase export failed');
    }
    console.log(`   ✔ Portfolio Showcase exported to: ${testShowcaseFile}`);
    fs.unlinkSync(testShowcaseFile); // clean up

    console.log('\n=====================================================');
    console.log('  🎉 ALL END-TO-END TESTS PASSED (100% SUCCESS)');
    console.log('=====================================================\n');
  } finally {
    server.close();
  }
}

runComprehensiveTest().catch(err => {
  console.error('\n❌ Test failed:', err);
  process.exit(1);
});
