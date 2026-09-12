#!/usr/bin/env python3
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SECRETS_PATTERNS = [
    r'password\s*=\s*[\'"][^\'"]+[\'"]',
    r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
    r'secret\s*=\s*[\'"][^\'"]+[\'"]',
    r'-----BEGIN\s+PRIVATE\s+KEY-----',
    r'-----BEGIN\s+RSA\s+PRIVATE\s+KEY-----'
]

compiled = [re.compile(p, re.IGNORECASE) for p in SECRETS_PATTERNS]

def audit():
    leaks = []
    skip = {'.git', 'node_modules', '__pycache__', 'waste', 'Not Working'}
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in files:
            if f.endswith(('.py', '.json', '.yaml', '.txt', '.js', '.md')):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as file_obj:
                        for idx, line in enumerate(file_obj, 1):
                            for pattern in compiled:
                                if pattern.search(line):
                                    leaks.append((os.path.relpath(fp, BASE_DIR), idx, line.strip()))
                except Exception:
                    pass
    return leaks

if __name__ == '__main__':
    findings = audit()
    print(f"Privacy Guard Audit Completed: Found {len(findings)} issues.")
    for f in findings:
        print(f"  ⚠️ {f[0]}:{f[1]} -> {f[2][:80]}")
