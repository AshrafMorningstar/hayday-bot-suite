const fs = require('fs');
const path = require('path');
const { exec, execSync } = require('child_process');

class BotManager {
  /**
   * Catalog of known bot engine signatures
   */
  static BOT_SIGNATURES = [
    {
      id: 'hay-star-exe',
      name: 'HayStar Bot Engine (Executable)',
      relPath: 'Working FIne/hay-star/hay-star.exe',
      type: 'executable',
      runCmd: 'hay-star.exe',
      description: 'High-speed compiled Rust/C++ native HayStar automation engine.',
      icon: '⭐'
    },
    {
      id: 'hay-star-supervisor',
      name: 'HayStar Frida Supervisor',
      relPath: 'Working FIne/hay-star/supervisor.py',
      type: 'python',
      runCmd: 'python supervisor.py',
      description: 'Python Frida bridge supervisor & game process guard.',
      icon: '🛡️'
    },
    {
      id: 'hay-star-frida',
      name: 'HayStar Frida Bridge',
      relPath: 'Working FIne/hay-star/frida_bridge.py',
      type: 'python',
      runCmd: 'python frida_bridge.py',
      description: 'Frida memory probe & network packet analyzer.',
      icon: '🔗'
    },
    {
      id: 'hdx-bot-exe',
      name: 'HDX Bot Engine (HDXC)',
      relPath: 'Working FIne/hdx bot/hdxc.exe',
      type: 'executable',
      runCmd: 'hdxc.exe',
      description: 'HDX Multi-account farm management executable.',
      icon: '🚜'
    },
    {
      id: 'inxernal-loader',
      name: 'Inxernal Framework Loader',
      relPath: 'Working FIne/inxernal-main/loader.py',
      type: 'python',
      runCmd: 'python loader.py',
      description: 'Inxernal account access finder & offset loader.',
      icon: '🔑'
    },
    {
      id: 'hay-star-working',
      name: 'HayStar Engine (Working Backup)',
      relPath: 'Working/hay-star-main/supervisor.py',
      type: 'python',
      runCmd: 'python supervisor.py',
      description: 'Backup HayStar supervisor engine.',
      icon: '📦'
    }
  ];

  /**
   * Scans rootDir to locate installed bot engines and inspect their existence
   */
  static scanBots(rootDir = process.cwd()) {
    const resolvedRoot = path.resolve(rootDir);
    const discovered = [];

    for (const sig of this.BOT_SIGNATURES) {
      const fullPath = path.join(resolvedRoot, sig.relPath);
      const exists = fs.existsSync(fullPath);
      const dirPath = path.dirname(fullPath);

      discovered.push({
        ...sig,
        fullPath,
        dirPath,
        status: exists ? 'ready' : 'missing',
        lastModified: exists ? fs.statSync(fullPath).mtime.toISOString() : null
      });
    }

    // Also scan recursively for any other .exe or .py bot scripts in Working directories
    try {
      const workingDirs = ['Working', 'Working FIne', 'Edit Game Files'];
      for (const wDir of workingDirs) {
        const target = path.join(resolvedRoot, wDir);
        if (fs.existsSync(target)) {
          const files = fs.readdirSync(target, { recursive: true });
          for (const f of files) {
            const ext = path.extname(f).toLowerCase();
            const normF = f.replace(/\\/g, '/');
            const baseF = path.basename(f);
            const isIgnored = normF.includes('target/') || normF.includes('node_modules/') || normF.includes('.cargo/') || normF.includes('adb.exe') || normF.includes('build-script-build') || normF.includes('/tests/') || baseF.startsWith('test_') || baseF.startsWith('scan_') || baseF.startsWith('trace_') || baseF.startsWith('dump_') || baseF.startsWith('parse_');
            if (!isIgnored && (ext === '.exe' || f.endsWith('_bot.py') || f.endsWith('_main.py') || f.endsWith('loader.py') || f.endsWith('supervisor.py') || f.endsWith('frida_bridge.py')) && !discovered.some(d => d.fullPath.endsWith(f))) {
              const fullP = path.join(target, f);
              const dirP = path.dirname(fullP);
              discovered.push({
                id: `bot-custom-${path.basename(f, ext)}`,
                name: `Custom Bot (${path.basename(f)})`,
                relPath: path.relative(resolvedRoot, fullP),
                fullPath: fullP,
                dirPath: dirP,
                type: ext === '.exe' ? 'executable' : 'python',
                runCmd: ext === '.exe' ? path.basename(f) : `python "${path.basename(f)}"`,
                description: `Custom detected bot script in ${wDir}`,
                icon: '🤖',
                status: 'ready',
                lastModified: fs.statSync(fullP).mtime.toISOString()
              });
            }
          }
        }
      }
    } catch (_) {}

    return discovered;
  }

  /**
   * Launches target bot in an interactive Windows command window
   */
  static launchBot(botId, rootDir = process.cwd()) {
    const bots = this.scanBots(rootDir);
    const bot = bots.find(b => b.id === botId || b.relPath.includes(botId));

    if (!bot) {
      throw new Error(`Bot engine not found: ${botId}`);
    }

    if (bot.status !== 'ready' || !fs.existsSync(bot.fullPath)) {
      throw new Error(`Bot executable is missing at: ${bot.fullPath}`);
    }

    const dir = bot.dirPath;
    const cmd = bot.runCmd;

    if (process.platform === 'win32') {
      exec(`start cmd.exe /k "cd /d "${dir}" && title ${bot.name} && ${cmd}"`);
    } else {
      exec(`cd "${dir}" && ${cmd} &`);
    }

    return {
      success: true,
      bot,
      message: `Launched ${bot.name} in interactive terminal window.`
    };
  }
}

module.exports = BotManager;
