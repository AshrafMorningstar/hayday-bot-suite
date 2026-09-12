const fs = require('fs');
const path = require('path');

const MANIFEST_FILENAME = '.repoforge-manifest.json';

class FolderArranger {
  /**
   * Generates a preview plan for organizing projects.
   * @param {Array<object>} projects 
   * @param {string} destinationDir 
   * @param {'activity'|'frequency'|'date'|'year'|'fame'|'language'|'status'} mode 
   * @param {'junction'|'copy'|'move'} type 
   */
  static plan(projects, destinationDir, mode = 'activity', type = 'junction') {
    const dest = path.resolve(destinationDir);
    const planItems = [];

    for (const p of projects) {
      const category = this.determineCategory(p, mode);
      const sanitizedCategory = category.replace(/[<>:"/\\|?*]/g, '_');
      const sanitizedName = p.name.replace(/[<>:"/\\|?*]/g, '_');
      const categoryDir = path.join(dest, sanitizedCategory);
      const targetPath = path.join(categoryDir, sanitizedName);

      const isInsideDest = p.path.toLowerCase().startsWith(dest.toLowerCase());

      planItems.push({
        id: p.id || p.path,
        name: p.name,
        source: p.path,
        category: sanitizedCategory,
        target: targetPath,
        categoryDir,
        type,
        canExecute: !isInsideDest && p.path.toLowerCase() !== targetPath.toLowerCase(),
        reason: isInsideDest ? 'Source is already inside destination' : 'Ready'
      });
    }

    return {
      destinationDir: dest,
      mode,
      type,
      totalCount: planItems.length,
      executableCount: planItems.filter(i => i.canExecute).length,
      items: planItems
    };
  }

  // Alias for backward-compatibility
  static generatePlan(projects, destinationDir, mode = 'activity', type = 'junction') {
    return this.plan(projects, destinationDir, mode, type);
  }

  /**
   * Determines the category label for a project.
   */
  static determineCategory(project, mode) {
    const daysSince = project.fame?.daysSinceActive ?? 0;
    const lastActive = project.timestamps?.lastActive ? new Date(project.timestamps.lastActive) : new Date();

    switch (mode) {
      case 'activity':
      case 'frequency':
        if (daysSince <= 14) return '01_Active (Last 2 Weeks)';
        if (daysSince <= 60) return '02_Recent (Last 2 Months)';
        if (daysSince <= 365) return '03_Dormant (This Year)';
        return '04_Ancient Relics (> 1 Year)';

      case 'date':
      case 'year': {
        const year = lastActive.getFullYear();
        const currentYear = new Date().getFullYear();
        if (isNaN(year)) return 'Undated';
        if (year === currentYear) return `${year}_Current Year`;
        if (year === currentYear - 1) return `${year}_Last Year`;
        return `${year}_Archive`;
      }

      case 'fame':
      case 'popularity': {
        const tier = project.fame?.tier?.id;
        if (tier === 'diamond') return '01_Diamond Masterpieces';
        if (tier === 'rising') return '02_Rising Stars';
        if (tier === 'relic') return '03_Ancient Relics';
        return '04_Fresh Sprouts';
      }

      case 'language': {
        const lang = project.primaryLanguage || 'Unknown';
        return lang.replace(/[\\/:*?"<>|]/g, '_');
      }

      case 'status':
        if (project.git?.isUnreleased) return '01_Unreleased (Local Only)';
        if (project.git?.isDirty) return '02_Work In Progress (Uncommitted)';
        return '03_Published Repositories';

      default:
        return 'General';
    }
  }

  /**
   * Executes organization of projects and records an undo manifest.
   */
  static execute(projects, destinationDir, mode = 'activity', type = 'junction') {
    const plan = this.plan(projects, destinationDir, mode, type);
    const dest = plan.destinationDir;

    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }

    const executedOperations = [];
    const errors = [];
    const skipped = [];

    for (const item of plan.items) {
      if (!item.canExecute) {
        skipped.push({ name: item.name, reason: item.reason });
        continue;
      }

      // Ensure category directory exists
      if (!fs.existsSync(item.categoryDir)) {
        try {
          fs.mkdirSync(item.categoryDir, { recursive: true });
        } catch (e) {
          errors.push({ name: item.name, error: `Failed to create category directory: ${e.message}` });
          continue;
        }
      }

      // Destination collision handling
      if (fs.existsSync(item.target)) {
        try {
          const stat = fs.lstatSync(item.target);
          if (stat.isSymbolicLink() || (process.platform === 'win32' && stat.isDirectory())) {
            try {
              fs.unlinkSync(item.target);
            } catch (_) {}
          }
        } catch (_) {}
      }

      try {
        if (type === 'junction') {
          if (fs.existsSync(item.target)) {
            skipped.push({ name: item.name, reason: 'Destination already exists' });
            continue;
          }
          if (process.platform === 'win32') {
            fs.symlinkSync(item.source, item.target, 'junction');
          } else {
            fs.symlinkSync(item.source, item.target, 'dir');
          }
          executedOperations.push({
            name: item.name,
            source: item.source,
            target: item.target,
            category: item.category,
            type: 'junction'
          });
        } else if (type === 'copy') {
          fs.cpSync(item.source, item.target, { recursive: true });
          executedOperations.push({
            name: item.name,
            source: item.source,
            target: item.target,
            category: item.category,
            type: 'copy'
          });
        } else if (type === 'move') {
          try {
            fs.renameSync(item.source, item.target);
          } catch (renameErr) {
            fs.cpSync(item.source, item.target, { recursive: true });
            fs.rmSync(item.source, { recursive: true, force: true });
          }
          executedOperations.push({
            name: item.name,
            source: item.source,
            target: item.target,
            category: item.category,
            type: 'move'
          });
        }
      } catch (err) {
        errors.push({
          name: item.name,
          source: item.source,
          target: item.target,
          error: err.message
        });
      }
    }

    // Save Undo Manifest in the target directory
    const manifest = {
      timestamp: new Date().toISOString(),
      destinationDir: dest,
      mode,
      type,
      operations: executedOperations
    };

    try {
      fs.writeFileSync(path.join(dest, MANIFEST_FILENAME), JSON.stringify(manifest, null, 2), 'utf8');
    } catch (_) {}

    return {
      success: executedOperations.length > 0 || plan.items.length === 0,
      destinationDir: dest,
      mode,
      type,
      total: plan.items.length,
      executedCount: executedOperations.length,
      errorCount: errors.length,
      skippedCount: skipped.length,
      operations: executedOperations,
      errors,
      skipped
    };
  }

  // Alias for backward compatibility
  static executePlan(plan) {
    return this.execute(plan.items.map(i => ({
      name: i.name,
      path: i.sourcePath || i.source,
      fame: { daysSinceActive: 0 }
    })), plan.targetDir || plan.destinationDir, plan.criterion || plan.mode, plan.mode || plan.type);
  }

  /**
   * Checks if an undo manifest exists in the specified destination directory.
   */
  static hasManifest(destinationDir) {
    if (!destinationDir) return false;
    const manifestPath = path.join(path.resolve(destinationDir), MANIFEST_FILENAME);
    return fs.existsSync(manifestPath);
  }

  /**
   * Undoes the last organization by reversing operations from the manifest.
   */
  static undo(destinationDir) {
    const dest = path.resolve(destinationDir);
    const manifestPath = path.join(dest, MANIFEST_FILENAME);

    if (!fs.existsSync(manifestPath)) {
      return { success: false, error: `No undo manifest found at: ${manifestPath}` };
    }

    let manifest;
    try {
      manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    } catch (e) {
      return { success: false, error: `Corrupt manifest file: ${e.message}` };
    }

    const reversed = [];
    const errors = [];

    for (const op of (manifest.operations || [])) {
      try {
        if (op.type === 'junction') {
          if (fs.existsSync(op.target)) {
            try {
              fs.unlinkSync(op.target);
            } catch (_) {
              fs.rmSync(op.target, { recursive: true, force: true });
            }
            reversed.push({ name: op.name, action: 'Removed junction', target: op.target });
          }
        } else if (op.type === 'copy') {
          if (fs.existsSync(op.target)) {
            fs.rmSync(op.target, { recursive: true, force: true });
            reversed.push({ name: op.name, action: 'Removed copied directory', target: op.target });
          }
        } else if (op.type === 'move') {
          // Move back to original source
          if (fs.existsSync(op.target)) {
            // Ensure original parent dir exists
            const origParent = path.dirname(op.source);
            if (!fs.existsSync(origParent)) {
              fs.mkdirSync(origParent, { recursive: true });
            }
            try {
              fs.renameSync(op.target, op.source);
            } catch (_) {
              fs.cpSync(op.target, op.source, { recursive: true });
              fs.rmSync(op.target, { recursive: true, force: true });
            }
            reversed.push({ name: op.name, action: 'Restored to original location', source: op.source });
          }
        }
      } catch (err) {
        errors.push({ name: op.name, error: err.message });
      }
    }

    // Clean up empty category directories inside dest
    try {
      const entries = fs.readdirSync(dest, { withFileTypes: true });
      for (const e of entries) {
        if (e.isDirectory()) {
          const subDirPath = path.join(dest, e.name);
          const contents = fs.readdirSync(subDirPath);
          if (contents.length === 0) {
            fs.rmdirSync(subDirPath);
          }
        }
      }
    } catch (_) {}

    // Delete manifest
    try {
      fs.unlinkSync(manifestPath);
    } catch (_) {}

    return {
      success: true,
      destinationDir: dest,
      reversedCount: reversed.length,
      errorCount: errors.length,
      reversed,
      errors
    };
  }
}

module.exports = FolderArranger;
