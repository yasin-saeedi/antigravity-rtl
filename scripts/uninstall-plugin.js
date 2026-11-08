import fs from 'fs';
import path from 'path';
import os from 'os';
import http from 'http';
import { execSync } from 'child_process';

const PLUGIN_NAME = 'antigravity-rtl';
const PLUGINS_DIR = path.join(os.homedir(), '.gemini', 'config', 'plugins');
const TARGET_DIR = path.join(PLUGINS_DIR, PLUGIN_NAME);

export async function uninstall() {
  console.log(`🗑️ Uninstalling ${PLUGIN_NAME}...`);

  // 1. Remove DOM nodes from live window if active
  try {
    const portFile = path.join(process.env.APPDATA || '', 'Antigravity', 'DevToolsActivePort');
    if (fs.existsSync(portFile)) {
      const port = parseInt(fs.readFileSync(portFile, 'utf8').trim().split('\n')[0], 10);
      const res = await fetch(`http://127.0.0.1:${port}/json`).then(r => r.json()).catch(() => null);
      const target = res?.find(t => t.type === 'page' && (t.url?.includes('127.0.0.1') || t.title?.includes('Antigravity') || t.url?.includes('workbench.html')));
      if (target?.webSocketDebuggerUrl) {
        const ws = new WebSocket(target.webSocketDebuggerUrl);
        await new Promise((resolve) => {
          ws.onopen = resolve;
          ws.onerror = resolve;
          setTimeout(resolve, 1500);
        });
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({
            id: 999,
            method: 'Runtime.evaluate',
            params: {
              expression: `(() => {
                document.getElementById('antigravity-chat-rtl-style')?.remove();
                document.getElementById('ag-appearance-menu-container')?.remove();
                document.querySelectorAll('[dir="rtl"]').forEach(el => el.removeAttribute('dir'));
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
    try {
      fs.rmSync(TARGET_DIR, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
    } catch {
      if (process.platform === 'win32') {
        try {
          execSync(`powershell -NoProfile -Command "Remove-Item -Path '${TARGET_DIR}' -Recurse -Force"`, { stdio: 'ignore' });
        } catch {}
      }
    }
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
