#!/bin/bash

set -e

echo "Starting redeployment process"

# Change to project directory, exit if not found
cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

# Pull latest changes from main branch
echo "Updating code from Git"
# First, check if we can access the repository
if git ls-remote origin > /dev/null 2>&1; then
    echo "Git access confirmed, pulling latest changes..."
    git fetch && git reset --hard origin/main || {
        echo "Error: Failed to update git repository"
        exit 1
    }
else
    echo "Warning: Cannot access Git repository (SSH key issue or network problem)"
    echo "Skipping Git update - using current local code"
    echo "To fix this, either:"
    echo "1. Set up SSH keys for GitHub access, or"
    echo "2. Change remote URL to HTTPS: git remote set-url origin https://github.com/AyanMulla09/flask-portfolio.git"
    echo "3. Or manually pull changes before running this script"
    echo ""
    echo "Continuing with deployment using current code..."
    sleep 3
fi

# Activate virtual environment
echo "Activating virtual environment"
source /root/flask-portfolio/python3-virtualenv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

# Install dependencies
echo "Installing Python dependencies"
pip install -r requirements.txt || {
    echo "Error: Failed to install dependencies"
    exit 1
}

# Ensure MySQL service is running
echo "Checking MySQL service"
sudo systemctl start mysqld || {
    echo "Warning: MySQL service might not be running"
}

# Copy systemd service file to proper location if it doesn't exist
if [ ! -f /etc/systemd/system/myportfolio.service ]; then
    echo "Installing systemd service file"
    sudo cp myportfolio.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable myportfolio
fi

# Restart the systemd service
echo "Restarting myportfolio service"
sudo systemctl restart myportfolio || {
    echo "Error: Failed to restart myportfolio service"
    exit 1
}

# Check status
echo "Checking service status"
sudo systemctl status myportfolio --no-pager

echo "Redeployment completed successfully!"
