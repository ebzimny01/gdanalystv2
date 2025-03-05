#!/bin/bash
# Run this script to manually set your GitHub credentials
# This avoids credential manager issues in WSL

echo "Setting up GitHub credentials in git cache"
read -p "GitHub Username: " username
read -sp "GitHub Personal Access Token: " token
echo

git config --global credential.helper cache
echo "https://$username:$token@github.com" | git credential approve

echo "Credentials cached. Try pushing now."
