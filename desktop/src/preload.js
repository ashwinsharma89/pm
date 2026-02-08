/**
 * Preload script — secure bridge between Electron main process and renderer.
 * Exposes Claude API methods via contextBridge.
 */

const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  platform: process.platform,
  isElectron: true,

  // Claude API
  claude: {
    setApiKey: (key) => ipcRenderer.invoke("claude:set-api-key", key),
    hasApiKey: () => ipcRenderer.invoke("claude:has-api-key"),
    chat: (message, currentData) => ipcRenderer.invoke("claude:chat", message, currentData),
    clearHistory: () => ipcRenderer.invoke("claude:clear-history"),
    removeApiKey: () => ipcRenderer.invoke("claude:remove-api-key"),
  },
});
