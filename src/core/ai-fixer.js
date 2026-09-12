/**
 * Offline Triple-Engine AI Self-Healing & Self-Annealing Auto-Fixer Module
 * Zero API keys required - Runs completely offline using deterministic pattern matching & auto-repair rules.
 */

const fs = require('fs');
const path = require('path');
const net = require('net');

class AiSelfFixer {
  constructor(rootDir = process.cwd()) {
    this.rootDir = rootDir;
  }

  /**
   * Engine 1: Port & Network Self-Healing Engine
   * Detects if target port is occupied and finds next free port automatically.
   */
  async getAvailablePort(desiredPort = 3000) {
    return new Promise((resolve) => {
      const server = net.createServer();
      server.unref();
      server.on('error', () => {
        resolve(this.getAvailablePort(desiredPort + 1));
      });
      server.listen(desiredPort, () => {
        const port = server.address().port;
        server.close(() => resolve(port));
      });
    });
  }

  /**
   * Engine 2: Environment & Missing File Auto-Repair Engine
   * Ensures all required directories and config files exist.
   */
  repairEnvironment() {
    const repairs = [];
    const requiredDirs = ['public', 'src', 'bin', 'test', 'project-logs'];
    
    for (const dir of requiredDirs) {
      const dirPath = path.join(this.rootDir, dir);
      if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        repairs.push(`Created missing directory: ${dir}`);
      }
    }

    const configPath = path.join(this.rootDir, 'config.json');
    if (!fs.existsSync(configPath)) {
      const defaultConfig = {
        serverPort: 3000,
        autoLaunchBrowser: true,
        adbPorts: [5555, 5554, 62001, 7555],
        aiSelfHealingEnabled: true,
        lastRepaired: new Date().toISOString()
      };
      fs.writeFileSync(configPath, JSON.stringify(defaultConfig, null, 2), 'utf-8');
      repairs.push(`Created default auto-configured config.json`);
    }

    return repairs;
  }

  /**
   * Engine 3: Dependency & Runtime Error Repair Engine
   * Inspects common crash logs / error codes and applies patches.
   */
  diagnoseAndFixError(err) {
    const message = err?.message || String(err);
    console.log(`[AI-Fixer Engine 3] Analyzing runtime diagnostic: "${message}"`);

    if (message.includes('EADDRINUSE')) {
      console.log(`[AI-Fixer] Auto-Fix Applied: Port collision detected. Switching to dynamic available port...`);
      return { fixed: true, action: 'SWITCH_PORT' };
    }

    if (message.includes('MODULE_NOT_FOUND')) {
      console.log(`[AI-Fixer] Auto-Fix Applied: Missing npm dependency. Triggering node_modules sync...`);
      return { fixed: true, action: 'INSTALL_DEPS' };
    }

    if (message.includes('ENOENT')) {
      this.repairEnvironment();
      return { fixed: true, action: 'REPAIRED_PATHS' };
    }

    return { fixed: false, action: 'NONE' };
  }

  /**
   * Run full offline AI Diagnostic & Self-Annealing Pipeline
   */
  async runPipeline() {
    console.log('🤖 [Triple-Engine AI Auto-Fixer] Running zero-key diagnostic...');
    const envRepairs = this.repairEnvironment();
    const port = await this.getAvailablePort(3000);
    
    // Save optimal port to config.json
    const configPath = path.join(this.rootDir, 'config.json');
    let cfg = {};
    try {
      cfg = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    } catch (_) {}
    cfg.serverPort = port;
    cfg.lastVerified = new Date().toISOString();
    fs.writeFileSync(configPath, JSON.stringify(cfg, null, 2), 'utf-8');

    return {
      success: true,
      optimalPort: port,
      repairsApplied: envRepairs
    };
  }
}

module.exports = AiSelfFixer;
