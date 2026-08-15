#!/usr/bin/env bash

# ============================================================================
# GnarlyPi - Headless Android Build & Deployment Tool
# ============================================================================

# Define absolute paths based on your established environment
GNARLY_DIR="$HOME/Repos/personal/python/gnarlypi"
APP_DIR="$GNARLY_DIR/android_app"
DEPLOY_DIR="$GNARLY_DIR/website/static"
BUILD_SCRIPT="$APP_DIR/app/build.gradle.kts"
APK_OUTPUT="$APP_DIR/app/build/outputs/apk/release/app-release.apk"

echo "Initialising headless Gradle compilation..."

# Navigate safely into the Android project root
cd "$APP_DIR" || { echo "Error: Could not locate Android project directory at $APP_DIR"; exit 1; }

# ----------------------------------------------------------------------------
# Dynamic Version Extraction
# ----------------------------------------------------------------------------
# Utilise awk to safely extract the versionName string from the Kotlin build script.
# The 'exit' command ensures it stops at the first match to prevent multi-line errors.
APP_VERSION=$(awk -F'"' '/versionName[[:space:]]*=[[:space:]]*/ {print $2; exit}' "$BUILD_SCRIPT")

# Fallback protection in case the extraction fails or the string is empty
if [ -z "$APP_VERSION" ]; then
    APP_VERSION="latest"
    echo "Warning: Could not extract versionName from build script. Defaulting to '$APP_VERSION'."
else
    echo "Detected target version: $APP_VERSION"
fi

# Instruct the Gradle Wrapper to clean old artifacts and build a fresh, signed release APK
./gradlew clean assembleRelease

# Verify the compilation was successful by checking if the binary file exists
if [ -f "$APK_OUTPUT" ]; then
    echo "Compilation successful. Deploying to Nginx web directory..."
    
    # Copy the binary to the static folder, naming it dynamically using the extracted version
    FINAL_APK_NAME="gnarlypi.${APP_VERSION}.apk"
    cp "$APK_OUTPUT" "$DEPLOY_DIR/$FINAL_APK_NAME"
    
    # Create the static "latest" pointer for the web frontend to ensure links never break
    cp "$APK_OUTPUT" "$DEPLOY_DIR/gnarlypi.latest.apk"
    
    echo "Deployment complete! The updated Android Wrapper ($FINAL_APK_NAME) and latest pointer are now live for download."
else
    echo "Compilation failed. Please check the terminal output above for Kotlin or Gradle errors."
    exit 1
fi