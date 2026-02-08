#!/bin/bash
# ============================================================
# Arsenal Transfer War Room - macOS App Builder
# ============================================================
# Run this on your Mac to build the .app:
#
#   cd desktop
#   bash setup-and-build.sh
#
# Prerequisites: Node.js (v18+). Install from https://nodejs.org
# ============================================================

set -e

echo ""
echo "  =========================================="
echo "  Arsenal Transfer War Room - macOS Builder"
echo "  =========================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Install from https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "ERROR: Node.js 18+ required (found v$(node -v))"
    exit 1
fi

echo "[1/4] Installing dependencies..."
npm install

echo ""
echo "[2/4] Building app.html..."
node build.js

echo ""
echo "[3/4] Generating app icon..."
if [ -f icons/icon.icns ]; then
    echo "  Icon already exists, skipping."
else
    if command -v iconutil &> /dev/null; then
        cd icons
        bash create-icon.sh 2>/dev/null || echo "  Icon generation skipped (install rsvg-convert or provide icon_1024.png)"
        cd ..
    else
        echo "  iconutil not available, skipping icon generation."
        echo "  (The app will use a default icon)"
    fi
fi

echo ""
echo "[4/4] Building macOS app..."
npx electron-builder --mac

echo ""
echo "  =========================================="
echo "  BUILD COMPLETE!"
echo "  =========================================="
echo ""
echo "  Your app is in: desktop/dist/"
echo ""
echo "  To install:"
echo "    1. Open the .dmg file in dist/"
echo "    2. Drag 'Arsenal Transfer War Room' to Applications"
echo "    3. Launch from Applications or Spotlight"
echo ""
echo "  Or run directly:"
echo "    npm start"
echo ""
