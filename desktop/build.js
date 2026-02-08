#!/usr/bin/env node
/**
 * Build script: Generates the self-contained app.html for the Electron app.
 *
 * If the Flask backend is available (Python), it generates fresh data.
 * Otherwise, it copies the pre-built arsenal_transfer_warroom.html.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const OUTPUT = path.join(__dirname, "app.html");

// Try to find the pre-built standalone HTML first
const prebuilt = path.join(ROOT, "arsenal_transfer_warroom.html");

if (fs.existsSync(prebuilt)) {
  console.log("[build] Using pre-built arsenal_transfer_warroom.html");

  let html = fs.readFileSync(prebuilt, "utf-8");

  // Patch: hide the bridge/WebSocket section (not needed in desktop app)
  // and remove the "Direct Link to Claude Code" card since it won't work
  // Also add electron-specific titlebar padding
  const electronPatch = `
    <style>
      /* Electron: add space for traffic light buttons */
      .top-bar { padding-left: 80px; -webkit-app-region: drag; }
      .top-bar * { -webkit-app-region: no-drag; }
      /* Hide bridge section in desktop app */
      #bridgeStatus { display: none !important; }
    </style>
  `;
  html = html.replace("</head>", electronPatch + "\n</head>");

  fs.writeFileSync(OUTPUT, html, "utf-8");
  console.log(`[build] Written to ${OUTPUT} (${(html.length / 1024).toFixed(0)} KB)`);
} else {
  console.error("[build] ERROR: arsenal_transfer_warroom.html not found.");
  console.error("[build] Run this from the project root after generating the HTML.");
  process.exit(1);
}
