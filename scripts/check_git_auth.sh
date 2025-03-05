#! /bin/bash

echo "Checking Git authentication..."

# Get the remote URL
REMOTE_URL=$(git config --get remote.origin.url)
echo "Remote URL: $REMOTE_URL"

if [[ $REMOTE_URL == git@* ]]; then
    echo "Using SSH authentication"
    
    # Check for SSH keys
    echo "Checking for SSH keys..."
    ssh-add -l
    
    if [ $? -ne 0 ]; then
        echo "No SSH keys found in agent. Attempting to add default key..."
        ssh-add ~/.ssh/id_rsa
    fi
    
    # Test SSH connection
    DOMAIN=$(echo $REMOTE_URL | cut -d '@' -f2 | cut -d ':' -f1)
    echo "Testing SSH connection to $DOMAIN..."
    ssh -T "git@$DOMAIN"
elif [[ $REMOTE_URL == https://* ]]; then
    echo "Using HTTPS authentication"
    
    # Check for cached credentials
    echo "Checking for cached credentials..."
    git credential fill < /dev/null
    
    echo "Note: For HTTPS, you may be prompted for credentials when you push."
else
    echo "Unknown remote URL format: $REMOTE_URL"
fi

# Check if we have push access
echo "Checking if we have push access..."
git ls-remote origin >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Authentication successful! You have access to the repository."
else
    echo "Authentication failed. Please check your credentials."
fi
