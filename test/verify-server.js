/**
 * Autonomous Server Verification Script
 * Starts the server, hits endpoints, verifies index.html and CSS delivery, then exits cleanly.
 */

const { startServer } = require('../src/server/app');

async function verify() {
  console.log('🚀 Launching RepoForge server for automated verification...');
  const { server, port } = await startServer(4199);
  console.log(`✔ Server successfully started on port ${port}`);

  try {
    // 1. Fetch HTML UI
    const htmlRes = await fetch(`http://localhost:${port}/`);
    if (!htmlRes.ok) throw new Error(`Failed to fetch index.html: ${htmlRes.status}`);
    const html = await htmlRes.text();
    if (!html.includes('RepoForge') || !html.includes('style.css')) {
      throw new Error('Index.html did not contain expected content');
    }
    console.log('✔ Verified index.html UI delivery');

    // 2. Fetch style.css
    const cssRes = await fetch(`http://localhost:${port}/style.css`);
    if (!cssRes.ok) throw new Error(`Failed to fetch style.css: ${cssRes.status}`);
    const css = await cssRes.text();
    if (!css.includes('--bg-main')) throw new Error('CSS delivery failed');
    console.log('✔ Verified modern glassmorphic style.css delivery');

    // 3. Fetch app.js
    const jsRes = await fetch(`http://localhost:${port}/app.js`);
    if (!jsRes.ok) throw new Error(`Failed to fetch app.js: ${jsRes.status}`);
    console.log('✔ Verified app.js controller delivery');

    // 4. Test API Status
    const apiRes = await fetch(`http://localhost:${port}/api/status`);
    const status = await apiRes.json();
    if (status.status !== 'online') throw new Error('API status not online');
    console.log(`✔ Verified REST API: ${JSON.stringify(status)}`);

    console.log('\n\x1b[32m🎉 FULL AUTONOMOUS VERIFICATION SUCCESSFUL!\x1b[0m\n');
  } finally {
    server.close();
  }
}

verify().catch(err => {
  console.error('\x1b[31mVerification failed:\x1b[0m', err.message);
  process.exit(1);
});
