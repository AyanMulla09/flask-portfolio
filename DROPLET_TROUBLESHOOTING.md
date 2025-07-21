# Droplet Deployment Troubleshooting Guide

## Git SSH Issues (Current Problem)

### Problem
```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

### Solutions

#### Option 1: Switch to HTTPS (Recommended)
```bash
cd /root/flask-portfolio
chmod +x fix-git-remote.sh
./fix-git-remote.sh
```

#### Option 2: Set up SSH Keys
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add this key to your GitHub account:
# 1. Go to GitHub Settings > SSH and GPG keys
# 2. Click "New SSH key"
# 3. Paste the public key content
```

#### Option 3: Deploy without Git updates
```bash
cd /root/flask-portfolio
chmod +x deploy-local.sh
./deploy-local.sh
```

## Available Scripts

### 1. `redeploy-site.sh` - Full deployment with Git update
- Pulls latest code from GitHub
- Installs dependencies
- Restarts service
- **Requires Git access**

### 2. `deploy-local.sh` - Local deployment
- Uses current code (no Git update)
- Installs dependencies
- Restarts service
- **Works without Git access**

### 3. `run-test.sh` - Run tests
- Sets up test environment
- Runs all unit tests
- **Always works locally**

### 4. `fix-git-remote.sh` - Fix Git configuration
- Changes SSH to HTTPS
- Tests Git access
- **One-time setup**

## Common Issues and Solutions

### Issue: Virtual Environment Not Found
```bash
# Recreate virtual environment
cd /root/flask-portfolio
python3 -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
```

### Issue: MySQL Not Running
```bash
# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Check status
sudo systemctl status mysql
```

### Issue: Service Won't Start
```bash
# Check service logs
sudo journalctl -u myportfolio -n 50

# Test app manually
cd /root/flask-portfolio
source python3-virtualenv/bin/activate
python app/__init__.py
```

### Issue: Port Already in Use
```bash
# Find what's using port 5001
sudo netstat -tulpn | grep :5001

# Kill the process if needed
sudo kill -9 <PID>
```

## Quick Start Commands

### First Time Setup
```bash
cd /root/flask-portfolio
chmod +x *.sh
./fix-git-remote.sh  # Fix Git if needed
./deploy-local.sh    # Deploy the app
```

### Regular Deployment
```bash
cd /root/flask-portfolio
./redeploy-site.sh   # If Git works
# OR
./deploy-local.sh    # If no Git access
```

### Testing
```bash
cd /root/flask-portfolio
./run-test.sh
```

### Check App Status
```bash
# Check service
sudo systemctl status myportfolio

# Check logs
sudo journalctl -u myportfolio -f

# Test manually
curl http://localhost:5001
```

## Next Steps

1. **Fix Git access**: Run `./fix-git-remote.sh`
2. **Deploy app**: Run `./deploy-local.sh`
3. **Test everything**: Run `./run-test.sh`
4. **Access your site**: `http://your-domain:5001`

The app should create database tables automatically when it starts!
