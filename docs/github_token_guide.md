# GitHub Personal Access Token Guide

## Creating a New Token

1. Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Name your token and set an expiration date
4. Select the required scopes:
   - `repo` - Full control of private repositories
   - `workflow` - If you need to trigger GitHub Actions
   - `read:packages` - For accessing GitHub Packages
5. Click "Generate token"
6. **IMPORTANT**: Copy and save your token immediately. GitHub will only show it once!

## Using Your Token

### With Git Credential Cache

```bash
# Run the credential helper script
/home/edz/code/gdanalystv2/scripts/github_credentials.sh

# When prompted, enter:
# - Your GitHub username
# - Your personal access token (instead of password)
```

### Manual Git Configuration

```bash
# Configure Git to use your credentials
git config --global credential.helper store
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Store credentials (without showing token in command history)
echo "https://username:your_token_here@github.com" | git credential approve
```

## Security Best Practices

1. **Set an expiration date** for your tokens
2. **Use the minimum permissions** necessary
3. **Never commit tokens** to your repository
4. **Revoke tokens** when no longer needed
5. Consider using **fine-grained tokens** for better security

## Troubleshooting

If you encounter authentication issues:

1. Verify your token has the correct permissions
2. Check if your token has expired
3. Run `git credential-cache exit` to clear cached credentials
4. Try regenerating your token
5. Use the WSL fix script: `/home/edz/code/gdanalystv2/scripts/fix_credential_manager.sh`
