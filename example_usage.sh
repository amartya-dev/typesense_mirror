#!/bin/bash

# Example usage of the Typesense mirror script
# Replace the placeholder values with your actual GitHub credentials

echo "=== Typesense Docker Image Mirror Example ==="

# Set your GitHub credentials (replace with your actual values)
GITHUB_USERNAME="your-github-username"
GITHUB_TOKEN="your-github-token"
GITHUB_REPO="your-github-username/your-repo-name"

# Make the script executable
chmod +x typesense_mirror.py

# Example 1: Mirror latest version
echo "Mirroring latest Typesense image..."
python3 typesense_mirror.py \
  --username "$GITHUB_USERNAME" \
  --token "$GITHUB_TOKEN" \
  --repo "$GITHUB_REPO"

# Example 2: Mirror specific version (uncomment to use)
# echo "Mirroring Typesense v0.25.2..."
# python3 typesense_mirror.py \
#   --username "$GITHUB_USERNAME" \
#   --token "$GITHUB_TOKEN" \
#   --repo "$GITHUB_REPO" \
#   --source-tag 0.25.2 \
#   --target-tag v0.25.2

echo "Done!" 