#!/bin/bash
# Script to set up GitHub CLI authentication

echo "Setting up GitHub CLI for authentication"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI not found. Installing..."
    
    # For Ubuntu/Debian based distributions
    if command -v apt &> /dev/null; then
        echo "Installing via apt..."
        sudo apt update
        sudo apt install gh
    # For CentOS/RHEL/Fedora
    elif command -v dnf &> /dev/null; then
        echo "Installing via dnf..."
        sudo dnf install gh
    else
        echo "Unable to detect package manager. Please install GitHub CLI manually:"
        echo "https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
        exit 1
    fi
fi

echo "Authenticating with GitHub CLI..."
gh auth login

echo "Setting up git to use GitHub CLI as a credential helper"
gh auth setup-git

echo "Testing authentication..."
gh auth status

echo "GitHub CLI setup complete. You can now use git commands without tokens!"
echo "Try git push or git pull to verify authentication works properly."
