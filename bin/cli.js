#!/usr/bin/env node

import path from 'path';
import { fileURLToPath } from 'url';
import { install, triggerLiveReload, getInstalledVersion } from '../scripts/install-plugin.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);
const command = args[0];

async function main() {
  console.log('\n🌌 Antigravity RTL & Persian Typography (v2.0.0)');
  console.log('──────────────────────────────────────────────────');

  if (!command || command === 'install' || command === 'update') {
    const installed = getInstalledVersion();
    if (!installed) {
      console.log('📦 Installing Antigravity RTL plugin...');
      await install();
      console.log('\n✅ Antigravity RTL installed successfully!');
      console.log('💡 Open Google Antigravity to enjoy native RTL and Persian fonts.\n');
    } else {
      console.log(`⚡ Syncing & refreshing Antigravity RTL plugin (v${installed})...`);
      await install({ silent: true });
      const reloaded = await triggerLiveReload();
      if (reloaded) {
        console.log('✨ Live hot-reload applied to active Antigravity window.');
      }
      console.log('🚀 Ready and active!\n');
    }
    return;
  }

  if (command === 'uninstall') {
    await import('../scripts/uninstall-plugin.js');
    return;
  }

  if (command === 'status') {
    const ver = getInstalledVersion();
    console.log(`Plugin Status: ${ver ? `🟢 Installed (v${ver})` : '⚪ Not Installed'}`);
    console.log('──────────────────────────────────────────────────\n');
    return;
  }

  console.log(`Unknown command: ${command}`);
  console.log('Usage: npx antigravity-rtl [install|uninstall|status]');
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
