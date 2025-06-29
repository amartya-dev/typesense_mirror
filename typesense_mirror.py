#!/usr/bin/env python3
"""
Script to fetch Typesense Docker image from Docker Hub and push it to GitHub Container Registry.
"""

import subprocess
import sys
import os
import argparse
from typing import Optional


def run_command(command: list, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, check=check)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def check_docker_installed() -> bool:
    """Check if Docker is installed and running."""
    try:
        run_command(["docker", "--version"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Docker is not installed or not running.")
        return False


def login_to_ghcr(username: str, token: str) -> bool:
    """Login to GitHub Container Registry."""
    try:
        run_command([
            "docker", "login", "ghcr.io", 
            "-u", username, 
            "-p", token
        ])
        print("Successfully logged in to GitHub Container Registry")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to login to GitHub Container Registry: {e}")
        return False


def pull_typesense_image(tag: str = "latest") -> bool:
    """Pull Typesense image from Docker Hub."""
    try:
        run_command([
            "docker", "pull", f"typesense/typesense:{tag}"
        ])
        print(f"Successfully pulled typesense/typesense:{tag}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull Typesense image: {e}")
        return False


def tag_for_ghcr(source_tag: str, target_repo: str, target_tag: str) -> bool:
    """Tag the image for GitHub Container Registry."""
    try:
        run_command([
            "docker", "tag", 
            f"typesense/typesense:{source_tag}",
            f"ghcr.io/{target_repo}/typesense:{target_tag}"
        ])
        print(f"Successfully tagged image as ghcr.io/{target_repo}/typesense:{target_tag}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to tag image: {e}")
        return False


def push_to_ghcr(target_repo: str, tag: str) -> bool:
    """Push the image to GitHub Container Registry."""
    try:
        run_command([
            "docker", "push", f"ghcr.io/{target_repo}/typesense:{tag}"
        ])
        print(f"Successfully pushed to ghcr.io/{target_repo}/typesense:{tag}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to push to GitHub Container Registry: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Mirror Typesense Docker image to GitHub Container Registry"
    )
    parser.add_argument(
        "--username", 
        required=True,
        help="GitHub username"
    )
    parser.add_argument(
        "--token", 
        required=True,
        help="GitHub Personal Access Token with write:packages permission"
    )
    parser.add_argument(
        "--repo", 
        required=True,
        help="GitHub repository name (e.g., 'username/repo-name')"
    )
    parser.add_argument(
        "--source-tag", 
        default="latest",
        help="Source tag to pull from Docker Hub (default: latest)"
    )
    parser.add_argument(
        "--target-tag", 
        default="latest",
        help="Target tag for GitHub Container Registry (default: latest)"
    )
    parser.add_argument(
        "--skip-login", 
        action="store_true",
        help="Skip Docker login (useful if already logged in)"
    )

    args = parser.parse_args()

    print("=== Typesense Docker Image Mirror Script ===")
    print(f"Source: typesense/typesense:{args.source_tag}")
    print(f"Target: ghcr.io/{args.repo}/typesense:{args.target_tag}")
    print()

    # Check if Docker is installed
    if not check_docker_installed():
        sys.exit(1)

    # Login to GitHub Container Registry
    if not args.skip_login:
        if not login_to_ghcr(args.username, args.token):
            sys.exit(1)

    # Pull Typesense image
    if not pull_typesense_image(args.source_tag):
        sys.exit(1)

    # Tag for GitHub Container Registry
    if not tag_for_ghcr(args.source_tag, args.repo, args.target_tag):
        sys.exit(1)

    # Push to GitHub Container Registry
    if not push_to_ghcr(args.repo, args.target_tag):
        sys.exit(1)

    print("\n=== Success! ===")
    print(f"Typesense image has been successfully mirrored to:")
    print(f"ghcr.io/{args.repo}/typesense:{args.target_tag}")
    print("\nYou can now use this image with:")
    print(f"docker pull ghcr.io/{args.repo}/typesense:{args.target_tag}")


if __name__ == "__main__":
    main() 