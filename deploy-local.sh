#!/bin/bash

set -e

echo "Starting local deployment (without Git update)..."

# Change to project directory, exit if not found
cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

echo "Using current local code (no Git update)"

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
sudo systemctl start mysql || {
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

echo "Local deployment completed successfully!"
echo "Your app should be running at: http://your-domain:5001"
