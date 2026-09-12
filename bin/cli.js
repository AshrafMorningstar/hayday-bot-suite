#!/usr/bin/env node

const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const { startServer } = require('../src/server/app');

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'menu';

  console.log('\x1b[36m%s\x1b[0m', '═══════════════════════════════════════════════════════════════');
  console.log('\x1b[1m\x1b[32m%s\x1b[0m', '  🌾 Hay Day Bot Suite — Farm Control Center & Automation');
  console.log('\x1b[36m%s\x1b[0m', '═══════════════════════════════════════════════════════════════');

  if (command === 'ui' || command === 'serve' || command === 'web') {
    const port = parseInt(process.env.PORT || '3000', 10);
    try {
      const { port: actualPort } = await startServer(port);
      const url = `http://localhost:${actualPort}`;
      console.log(`\x1b[32m✔ Farm Control Center running at:\x1b[0m \x1b[1m\x1b[4m${url}\x1b[0m`);
      console.log('\x1b[90mPress Ctrl+C to stop the server\x1b[0m\n');

      try {
        const open = require('open');
        await open(url);
      } catch (_) {}
    } catch (err) {
      console.error('\x1b[31mFailed to start server:\x1b[0m', err.message);
      process.exit(1);
    }

  } else if (command === 'bot' || command === 'run' || command === 'live') {
    console.log('\n🌾 Starting Hay Day Bot Live Automation Loop...');
    const pythonProc = spawn('python', ['start_bot.py', '--live'], { stdio: 'inherit', cwd: path.resolve(__dirname, '..') });
    pythonProc.on('exit', (code) => {
      console.log(`\nProcess exited with code ${code}`);
    });

  } else if (command === 'test' || command === 'simulate') {
    console.log('\n🧪 Running Hay Day Bot in Terminal Simulation Mode...');
    const pythonProc = spawn('python', ['start_bot.py', '--simulate'], { stdio: 'inherit', cwd: path.resolve(__dirname, '..') });
    pythonProc.on('exit', (code) => {
      console.log(`\nSimulation completed with code ${code}`);
    });

  } else if (command === 'setup' || command === 'install' || command === 'fix') {
    console.log('\n🛠️ Running 1-Click Automatic Setup & Self-Healing Fixer...');
    const pythonProc = spawn('python', ['installer.py'], { stdio: 'inherit', cwd: path.resolve(__dirname, '..') });
    pythonProc.on('exit', (code) => {
      console.log(`\nSetup completed with code ${code}`);
    });

  } else if (command === 'release' || command === 'releases') {
    console.log('\n📦 Generating Authentic GitHub Monthly Releases...');
    const nodeProc = spawn('node', ['create_releases.js'], { stdio: 'inherit', cwd: path.resolve(__dirname, '..') });
    nodeProc.on('exit', (code) => {
      console.log(`\nReleases generated with code ${code}`);
    });

  } else {
    // Interactive menu
    const pythonProc = spawn('python', ['start_bot.py'], { stdio: 'inherit', cwd: path.resolve(__dirname, '..') });
    pythonProc.on('exit', (code) => {
      process.exit(code || 0);
    });
  }
}

main().catch(console.error);
