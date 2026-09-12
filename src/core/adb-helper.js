const { execSync } = require('child_process');
const net = require('net');

class AdbHelper {
  static EMULATOR_PORTS = [
    { name: 'LDPlayer / Generic ADB', port: 5555 },
    { name: 'BlueStacks 5 (Instance 1)', port: 5554 },
    { name: 'BlueStacks 5 (Instance 2)', port: 5556 },
    { name: 'Nox App Player', port: 62001 },
    { name: 'MEmu App Player', port: 21503 },
    { name: 'MuMu Player', port: 7555 }
  ];

  /**
   * Scans system for connected ADB devices via `adb devices` or port checks
   */
  static async getDevices() {
    const devices = [];

    // 1. Try native ADB command if adb is installed in PATH or local bot folder
    try {
      const output = execSync('adb devices', { stdio: ['pipe', 'pipe', 'ignore'], timeout: 1500 }).toString().trim();
      const lines = output.split(/\r?\n/).slice(1);
      for (const line of lines) {
        const parts = line.split(/\s+/);
        if (parts.length >= 2 && parts[1] === 'device') {
          devices.push({
            id: parts[0],
            name: parts[0].includes('127.0.0.1') ? `Emulator (${parts[0]})` : `Device (${parts[0]})`,
            status: 'online',
            type: parts[0].includes('127.0.0.1') ? 'emulator' : 'physical'
          });
        }
      }
    } catch (_) {}

    // 2. Scan standard emulator TCP ports if no ADB devices returned
    if (devices.length === 0) {
      for (const emu of this.EMULATOR_PORTS) {
        const isOpen = await this.checkPort('127.0.0.1', emu.port);
        if (isOpen) {
          devices.push({
            id: `127.0.0.1:${emu.port}`,
            name: `${emu.name} (Port ${emu.port})`,
            status: 'online',
            type: 'emulator'
          });
        }
      }
    }

    return devices;
  }

  static checkPort(host, port, timeout = 300) {
    return new Promise((resolve) => {
      const socket = new net.Socket();
      socket.setTimeout(timeout);

      socket.on('connect', () => {
        socket.destroy();
        resolve(true);
      });

      socket.on('timeout', () => {
        socket.destroy();
        resolve(false);
      });

      socket.on('error', () => {
        socket.destroy();
        resolve(false);
      });

      socket.connect(port, host);
    });
  }
}

module.exports = AdbHelper;
