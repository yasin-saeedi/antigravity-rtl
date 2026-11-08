import fs from 'fs';
import path from 'path';
import os from 'os';
import { EventEmitter } from 'events';

const DEVTOOLS_PORT_PATH = path.join(
  process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'),
  'Antigravity',
  'DevToolsActivePort'
);

export class CdpBridge extends EventEmitter {
  constructor() {
    super();
    this.ws = null;
    this.port = null;
    this.msgId = 1;
    this.pendingCallbacks = new Map();
    this.isConnected = false;
    this.isConnecting = false;
    this.reconnectTimer = null;
  }

  getDevToolsPort() {
    if (!fs.existsSync(DEVTOOLS_PORT_PATH)) return null;
    try {
      const content = fs.readFileSync(DEVTOOLS_PORT_PATH, 'utf8').trim().split('\n');
      const port = parseInt(content[0].trim(), 10);
      return isNaN(port) ? null : port;
    } catch {
      return null;
    }
  }

  async findMainTarget() {
    this.port = this.getDevToolsPort();
    if (!this.port) return null;

    try {
      const res = await fetch(`http://127.0.0.1:${this.port}/json`, {
        signal: AbortSignal.timeout(3000)
      });
      if (!res.ok) return null;
      const targets = await res.json();
      return targets.find(t => t.type === 'page' && (t.url?.includes('127.0.0.1') || t.title?.includes('Antigravity') || t.url?.includes('workbench.html')));
    } catch {
      return null;
    }
  }

  async connect() {
    if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
      return true;
    }
    if (this.isConnecting) {
      return false;
    }
    this.isConnecting = true;

    try {
      const target = await this.findMainTarget();
      if (!target || !target.webSocketDebuggerUrl) {
        this.scheduleReconnect();
        return false;
      }

      return await new Promise((resolve) => {
        let settled = false;
        const connectTimeout = setTimeout(() => {
          try { this.ws?.close(); } catch {}
          done(false);
        }, 5000);

        const done = (val) => {
          if (!settled) {
            settled = true;
            clearTimeout(connectTimeout);
            resolve(val);
          }
        };

        try {
          this.ws = new WebSocket(target.webSocketDebuggerUrl);

          this.ws.onopen = async () => {
            this.isConnected = true;
            this.isConnecting = false;

            // Enable Page and Runtime domains
            try {
              await this.send('Page.enable');
              await this.send('Runtime.enable');
            } catch {}

            this.emit('connected');
            done(true);
          };

          this.ws.onmessage = (event) => {
            try {
              const msg = JSON.parse(event.data);
              if (msg.id && this.pendingCallbacks.has(msg.id)) {
                const { resolve, reject } = this.pendingCallbacks.get(msg.id);
                this.pendingCallbacks.delete(msg.id);
                if (msg.error) reject(new Error(msg.error.message || 'CDP Error'));
                else resolve(msg.result);
              } else if (msg.method) {
                this.emit('event', msg);
              }
            } catch {}
          };

          this.ws.onclose = () => {
            this.cleanup();
            done(false);
            this.scheduleReconnect();
          };

          this.ws.onerror = () => {
            this.cleanup();
            done(false);
            this.scheduleReconnect();
          };
        } catch {
          this.cleanup();
          done(false);
          this.scheduleReconnect();
        }
      });
    } catch {
      this.cleanup();
      this.scheduleReconnect();
      return false;
    }
  }

  cleanup() {
    this.isConnected = false;
    this.isConnecting = false;
    this.ws = null;
    for (const { reject } of this.pendingCallbacks.values()) {
      reject(new Error('CDP connection closed'));
    }
    this.pendingCallbacks.clear();
    this.emit('disconnected');
  }

  scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(async () => {
      this.reconnectTimer = null;
      await this.connect();
    }, 4000);
  }

  send(method, params = {}, timeoutMs = 5000) {
    if (!this.isConnected || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
      return Promise.reject(new Error('CDP bridge is not connected'));
    }

    const id = this.msgId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pendingCallbacks.delete(id);
        reject(new Error(`CDP request ${method} timed out after ${timeoutMs}ms`));
      }, timeoutMs);

      this.pendingCallbacks.set(id, {
        resolve: (val) => { clearTimeout(timer); resolve(val); },
        reject: (err) => { clearTimeout(timer); reject(err); }
      });

      try {
        this.ws.send(JSON.stringify({ id, method, params }));
      } catch (err) {
        clearTimeout(timer);
        this.pendingCallbacks.delete(id);
        reject(err);
      }
    });
  }

  async evaluate(expression, returnByValue = true, timeoutMs = 5000) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue,
      awaitPromise: true
    }, timeoutMs);
    return res?.result?.value;
  }
}
