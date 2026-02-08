#!/bin/bash
# Generates macOS .icns icon from the SVG.
# Run this on macOS: cd desktop/icons && bash create-icon.sh

set -e

# Create iconset directory
mkdir -p icon.iconset

# Use sips to convert SVG → PNG at various sizes
# First create a 1024x1024 PNG from the SVG
# If you have a PNG already, skip the conversion step
if command -v rsvg-convert &> /dev/null; then
    rsvg-convert -w 1024 -h 1024 icon.svg > icon_1024.png
elif command -v convert &> /dev/null; then
    convert -background none -resize 1024x1024 icon.svg icon_1024.png
else
    echo "No SVG converter found. Please provide a 1024x1024 icon_1024.png manually."
    echo "You can use any online SVG-to-PNG converter with the icon.svg file."
    exit 1
fi

# Generate all required sizes
for size in 16 32 128 256 512; do
    sips -z $size $size icon_1024.png --out icon.iconset/icon_${size}x${size}.png
    double=$((size * 2))
    sips -z $double $double icon_1024.png --out icon.iconset/icon_${size}x${size}@2x.png
done

# Generate the .icns file
iconutil -c icns icon.iconset -o icon.icns

# Cleanup
rm -rf icon.iconset icon_1024.png

echo "Created icon.icns successfully!"
