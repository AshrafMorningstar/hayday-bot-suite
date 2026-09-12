const fs = require('fs');
const path = require('path');

class VirtualViews {
  /**
   * Generates a virtual hierarchy of projects organized by categories.
   * @param {Array<object>} projects 
   * @param {'frequency'|'activity'|'date'|'language'|'fame'|'popularity'|'unreleased'} mode 
   */
  static generateHierarchy(projects, mode = 'activity') {
    const tree = {};

    for (const p of projects) {
      let category = 'General';

      if (mode === 'language') {
        category = p.primaryLanguage || 'Unknown';
      } else if (mode === 'activity' || mode === 'frequency') {
        const days = p.fame?.daysSinceActive !== undefined ? p.fame.daysSinceActive : 0;
        if (days <= 14) category = '01_Active (Last 2 Weeks)';
        else if (days <= 60) category = '02_Recent (Last 2 Months)';
        else if (days <= 365) category = '03_Dormant (This Year)';
        else category = '04_Ancient Relics (> 1 Year)';
      } else if (mode === 'date') {
        const dateObj = new Date(p.timestamps?.lastActive || Date.now());
        const year = dateObj.getFullYear() ? dateObj.getFullYear() : 'Undated';
        const month = String(dateObj.getMonth() + 1).padStart(2, '0');
        category = `${year}-${month}`;
      } else if (mode === 'fame' || mode === 'tier') {
        const tierId = p.fame?.tier?.id || 'sprout';
        if (tierId === 'diamond') category = '01_Diamond Masterpieces 💎';
        else if (tierId === 'rising') category = '02_Rising Stars 🚀';
        else if (tierId === 'workhorse') category = '03_Steady Engines ⚙️';
        else if (tierId === 'relic') category = '04_Ancient Relics 🏺';
        else category = '05_Fresh Sprouts 🌱';
      } else if (mode === 'popularity') {
        const stars = p.fame?.stars || p.git?.stars || 0;
        if (stars >= 50) category = '01_Viral (> 50 Stars)';
        else if (stars >= 10) category = '02_Popular (10-49 Stars)';
        else if (stars >= 1) category = '03_Growing (1-9 Stars)';
        else category = '04_Unstarred (Local)';
      } else if (mode === 'unreleased' || mode === 'status') {
        category = p.git?.isUnreleased ? '01_Local & Unreleased' : '02_Published Repositories';
      }

      if (!tree[category]) tree[category] = [];
      tree[category].push({
        id: p.id,
        name: p.name,
        path: p.path,
        primaryLanguage: p.primaryLanguage,
        fameScore: p.fame?.fameScore || 0,
        tier: p.fame?.tier?.label || 'Sprout',
        lastActive: p.timestamps?.lastActive,
        isUnreleased: p.git?.isUnreleased,
        description: p.description
      });
    }

    return tree;
  }

  /**
   * Creates a directory of symlinks / Windows junctions pointing to original projects.
   * Completely safe, non-destructive, zero disk space.
   * @param {Array<object>} projects 
   * @param {string} destinationDir 
   * @param {'frequency'|'activity'|'date'|'language'|'fame'|'popularity'|'unreleased'} mode 
   */
  static createVirtualJunctions(projects, destinationDir, mode = 'activity') {
    const hierarchy = this.generateHierarchy(projects, mode);
    const dest = path.resolve(destinationDir);

    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }

    const report = {
      target: dest,
      mode,
      type: 'virtual_junction',
      createdJunctions: [],
      errors: []
    };

    const manifest = {
      timestamp: new Date().toISOString(),
      type: 'virtual',
      mode,
      entries: []
    };

    for (const [category, items] of Object.entries(hierarchy)) {
      const sanitizedCategory = category.replace(/[<>:"/\\|?*]/g, '_');
      const catDir = path.join(dest, sanitizedCategory);
      if (!fs.existsSync(catDir)) {
        fs.mkdirSync(catDir, { recursive: true });
      }

      for (const item of items) {
        const sanitizedName = item.name.replace(/[<>:"/\\|?*]/g, '_');
        const linkPath = path.join(catDir, sanitizedName);

        if (fs.existsSync(linkPath)) {
          continue; // skip existing
        }

        try {
          if (process.platform === 'win32') {
            fs.symlinkSync(item.path, linkPath, 'junction');
          } else {
            fs.symlinkSync(item.path, linkPath, 'dir');
          }
          report.createdJunctions.push({ name: item.name, linkPath, original: item.path, category });
          manifest.entries.push({ name: item.name, linkPath, original: item.path });
        } catch (err) {
          report.errors.push({ name: item.name, error: err.message });
        }
      }
    }

    // Save manifest for safe tracking & undo
    try {
      fs.writeFileSync(path.join(dest, '.repoforge_manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
    } catch (_) {}

    return report;
  }

  /**
   * Real Physical Organization: copies or moves project directories into categorized hierarchy.
   * Maintains full undo manifest so changes can be reverted instantly.
   */
  static createPhysicalOrganization(projects, destinationDir, mode = 'activity', action = 'copy') {
    const hierarchy = this.generateHierarchy(projects, mode);
    const dest = path.resolve(destinationDir);

    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }

    const report = {
      target: dest,
      mode,
      action,
      type: 'physical',
      processed: [],
      errors: []
    };

    const manifest = {
      timestamp: new Date().toISOString(),
      type: 'physical',
      action,
      mode,
      entries: []
    };

    for (const [category, items] of Object.entries(hierarchy)) {
      const sanitizedCategory = category.replace(/[<>:"/\\|?*]/g, '_');
      const catDir = path.join(dest, sanitizedCategory);
      if (!fs.existsSync(catDir)) {
        fs.mkdirSync(catDir, { recursive: true });
      }

      for (const item of items) {
        const sanitizedName = item.name.replace(/[<>:"/\\|?*]/g, '_');
        const targetPath = path.join(catDir, sanitizedName);

        if (fs.existsSync(targetPath)) {
          report.errors.push({ name: item.name, error: `Target already exists: ${targetPath}` });
          continue;
        }

        try {
          if (action === 'move') {
            fs.renameSync(item.path, targetPath);
            report.processed.push({ name: item.name, from: item.path, to: targetPath, category });
            manifest.entries.push({ name: item.name, original: item.path, destination: targetPath, action: 'moved' });
          } else {
            // copy recursively
            fs.cpSync(item.path, targetPath, { recursive: true });
            report.processed.push({ name: item.name, from: item.path, to: targetPath, category });
            manifest.entries.push({ name: item.name, original: item.path, destination: targetPath, action: 'copied' });
          }
        } catch (err) {
          report.errors.push({ name: item.name, error: err.message });
        }
      }
    }

    try {
      fs.writeFileSync(path.join(dest, '.repoforge_manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
    } catch (_) {}

    return report;
  }

  /**
   * Unified organization entrypoint.
   */
  static organize(projects, destinationDir, options = {}) {
    const { mode = 'activity', virtual = true, action = 'copy' } = options;
    if (virtual) {
      return this.createVirtualJunctions(projects, destinationDir, mode);
    } else {
      return this.createPhysicalOrganization(projects, destinationDir, mode, action);
    }
  }

  /**
   * Reverts / undoes an organization operation using the manifest file.
   */
  static undoOrganization(destinationDir) {
    const dest = path.resolve(destinationDir);
    const manifestPath = path.join(dest, '.repoforge_manifest.json');

    if (!fs.existsSync(manifestPath)) {
      return { success: false, error: 'No .repoforge_manifest.json found in destination directory' };
    }

    let manifest;
    try {
      manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    } catch (err) {
      return { success: false, error: `Corrupted manifest: ${err.message}` };
    }

    const report = {
      reverted: [],
      errors: []
    };

    for (const entry of (manifest.entries || [])) {
      try {
        if (manifest.type === 'virtual') {
          if (fs.existsSync(entry.linkPath)) {
            try {
              fs.rmSync(entry.linkPath, { recursive: true, force: true });
            } catch (_) {
              try {
                fs.rmdirSync(entry.linkPath);
              } catch (_) {
                fs.unlinkSync(entry.linkPath);
              }
            }
            report.reverted.push(entry.linkPath);
          }
        } else if (manifest.type === 'physical') {
          if (entry.action === 'moved') {
            if (fs.existsSync(entry.destination)) {
              fs.renameSync(entry.destination, entry.original);
              report.reverted.push(`${entry.destination} -> ${entry.original}`);
            }
          } else if (entry.action === 'copied') {
            if (fs.existsSync(entry.destination)) {
              fs.rmSync(entry.destination, { recursive: true, force: true });
              report.reverted.push(`Removed copied ${entry.destination}`);
            }
          }
        }
      } catch (err) {
        report.errors.push({ entry, error: err.message });
      }
    }

    // Clean up empty directories
    try {
      const subdirs = fs.readdirSync(dest, { withFileTypes: true }).filter(d => d.isDirectory());
      for (const sd of subdirs) {
        const full = path.join(dest, sd.name);
        try {
          const files = fs.readdirSync(full);
          if (files.length === 0) fs.rmdirSync(full);
        } catch (_) {}
      }
    } catch (_) {}

    return { success: true, report };
  }
}

module.exports = VirtualViews;
