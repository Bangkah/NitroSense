#!/bin/bash

# NitroSense V3 installer script (Auto Desktop Shortcut)

APP_NAME="Linux NitroSense V3"
APP_IMAGE="Linux_NitroSense_V3-x86_64.AppImage"
APP_URL="https://github.com/Bangkah/NitroSense/releases/download/v3/$APP_IMAGE"
INSTALL_DIR="$HOME/.nitrosense"
DESKTOP_FILE="$HOME/.local/share/applications/nitrosense.desktop"
ICON_FILE="$INSTALL_DIR/nitro_icon.png"

# Step 1: Buat folder installasi
mkdir -p "$INSTALL_DIR"

# Step 2: Download AppImage
echo "Downloading $APP_NAME..."
wget "$APP_URL" -O "$INSTALL_DIR/$APP_IMAGE"

# Step 3: Download icon (atau gunakan yang sudah ada)
echo "Copying icon..."
cp nitro_icon.png "$ICON_FILE"

# Step 4: Set permission executable
chmod +x "$INSTALL_DIR/$APP_IMAGE"

# Step 5: Buat desktop shortcut
echo "Creating desktop shortcut..."
cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Name=$APP_NAME
Comment=Monitor & Control Nitro V16
Exec=$INSTALL_DIR/$APP_IMAGE
Icon=$ICON_FILE
Terminal=false
Type=Application
Categories=Utility;System;
EOL

# Step 6: Update desktop database
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null

echo "Installation complete!"
echo "You can now search for '$APP_NAME' in your applications menu or run it with:"
echo "$INSTALL_DIR/$APP_IMAGE"
