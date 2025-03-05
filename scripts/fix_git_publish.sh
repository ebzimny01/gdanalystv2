#! /bin/bash
# This script attempts to fix a stuck Git publish process by checking for running Git processes,

echo "Attempting to fix stuck Git publish process..."

# 1. Check for running Git processes
echo "Checking for running Git processes..."
ps aux | grep git

# 2. Kill any hung Git processes
echo "Killing any hung Git processes..."
pkill -f git

# 3. Clean up lock files
echo "Cleaning up any Git lock files..."
find .git -name "*.lock" -type f -delete

# 4. Reset Git state
echo "Resetting Git state..."
git reset --mixed

# 5. Check Git status
echo "Current Git status:"
git status

echo "Fix complete. Please try publishing your branch again."
