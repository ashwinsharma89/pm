// Preload script — runs before the renderer page loads.
// Provides a safe bridge between the Electron main process and the web content.

const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  platform: process.platform,
  isElectron: true,
});
