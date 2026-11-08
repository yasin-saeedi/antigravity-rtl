import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { CdpBridge } from './cdp-bridge.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CSS_PATH = path.join(__dirname, '..', 'antigravity-chat-rtl.css');
const ENGINE_JS_PATH = path.join(__dirname, '..', 'injector', 'rtl-engine.js');

async function main() {
  console.log('🌌 Antigravity RTL & Persian Typography Sidecar Starting...');

  const cdp = new CdpBridge();

  async function injectRTL() {
    try {
      if (!fs.existsSync(CSS_PATH) || !fs.existsSync(ENGINE_JS_PATH)) {
        console.warn('[rtl-sidecar] Missing CSS or Engine file');
        return;
      }

      const cssContent = fs.readFileSync(CSS_PATH, 'utf8');
      const engineJs = fs.readFileSync(ENGINE_JS_PATH, 'utf8');

      // 1. Evaluate in-DOM engine script
      await cdp.evaluate(engineJs, false, 6000);

      // 2. Initialize engine with CSS
      const initExpr = `if (window.__AG_RTL__) { window.__AG_RTL__.init(${JSON.stringify(cssContent)}); }`;
      await cdp.evaluate(initExpr, false, 6000);

      console.log('[rtl-sidecar] Successfully injected RTL engine & Persian fonts into Antigravity window.');
    } catch (err) {
      console.warn('[rtl-sidecar] Injection notice:', err.message);
    }
  }

  cdp.on('connected', async () => {
    console.log('[rtl-sidecar] Connected to Antigravity DevTools via CDP.');
    setTimeout(async () => {
      await injectRTL();
    }, 800);
  });

  // Watch for page navigation / reloads
  let reloadDebounce = null;
  cdp.on('event', async (data) => {
    if (data.method === 'Page.loadEventFired') {
      if (reloadDebounce) clearTimeout(reloadDebounce);
      reloadDebounce = setTimeout(async () => {
        console.log('[rtl-sidecar] Page load detected. Re-injecting RTL engine.');
        await injectRTL();
      }, 600);
    }
  });

  // Watchdog: Ensure styles and engine remain active in DOM
  setInterval(async () => {
    if (cdp.isConnected) {
      try {
        const injected = await cdp.evaluate('!!document.getElementById("antigravity-chat-rtl-style")', true, 2000);
        if (!injected) {
          await injectRTL();
        }
      } catch {}
    }
  }, 4000);

  // Initial connect
  await cdp.connect();

  // Keep process alive
  setInterval(() => {}, 60000);
}

main().catch(err => {
  console.error('[rtl-sidecar] Fatal error:', err);
  process.exit(1);
});
