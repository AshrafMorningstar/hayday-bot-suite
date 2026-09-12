const fs = require('fs');
const path = require('path');
const os = require('os');
const VirtualViews = require('./virtual-views');

class Arranger {
  static getManifestPath() {
    const configDir = path.join(os.homedir(), '.repoforge');
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }
    return path.join(configDir, 'rollback-manifest.json');
  }

  /**
   * Plans the reorganization without touching disk.
   * Returns a map of projects with their planned new destination paths.
   * @param {Array<object>} projects 
   * @param {string} destinationRoot 
   * @param {'activity'|'date'|'language'|'fame'|'status'} strategy 
   */
  static planOrganization(projects, destinationRoot, strategy = 'activity') {
    const dest = path.resolve(destinationRoot);
    const plan = [];

    for (const p of projects) {
      let category = 'Uncategorized';

      if (strategy === 'activity') {
        const days = p.fame?.daysSinceActive || 0;
        if (days <= 30) category = '01_Active_Projects';
        else if (days <= 90) category = '02_Recent_Projects';
        else if (days <= 365) category = '03_Dormant_Projects';
        else category = '04_Ancient_Relics';
      } else if (strategy === 'date') {
        const d = new Date(p.timestamps.lastActive);
        const year = d.getFullYear() || 2026;
        category = year >= 2024 ? `Year_${year}` : 'Archive_Pre_2024';
      } else if (strategy === 'language') {
        const lang = (p.primaryLanguage || 'General').replace(/[^a-zA-Z0-9_-]/g, '_');
        category = `Lang_${lang}`;
      } else if (strategy === 'fame') {
        const tier = p.fame?.tier?.id || 'sprout';
        if (tier === 'diamond') category = '01_Diamond_Masterpieces';
        else if (tier === 'rising') category = '02_Rising_Stars';
        else if (tier === 'relic') category = '03_Ancient_Relics';
        else if (tier === 'workhorse') category = '04_Steady_Engines';
        else category = '05_Fresh_Sprouts';
      } else if (strategy === 'status') {
        category = p.git.isUnreleased ? 'Unreleased_Local' : 'Published_Repositories';
      }

      const categoryPath = path.join(dest, category);
      const targetPath = path.join(categoryPath, path.basename(p.path));

      plan.push({
        id: p.id,
        name: p.name,
        originalPath: p.path,
        category,
        categoryPath,
        targetPath,
        isSame: path.resolve(p.path) === path.resolve(targetPath)
      });
    }

    return plan;
  }

  /**
   * Executes organization.
   * mode: 'move' (physical move) or 'junction' (virtual zero-copy)
   */
  static executeOrganization(projects, destinationRoot, strategy = 'activity', mode = 'junction') {
    const plan = this.planOrganization(projects, destinationRoot, strategy);
    const dest = path.resolve(destinationRoot);

    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }

    const executedMoves = [];
    const errors = [];

    for (const item of plan) {
      if (item.isSame) continue;

      // Avoid moving parent directory into child
      if (item.targetPath.startsWith(item.originalPath + path.sep)) {
        errors.push({ name: item.name, error: 'Cannot move directory into itself.' });
        continue;
      }

      try {
        if (!fs.existsSync(item.categoryPath)) {
          fs.mkdirSync(item.categoryPath, { recursive: true });
        }

        if (mode === 'move') {
          // Physical move
          if (fs.existsSync(item.targetPath)) {
            errors.push({ name: item.name, error: `Target already exists: ${item.targetPath}` });
            continue;
          }

          fs.renameSync(item.originalPath, item.targetPath);
          executedMoves.push({
            name: item.name,
            from: item.originalPath,
            to: item.targetPath,
            type: 'move'
          });
        } else {
          // Virtual Junction / Symlink
          if (fs.existsSync(item.targetPath)) {
            continue; // already linked
          }

          if (process.platform === 'win32') {
            fs.symlinkSync(item.originalPath, item.targetPath, 'junction');
          } else {
            fs.symlinkSync(item.originalPath, item.targetPath, 'dir');
          }

          executedMoves.push({
            name: item.name,
            from: item.originalPath,
            to: item.targetPath,
            type: 'junction'
          });
        }
      } catch (err) {
        errors.push({ name: item.name, error: err.message });
      }
    }

    // Save manifest for rollback
    if (executedMoves.length > 0) {
      const manifest = {
        timestamp: new Date().toISOString(),
        strategy,
        mode,
        destinationRoot: dest,
        moves: executedMoves
      };
      try {
        fs.writeFileSync(this.getManifestPath(), JSON.stringify(manifest, null, 2), 'utf8');
        fs.writeFileSync(path.join(dest, '.repoforge-manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
        fs.writeFileSync(path.join(dest, 'repoforge-manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
      } catch (_) {}
    }

    return {
      success: errors.length === 0,
      totalRequested: plan.length,
      executedCount: executedMoves.length,
      destinationRoot: dest,
      executedMoves,
      errors
    };
  }

  /**
   * Undoes the last organization by reversing physical moves or removing junctions.
   */
  static rollbackLastOrganization(targetDir = null) {
    let manifestFile = targetDir ? path.join(path.resolve(targetDir), '.repoforge-manifest.json') : null;
    if (targetDir && !fs.existsSync(manifestFile)) {
      manifestFile = path.join(path.resolve(targetDir), 'repoforge-manifest.json');
    }
    if (!manifestFile || !fs.existsSync(manifestFile)) {
      manifestFile = this.getManifestPath();
    }
    if (!fs.existsSync(manifestFile)) {
      return { success: false, message: 'No organization manifest found to rollback.' };
    }

    let manifest;
    try {
      manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
    } catch (e) {
      return { success: false, message: 'Corrupted rollback manifest.' };
    }

    const reversed = [];
    const errors = [];

    for (const m of (manifest.moves || [])) {
      try {
        if (m.type === 'move') {
          if (fs.existsSync(m.to)) {
            const originalDir = path.dirname(m.from);
            if (!fs.existsSync(originalDir)) {
              fs.mkdirSync(originalDir, { recursive: true });
            }
            fs.renameSync(m.to, m.from);
            reversed.push({ name: m.name, restoredTo: m.from });
          }
        } else if (m.type === 'junction') {
          if (fs.existsSync(m.to)) {
            try {
              fs.rmSync(m.to, { recursive: true, force: true });
            } catch (_) {
              try {
                fs.rmdirSync(m.to);
              } catch (_) {
                fs.unlinkSync(m.to);
              }
            }
            reversed.push({ name: m.name, removedJunction: m.to });
          }
        }
      } catch (err) {
        errors.push({ name: m.name, error: err.message });
      }
    }

    // Remove manifest after rollback
    try {
      fs.unlinkSync(manifestFile);
      if (manifest.destinationRoot) {
        const destManifest1 = path.join(manifest.destinationRoot, '.repoforge-manifest.json');
        const destManifest2 = path.join(manifest.destinationRoot, 'repoforge-manifest.json');
        if (fs.existsSync(destManifest1)) fs.unlinkSync(destManifest1);
        if (fs.existsSync(destManifest2)) fs.unlinkSync(destManifest2);
      }
    } catch (_) {}

    return {
      success: errors.length === 0,
      reversedCount: reversed.length,
      reversed,
      errors
    };
  }
}

module.exports = Arranger;
