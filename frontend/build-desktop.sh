#!/bin/bash

# QBClone Desktop Build Script
# This script builds the QBClone desktop application for Windows

echo "🚀 Building QBClone Desktop Application..."
echo "=========================================="

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the frontend directory"
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/
rm -rf build/

# Install dependencies
echo "📦 Installing dependencies..."
yarn install

# Build React application
echo "⚛️  Building React application..."
yarn build

# Check if build was successful
if [ ! -d "build" ]; then
    echo "❌ Error: React build failed"
    exit 1
fi

echo "✅ React build completed successfully"

# Build Electron application
echo "🖥️  Building Electron desktop application..."
echo "   Target: Windows x64"
echo "   Format: NSIS Installer"

yarn electron-pack --win

# Check if Electron build was successful
if [ -d "dist" ]; then
    echo "✅ Desktop application build completed!"
    echo ""
    echo "📁 Build artifacts:"
    ls -la dist/
    echo ""
    echo "🎉 QBClone Desktop Application is ready!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Find the installer in the 'dist' folder"
    echo "   2. Test the application: yarn electron"
    echo "   3. Distribute the installer to users"
else
    echo "❌ Error: Electron build failed"
    exit 1
fi