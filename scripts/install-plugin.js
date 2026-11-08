import fs from 'fs';
import path from 'path';
import os from 'os';
import http from 'http';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
export const ROOT_DIR = path.resolve(__dirname, '..');

export const PLUGIN_NAME = 'antigravity-rtl';
export const PLUGINS_DIR = path.join(os.homedir(), '.gemini', 'config', 'plugins');
export const TARGET_DIR = path.join(PLUGINS_DIR, PLUGIN_NAME);

export function getInstalledVersion() {
  const pkgPath = path.join(TARGET_DIR, 'package.json');
  if (fs.existsSync(pkgPath)) {
    try {
      const data = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      return data.version || null;
    } catch {
      return null;
    }
  }
  return null;
}

export function copyDirRecursive(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === '.cache') continue;

    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      try {
        fs.copyFileSync(srcPath, destPath);
      } catch {}
    }
  }
}

export async function triggerLiveReload() {
  try {
    const portFile = path.join(process.env.APPDATA || '', 'Antigravity', 'DevToolsActivePort');
    if (!fs.existsSync(portFile)) return false;

    const [portStr] = fs.readFileSync(portFile, 'utf8').trim().split('\n');
    const port = parseInt(portStr, 10);
    if (!port) return false;

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
    if (!page || !page.webSocketDebuggerUrl) return false;

    const cssPath = path.join(TARGET_DIR, 'src', 'antigravity-chat-rtl.css');
    const jsPath = path.join(TARGET_DIR, 'src', 'injector', 'rtl-engine.js');
    if (!fs.existsSync(cssPath) || !fs.existsSync(jsPath)) return false;

    const css = fs.readFileSync(cssPath, 'utf8');
    const js = fs.readFileSync(jsPath, 'utf8');

    const ws = new globalThis.WebSocket(page.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
      const tm = setTimeout(() => reject(new Error('timeout')), 4000);
      ws.onopen = () => { clearTimeout(tm); resolve(); };
      ws.onerror = reject;
    });

    let reqId = 1;
    function send(method, params = {}) {
      return new Promise((resolve) => {
        const id = reqId++;
        const handler = (evt) => {
          const msg = JSON.parse(evt.data);
          if (msg.id === id) {
            ws.removeEventListener('message', handler);
            resolve(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    // Inject Engine JS and Initialize with CSS
    await send('Runtime.evaluate', { expression: js });
    await send('Runtime.evaluate', { expression: `if (window.__AG_RTL__) { window.__AG_RTL__.init(${JSON.stringify(css)}); window.__AG_RTL__.processAll(); }` });

    ws.close();
    return true;
  } catch {
    return false;
  }
}

export async function install({ silent = false } = {}) {
  if (!fs.existsSync(PLUGINS_DIR)) {
    fs.mkdirSync(PLUGINS_DIR, { recursive: true });
  }

  copyDirRecursive(ROOT_DIR, TARGET_DIR);

  const reloaded = await triggerLiveReload();
  if (!silent) {
    if (reloaded) {
      console.log('⚡ Live hot-reload applied directly to active Antigravity window!');
    }
  }
  return true;
}

const isMain = process.argv[1] && (path.resolve(process.argv[1]) === __filename || path.resolve(process.argv[1]) === path.resolve(__dirname, 'install-plugin.js'));
if (isMain) {
  install().then(() => {
    console.log(`✅ ${PLUGIN_NAME} installed successfully.`);
    process.exit(0);
  }).catch(err => {
    console.error('Install failed:', err.message);
    process.exit(1);
  });
}
