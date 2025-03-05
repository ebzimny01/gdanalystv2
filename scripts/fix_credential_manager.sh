#! /bin/bash

echo "=== Fixing Git Credential Manager Issues in WSL ==="

# Check if we're running in WSL
if grep -q Microsoft /proc/version; then
    echo "WSL detected - proceeding with WSL-specific fixes"
else
    echo "Not running in WSL - some fixes may not apply"
fi

# Get current credential helper
CURRENT_HELPER=$(git config --get credential.helper)
echo "Current credential helper: $CURRENT_HELPER"

if [[ "$CURRENT_HELPER" == *"manager"* ]]; then
    echo "Git Credential Manager detected - this may be causing the hang"
    
    echo -e "\n1. Setting up a simpler credential helper..."
    
    # Backup current git config
    cp ~/.gitconfig ~/.gitconfig.backup
    echo "Backed up current config to ~/.gitconfig.backup"
    
    # Set credential helper to cache
    git config --global credential.helper cache
    git config --global credential.helper 'cache --timeout=3600'
    echo "Changed credential helper to cache with 1 hour timeout"
    
    # Remove any local credential helper settings
    if git config --local --get credential.helper > /dev/null; then
        echo "Removing local credential helper setting..."
        git config --local --unset credential.helper
    fi
    
    # Check for stored credentials that might be causing issues
    echo -e "\n2. Checking for stored credentials..."
    if [ -f ~/.git-credentials ]; then
        echo "Found stored credentials. Consider reviewing them:"
        cat ~/.git-credentials | sed 's/\/\/.*:.*@/\/\/username:password@/g'
    fi
    
    # Update the project gitconfig
    echo -e "\n3. Updating project gitconfig..."
    cat > /home/edz/code/gdanalystv2/.gitconfig << EOF
[http]
    postBuffer = 524288000
[core]
    compression = 0
[push]
    default = current
[pull]
    rebase = false
[credential]
    helper = cache --timeout=3600
[alias]
    verbose-push = "!GIT_TRACE=1 GIT_CURL_VERBOSE=1 GIT_TRACE_PERFORMANCE=1 git push"
    auth-check = "!bash /home/edz/code/gdanalystv2/scripts/check_git_auth.sh"
EOF
    echo "Updated project gitconfig to use cache credential helper"
    
    echo -e "\n4. Setting up environment to avoid Windows Git tools..."
    echo 'export GIT_TERMINAL_PROMPT=1' >> ~/.bashrc
    echo "Added GIT_TERMINAL_PROMPT=1 to ~/.bashrc"
    export GIT_TERMINAL_PROMPT=1
    
    echo -e "\n5. Creating a file with manual credentials instruction..."
    cat > /home/edz/code/gdanalystv2/scripts/github_credentials.sh << EOF
#!/bin/bash
# Run this script to manually set your GitHub credentials
# This avoids credential manager issues in WSL

echo "Setting up GitHub credentials in git cache"
read -p "GitHub Username: " username
read -sp "GitHub Personal Access Token: " token
echo

git config --global credential.helper cache
echo "https://\$username:\$token@github.com" | git credential approve

echo "Credentials cached. Try pushing now."
EOF
    chmod +x /home/edz/code/gdanalystv2/scripts/github_credentials.sh
    
    echo -e "\nSetup complete. Please try these steps:"
    echo "1. Run: source ~/.bashrc"
    echo "2. Run: /home/edz/code/gdanalystv2/scripts/github_credentials.sh"
    echo "3. Try pushing again with: git push origin your-branch-name"
else
    echo "You're not using Git Credential Manager. The issue might be different."
    echo "Try updating your credential helper:"
    echo "  git config --global credential.helper cache"
fi
