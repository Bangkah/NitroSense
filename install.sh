#!/bin/bash

# NitroSense V3 installer script

echo "Downloading Linux NitroSense V3..."
wget https://github.com/Bangkah/NitroSense/releases/download/v3/Linux_NitroSense_V3-x86_64.AppImage -O Linux_NitroSense_V3-x86_64.AppImage

echo "Setting executable permission..."
chmod +x Linux_NitroSense_V3-x86_64.AppImage

echo "Installation complete!"
echo "Run the app with: ./Linux_NitroSense_V3-x86_64.AppImage"
