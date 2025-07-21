#!/bin/bash

echo "Fixing Git remote URL to use HTTPS instead of SSH..."

# Change to project directory
cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

# Show current remote URL
echo "Current remote URL:"
git remote -v

# Change to HTTPS URL
echo "Changing remote URL to HTTPS..."
git remote set-url origin https://github.com/AyanMulla09/flask-portfolio.git

# Verify the change
echo "New remote URL:"
git remote -v

# Test if we can access the repository now
echo "Testing Git access..."
if git ls-remote origin > /dev/null 2>&1; then
    echo "✅ Git access successful! You can now use the redeploy script."
    echo "To pull latest changes, run: git pull origin main"
else
    echo "❌ Git access still failed. You may need to:"
    echo "1. Check your internet connection"
    echo "2. Verify the repository exists and is public"
    echo "3. Use a personal access token if the repo is private"
fi
