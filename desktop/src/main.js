const { app, BrowserWindow, Menu, shell, dialog, ipcMain } = require("electron");
const path = require("path");
const fs = require("fs");

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 900,
    minHeight: 600,
    title: "Arsenal Transfer War Room",
    backgroundColor: "#0d1117",
    titleBarStyle: "hiddenInset",
    trafficLightPosition: { x: 16, y: 16 },
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
    },
    show: false,
  });

  // Load the self-contained HTML
  const htmlPath = path.join(__dirname, "..", "app.html");
  mainWindow.loadFile(htmlPath);

  // Show window when ready (prevents white flash)
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  // Build native macOS menu
  buildMenu();
}

function buildMenu() {
  const template = [
    {
      label: app.name,
      submenu: [
        { role: "about" },
        { type: "separator" },
        {
          label: "Preferences...",
          accelerator: "Cmd+,",
          click: () => {
            mainWindow.webContents.executeJavaScript(`
              document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
              document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
              document.querySelector('[data-tab="intel"]').classList.add('active');
              document.getElementById('tab-intel').classList.add('active');
            `);
          },
        },
        { type: "separator" },
        { role: "hide" },
        { role: "hideOthers" },
        { role: "unhide" },
        { type: "separator" },
        { role: "quit" },
      ],
    },
    {
      label: "View",
      submenu: [
        {
          label: "Overview",
          accelerator: "Cmd+1",
          click: () => switchTab("overview"),
        },
        {
          label: "Squad Analysis",
          accelerator: "Cmd+2",
          click: () => switchTab("squad"),
        },
        {
          label: "Sell Recommendations",
          accelerator: "Cmd+3",
          click: () => switchTab("sell"),
        },
        {
          label: "Buy Recommendations",
          accelerator: "Cmd+4",
          click: () => switchTab("buy"),
        },
        {
          label: "Financial Model",
          accelerator: "Cmd+5",
          click: () => switchTab("financial"),
        },
        {
          label: "Rival Analysis",
          accelerator: "Cmd+6",
          click: () => switchTab("rivals"),
        },
        {
          label: "Strategy Timeline",
          accelerator: "Cmd+7",
          click: () => switchTab("strategy"),
        },
        {
          label: "Live Intel Updates",
          accelerator: "Cmd+8",
          click: () => switchTab("intel"),
        },
        { type: "separator" },
        { role: "reload" },
        { role: "toggleDevTools" },
        { type: "separator" },
        { role: "resetZoom" },
        { role: "zoomIn" },
        { role: "zoomOut" },
        { type: "separator" },
        { role: "togglefullscreen" },
      ],
    },
    {
      label: "Transfer",
      submenu: [
        {
          label: "Recalculate Plan",
          accelerator: "Cmd+R",
          click: () => {
            mainWindow.webContents.executeJavaScript(
              `document.getElementById('refreshBtn').click()`
            );
          },
        },
        {
          label: "Apply Intel Changes",
          accelerator: "Cmd+Shift+A",
          click: () => {
            mainWindow.webContents.executeJavaScript(
              `document.getElementById('intelApplyBtn').click()`
            );
          },
        },
        {
          label: "Reset All Intel",
          accelerator: "Cmd+Shift+R",
          click: () => {
            dialog
              .showMessageBox(mainWindow, {
                type: "warning",
                buttons: ["Cancel", "Reset"],
                defaultId: 0,
                title: "Reset Intel",
                message: "Reset all intel updates?",
                detail:
                  "This will clear all target status changes, fee adjustments, and notes. This cannot be undone.",
              })
              .then((result) => {
                if (result.response === 1) {
                  mainWindow.webContents.executeJavaScript(
                    `document.getElementById('intelResetBtn').click()`
                  );
                }
              });
          },
        },
        { type: "separator" },
        {
          label: "Export Intel Report",
          accelerator: "Cmd+E",
          click: () => {
            mainWindow.webContents.executeJavaScript(
              `document.getElementById('exportBtn').click()`
            );
            switchTab("intel");
          },
        },
      ],
    },
    {
      label: "Window",
      submenu: [
        { role: "minimize" },
        { role: "zoom" },
        { type: "separator" },
        { role: "front" },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

function switchTab(tabName) {
  mainWindow.webContents.executeJavaScript(`
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
    document.querySelector('[data-tab="${tabName}"]').classList.add('active');
    document.getElementById('tab-${tabName}').classList.add('active');
  `);
}

// macOS: re-create window when dock icon clicked
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.whenReady().then(createWindow);
