#! /bin/bash
# This script attempts to fix a stuck Git publish process by checking for running Git processes,

echo "Attempting to fix stuck Git publish process..."

# 1. Check for running Git processes
echo "Checking for running Git processes..."
ps aux | grep git

# 2. Check remote repository configuration
echo "Checking remote repository configuration..."
echo "Remote repositories:"
git remote -v
echo "Detailed origin information:"
git remote show origin

# 3. Kill any hung Git processes
echo "Killing any hung Git processes..."
pkill -f git

# 4. Clean up lock files
echo "Cleaning up any Git lock files..."
find .git -name "*.lock" -type f -delete

# 5. Reset Git state
echo "Resetting Git state..."
git reset --mixed

# 6. Check Git status
echo "Current Git status:"
git status

echo "Fix complete. Please try publishing your branch again."
