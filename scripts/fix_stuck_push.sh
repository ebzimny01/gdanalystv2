#! /bin/bash

echo "=== Advanced Git Push Troubleshooting ==="
echo "This script will help resolve issues with stuck git push operations"

# Get the current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"

# Check remote URL and connection
echo -e "\n1. Checking remote repository connection..."
REMOTE_URL=$(git config --get remote.origin.url)
echo "Remote URL: $REMOTE_URL"

# Check network connectivity to GitHub
echo -e "\n2. Testing network connectivity to GitHub..."
ping -c 4 github.com
if [ $? -ne 0 ]; then
    echo "WARNING: Network connectivity issues detected!"
fi

# Check for large files
echo -e "\n3. Checking for large files that might be causing issues..."
echo "Files larger than 50MB in your repo:"
find . -type f -size +50M -not -path "./.git/*"

# Check network issues
echo -e "\n4. Checking for network-related issues..."
GITHUB_IP=$(dig +short github.com)
echo "GitHub IP address: $GITHUB_IP"
echo "Running traceroute to GitHub:"
traceroute -m 15 github.com

# Kill any hung Git processes
echo -e "\n5. Killing any hung Git processes..."
pkill -f git

# Fix potential SSH/HTTPS issues
echo -e "\n6. Applying fixes based on protocol..."
if [[ $REMOTE_URL == https://* ]]; then
    echo "Using HTTPS protocol"
    
    # Increase buffer size and disable compression
    git config --local http.postBuffer 524288000
    git config --local core.compression 0
    
    echo "Do you want to try disabling SSL verification (security risk)? (y/n)"
    read -r answer
    if [[ $answer == "y" ]]; then
        git config --local http.sslVerify false
        echo "SSL verification disabled temporarily"
    fi
else
    echo "Using SSH protocol"
    echo "Testing SSH connection:"
    ssh -T git@github.com
fi

# Clear cache and try alternative push method
echo -e "\n7. Clearing Git credential cache..."
git credential-cache exit

echo -e "\n8. Trying alternative push methods..."
echo "Do you want to try pushing with the --force-with-lease option? (y/n)"
read -r answer
if [[ $answer == "y" ]]; then
    echo "Attempting push with --force-with-lease..."
    GIT_TRACE=1 GIT_CURL_VERBOSE=1 git push --force-with-lease origin "$CURRENT_BRANCH"
    exit $?
fi

echo "Do you want to try pushing with limited depth? (y/n)"
read -r answer
if [[ $answer == "y" ]]; then
    echo "Creating a new temporary branch with limited history..."
    TEMP_BRANCH="temp-${CURRENT_BRANCH}-$(date +%s)"
    git checkout -b "$TEMP_BRANCH"
    git push origin "$TEMP_BRANCH"
    git checkout "$CURRENT_BRANCH"
    git branch -D "$TEMP_BRANCH"
    exit $?
fi

echo -e "\n9. Final recommendations:"
echo "- Try using Git LFS if you have large files"
echo "- Check GitHub status page for service disruptions"
echo "- Consider cloning the repository again in a new location"
echo "- Try pushing from a different network"
echo "- If all else fails, contact GitHub support"

echo -e "\nWould you like to try pushing again with maximum verbosity? (y/n)"
read -r answer
if [[ $answer == "y" ]]; then
    echo "Pushing with maximum verbosity..."
    GIT_TRACE=2 GIT_CURL_VERBOSE=2 GIT_TRACE_PACKET=2 GIT_TRACE_PERFORMANCE=2 git push origin "$CURRENT_BRANCH"
fi
