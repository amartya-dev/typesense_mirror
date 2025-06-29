# Typesense Docker Image Mirror

This script fetches the Typesense Docker image from [Docker Hub](https://hub.docker.com/r/typesense/typesense) and pushes it to GitHub Container Registry (GHCR).

## Prerequisites

1. **Docker**: Make sure Docker is installed and running on your system
2. **GitHub Personal Access Token**: You need a GitHub token with `write:packages` permission
3. **Python 3.6+**: The script requires Python 3.6 or higher

## Setup

### 1. Create GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with the following permissions:
   - `write:packages` - to push packages to GitHub Container Registry
   - `read:packages` - to read packages from GitHub Container Registry

### 2. Configure Environment Variables

You have two options for configuration:

#### Option A: Quick Setup (Recommended)
Run the interactive setup script:
```bash
chmod +x setup_env.sh
./setup_env.sh
```

This will prompt you for your credentials and create a `.env` file automatically.

#### Option B: Manual Setup
1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```
2. Edit `.env` and replace the placeholder values with your actual credentials:
   ```bash
   # Your GitHub username
   GITHUB_USERNAME=your-actual-username
   
   # Your GitHub Personal Access Token
   GITHUB_TOKEN=your-actual-token
   
   # GitHub repository name
   GITHUB_REPO=your-username/your-repo-name
   ```

### 3. Make the script executable

```bash
chmod +x typesense_mirror.py
```

## Quick Start

After setting up your environment variables, you can use the example script:

```bash
chmod +x example_usage.sh
./example_usage.sh
```

This will automatically load your configuration from the `.env` file and run the mirror script.

## Usage

### Basic Usage

```bash
python3 typesense_mirror.py \
  --username YOUR_GITHUB_USERNAME \
  --token YOUR_GITHUB_TOKEN \
  --repo YOUR_GITHUB_USERNAME/REPO_NAME
```

### Advanced Usage

```bash
python3 typesense_mirror.py \
  --username YOUR_GITHUB_USERNAME \
  --token YOUR_GITHUB_TOKEN \
  --repo YOUR_GITHUB_USERNAME/REPO_NAME \
  --source-tag 0.25.2 \
  --target-tag v0.25.2 \
  --skip-login
```

### Command Line Arguments

- `--username`: Your GitHub username (required)
- `--token`: GitHub Personal Access Token with `write:packages` permission (required)
- `--repo`: GitHub repository name in format `username/repo-name` (required)
- `--source-tag`: Source tag to pull from Docker Hub (default: `29.0`)
- `--target-tag`: Target tag for GitHub Container Registry (default: `29.0`)
- `--skip-login`: Skip Docker login (useful if already logged in)

## Examples

### Mirror latest version
```bash
python3 typesense_mirror.py \
  --username johndoe \
  --token ghp_xxxxxxxxxxxxxxxxxxxx \
  --repo johndoe/my-typesense-mirror
```

### Mirror specific version
```bash
python3 typesense_mirror.py \
  --username johndoe \
  --token ghp_xxxxxxxxxxxxxxxxxxxx \
  --repo johndoe/my-typesense-mirror \
  --source-tag 0.25.2 \
  --target-tag v0.25.2
```

### Mirror multiple versions
```bash
# Mirror default version (29.0)
python3 typesense_mirror.py \
  --username johndoe \
  --token ghp_xxxxxxxxxxxxxxxxxxxx \
  --repo johndoe/my-typesense-mirror \
  --source-tag 29.0 \
  --target-tag 29.0

# Mirror specific version
python3 typesense_mirror.py \
  --username johndoe \
  --token ghp_xxxxxxxxxxxxxxxxxxxx \
  --repo johndoe/my-typesense-mirror \
  --source-tag 0.25.2 \
  --target-tag v0.25.2
```

## Using the Mirrored Image

After successfully running the script, you can use the mirrored image:

```bash
# Pull the image
docker pull ghcr.io/YOUR_USERNAME/REPO_NAME/typesense:29.0

# Run Typesense
docker run -p 8108:8108 -v typesense-data:/data \
  ghcr.io/YOUR_USERNAME/REPO_NAME/typesense:29.0 \
  --data-dir /data --api-key=xyz --enable-cors
```

## GitHub Actions Integration

You can also use this script in GitHub Actions to automatically mirror images:

```yaml
name: Mirror Typesense Image

on:
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM
  workflow_dispatch:  # Allow manual trigger

jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Mirror Typesense image
        run: |
          python3 typesense_mirror.py \
            --username ${{ github.actor }} \
            --token ${{ secrets.GITHUB_TOKEN }} \
            --repo ${{ github.repository }} \
            --source-tag 29.0 \
            --target-tag 29.0
```

## Security Notes

- Never commit your GitHub token to version control
- Use environment variables or GitHub Secrets to store sensitive information
- Consider using GitHub Actions for automated mirroring instead of running locally

## Troubleshooting

### Docker not running
```
Error: Docker is not installed or not running.
```
**Solution**: Start Docker Desktop or Docker daemon

### Authentication failed
```
Failed to login to GitHub Container Registry
```
**Solution**: 
- Verify your GitHub token has `write:packages` permission
- Check that your username is correct
- Ensure the token hasn't expired

### Permission denied
```
denied: requested access to the resource is denied
```
**Solution**: 
- Verify your GitHub token has the correct permissions
- Check that the repository name format is correct (`username/repo-name`)
- Ensure the repository exists and you have access to it

## License

This script is provided as-is for educational and development purposes. 