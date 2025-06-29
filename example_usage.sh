#!/bin/bash

# Example usage of the Typesense mirror script
# This script loads configuration from environment variables and .env file

echo "=== Typesense Docker Image Mirror Example ==="

# Function to load environment variables from .env file
load_env() {
    if [ -f ".env" ]; then
        echo "Loading configuration from .env file..."
        export $(cat .env | grep -v '^#' | xargs)
    else
        echo "Warning: .env file not found. Using environment variables or defaults."
    fi
}

# Load environment variables
load_env

# Validate required environment variables
if [ -z "$GITHUB_USERNAME" ]; then
    echo "Error: GITHUB_USERNAME is not set. Please set it in .env file or environment."
    exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is not set. Please set it in .env file or environment."
    exit 1
fi

if [ -z "$GITHUB_REPO" ]; then
    echo "Error: GITHUB_REPO is not set. Please set it in .env file or environment."
    exit 1
fi

# Set defaults for optional variables
TYPESENSE_VERSION=${TYPESENSE_VERSION:-"29.0"}
TARGET_TAG=${TARGET_TAG:-"$TYPESENSE_VERSION"}

echo "Configuration:"
echo "  GitHub Username: $GITHUB_USERNAME"
echo "  GitHub Repository: $GITHUB_REPO"
echo "  Typesense Version: $TYPESENSE_VERSION"
echo "  Target Tag: $TARGET_TAG"
echo ""

# Make the script executable
chmod +x typesense_mirror.py

# Example 1: Mirror with configuration from .env
echo "Mirroring Typesense image with configuration from .env..."
python3 typesense_mirror.py \
  --username "$GITHUB_USERNAME" \
  --token "$GITHUB_TOKEN" \
  --repo "$GITHUB_REPO" \
  --source-tag "$TYPESENSE_VERSION" \
  --target-tag "$TARGET_TAG"

# Example 2: Mirror specific version (uncomment to use)
# echo "Mirroring Typesense v0.25.2..."
# python3 typesense_mirror.py \
#   --username "$GITHUB_USERNAME" \
#   --token "$GITHUB_TOKEN" \
#   --repo "$GITHUB_REPO" \
#   --source-tag "0.25.2" \
#   --target-tag "v0.25.2"

echo "Done!" 