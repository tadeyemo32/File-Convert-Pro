#!/bin/bash

# Configuration
APP_NAME="FileConverter"
VERSION="1.0.0"
ICON_PATH="../icons/icon.icns"
BUILD_DIR="../build"
DIST_DIR="../dist"
SRC_DIR=$(pwd)

# Clean previous builds
rm -rf "${BUILD_DIR}"/* "${DIST_DIR}"/*

# Build C++ component
cd "${SRC_DIR}"
make clean
make
mv fileconvert "${BUILD_DIR}/"

# Build Python application
pyinstaller \
    --name "${APP_NAME}" \
    --windowed \
    --onefile \
    --icon "${ICON_PATH}" \
    --add-data "${BUILD_DIR}/fileconvert:." \
    --add-data "${ICON_PATH}:icons" \
    --osx-bundle-identifier "com.yourcompany.fileconverter" \
    main.py

# Move build artifacts
mv dist/* "${DIST_DIR}/"
rm -rf build dist *.spec

# Create macOS .app bundle (if on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    cd "${DIST_DIR}"
    create-dmg \
        --volname "${APP_NAME}" \
        --volicon "${ICON_PATH}" \
        --window-pos 200 120 \
        --window-size 800 400 \
        --icon-size 100 \
        --icon "${APP_NAME}.app" 200 190 \
        --hide-extension "${APP_NAME}.app" \
        --app-drop-link 600 185 \
        "${APP_NAME}-${VERSION}.dmg" \
        "${APP_NAME}.app"
fi

echo "Build complete! Check ${DIST_DIR} for output."