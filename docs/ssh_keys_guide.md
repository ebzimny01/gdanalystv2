# GitHub SSH Key Authentication Guide

SSH keys provide a secure and convenient alternative to Personal Access Tokens.

## Benefits of SSH Authentication
- No need to enter passwords or tokens
- More secure than password authentication
- No expiration (unless you set one)
- Works reliably across platforms including WSL

## Setting Up SSH Authentication

### 1. Generate an SSH Key
```bash
# Generate a new SSH key (press Enter when prompted for file location and passphrase)
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. Start the SSH Agent
```bash
# Start the ssh-agent in the background
eval "$(ssh-agent -s)"

# Add your SSH key to the agent
ssh-add ~/.ssh/id_ed25519
```

### 3. Add the SSH Key to GitHub
```bash
# Copy your public key to clipboard 
# In WSL, you might need to manually copy from the terminal
cat ~/.ssh/id_ed25519.pub
```

Then:
1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Add a title (e.g., "WSL Development Machine")
4. Paste your public key
5. Click "Add SSH key"

### 4. Test the Connection
```bash
ssh -T git@github.com
```
You should see: "Hi username! You've successfully authenticated..."

### 5. Change Your Repository to Use SSH

If your repository currently uses HTTPS, change it to SSH:

```bash
# Check current remote URL
git remote -v

# Change from HTTPS to SSH
git remote set-url origin git@github.com:username/repository.git
```

## Troubleshooting SSH Issues

If you encounter issues:

1. Ensure ssh-agent is running: `eval "$(ssh-agent -s)"`
2. Add your key again: `ssh-add ~/.ssh/id_ed25519`
3. Verify permissions: `chmod 600 ~/.ssh/id_ed25519`
4. Check connection: `ssh -vT git@github.com`
