const fs = require('fs');
const path = require('path');

const SECRET_PATTERNS = [
  { name: 'Private Key', regex: /-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----/ },
  { name: 'GitHub Personal Access Token', regex: /gh[pousr]_[A-Za-z0-9_]{36,255}/ },
  { name: 'GitLab Personal Access Token', regex: /glpat-[0-9a-zA-Z\-_]{20,}/ },
  { name: 'AWS Access Key ID', regex: /(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}/ },
  { name: 'AWS Secret Access Key', regex: /(?:aws_secret_access_key|aws_access_key_id)\s*=\s*['"]?[A-Za-z0-9\/+=]{40}['"]?/i },
  { name: 'Slack Token', regex: /xox[baprs]-[0-9a-zA-Z]{10,48}/ },
  { name: 'Stripe API Key', regex: /(?:sk|rk)_(?:live|test)_[0-9a-zA-Z]{24,}/ },
  { name: 'Generic Password Assignment', regex: /(?:password|passwd|pwd|secret|api_key|apikey)\s*[:=]\s*['"][^'"]{6,}['"]/i },
  { name: 'Database Connection String', regex: /(?:mongodb(?:\+srv)?|postgres(?:ql)?|mysql):\/\/[^:\s]+:[^@\s]+@[^/\s]+\/[^\s]+/i }
];

const SENSITIVE_FILENAMES = new Set([
  '.env', '.env.local', '.env.development', '.env.production', '.env.test',
  'id_rsa', 'id_ed25519', 'id_dsa', 'id_ecdsa',
  'credentials.json', 'client_secrets.json', '.npmrc', '.pypirc'
]);

const SKIP_EXTENSIONS = new Set([
  '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico',
  '.pdf', '.zip', '.tar', '.gz', '.7z', '.exe', '.dll', '.so',
  '.dylib', '.bin', '.mp4', '.mp3', '.wav', '.lock', '.map'
]);

class PrivacyGuard {
  /**
   * Audits a project directory for potential sensitive secrets and credentials.
   * @param {string} projectDir 
   * @param {number} maxFiles 
   * @returns {object} { safe: boolean, findings: Array<object> }
   */
  static audit(projectDir, maxFiles = 200) {
    const findings = [];
    let filesScanned = 0;

    function walk(dir) {
      if (filesScanned >= maxFiles) return;

      let entries;
      try {
        entries = fs.readdirSync(dir, { withFileTypes: true });
      } catch (_) {
        return;
      }

      for (const entry of entries) {
        if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === 'dist' || entry.name === 'build' || entry.name === 'test' || entry.name === 'tests') {
          continue;
        }

        const fullPath = path.join(dir, entry.name);
        const relPath = path.relative(projectDir, fullPath);

        if (entry.isDirectory()) {
          walk(fullPath);
        } else if (entry.isFile()) {
          filesScanned++;

          // 1. Check sensitive filenames
          if (SENSITIVE_FILENAMES.has(entry.name.toLowerCase())) {
            findings.push({
              file: relPath,
              type: 'Sensitive File',
              rule: `File name matches restricted secret file: ${entry.name}`,
              severity: 'HIGH'
            });
          }

          // 2. Scan file contents
          const ext = path.extname(entry.name).toLowerCase();
          if (SKIP_EXTENSIONS.has(ext)) continue;

          try {
            const stat = fs.statSync(fullPath);
            if (stat.size > 1024 * 512) continue; // skip files > 512KB

            const content = fs.readFileSync(fullPath, 'utf8');
            const lines = content.split('\n');

            for (let i = 0; i < lines.length; i++) {
              const line = lines[i];
              for (const pattern of SECRET_PATTERNS) {
                if (pattern.regex.test(line)) {
                  findings.push({
                    file: relPath,
                    line: i + 1,
                    type: pattern.name,
                    rule: `Matched pattern: ${pattern.name}`,
                    snippet: line.trim().slice(0, 80),
                    severity: 'CRITICAL'
                  });
                  break; // only record one pattern match per line
                }
              }
            }
          } catch (_) {}
        }
      }
    }

    walk(projectDir);

    return {
      safe: findings.length === 0,
      totalFindings: findings.length,
      findings
    };
  }
}

module.exports = PrivacyGuard;
