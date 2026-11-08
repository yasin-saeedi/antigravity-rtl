import fs from 'fs';
import path from 'path';
import os from 'os';
import http from 'http';

const PLUGIN_NAME = 'antigravity-rtl';
const PLUGINS_DIR = path.join(os.homedir(), '.gemini', 'config', 'plugins');
const TARGET_DIR = path.join(PLUGINS_DIR, PLUGIN_NAME);

export async function uninstall() {
  console.log(`🗑️ Uninstalling ${PLUGIN_NAME}...`);

  // 1. Remove DOM nodes from live window if active
  try {
    const portFile = path.join(process.env.APPDATA || '', 'Antigravity', 'DevToolsActivePort');
    if (fs.existsSync(portFile)) {
      const [portStr] = fs.readFileSync(portFile, 'utf8').trim().split('\n');
      const port = parseInt(portStr, 10);
      if (port) {
        const targets = await new Promise((resolve) => {
          http.get(`http://127.0.0.1:${port}/json`, (res) => {
            let d = '';
            res.on('data', c => d += c);
            res.on('end', () => {
              try { resolve(JSON.parse(d)); } catch { resolve([]); }
            });
          }).on('error', () => resolve([]));
        });

        const page = targets.find(t => t.type === 'page' && (t.url?.includes('127.0.0.1') || t.title?.includes('Antigravity') || t.url?.includes('workbench.html')));
        if (page && page.webSocketDebuggerUrl) {
          const ws = new globalThis.WebSocket(page.webSocketDebuggerUrl);
          await new Promise(r => ws.onopen = r);
          ws.send(JSON.stringify({
            id: 1,
            method: 'Runtime.evaluate',
            params: {
              expression: `(() => {
                const s = document.getElementById('antigravity-chat-rtl-style');
                if (s) s.remove();
                const m = document.getElementById('ag-appearance-modal');
                if (m) m.remove();
                const btn = document.getElementById('ag-appearance-menu-container');
                if (btn) btn.remove();
                document.body.classList.remove('ag-rtl-disabled');
                window.__AG_RTL_DISABLED__ = true;
              })()`
            }
          }));
          setTimeout(() => ws.close(), 500);
        }
      }
    }
  } catch {}

  // 2. Remove files
  if (fs.existsSync(TARGET_DIR)) {
    fs.rmSync(TARGET_DIR, { recursive: true, force: true });
    console.log(`✅ Removed ${TARGET_DIR}`);
  } else {
    console.log(`ℹ️ ${PLUGIN_NAME} was not installed.`);
  }

  console.log(`🎉 ${PLUGIN_NAME} has been completely uninstalled.`);
}

uninstall().catch(err => {
  console.error('Uninstall error:', err);
  process.exit(1);
});
