# Portfolio App Systemd Service Setup Guide

## Overview
This guide will help you set up your Flask portfolio app as a systemd service that:
- Automatically starts on system boot
- Restarts if the app crashes
- Creates database tables automatically
- Runs in the background without tmux

## Prerequisites
1. MySQL server installed and running
2. Python virtual environment set up at `/root/flask-portfolio/python3-virtualenv`
3. Portfolio code at `/root/flask-portfolio`

## Setup Steps

### 1. Set up MySQL Database
Run the database setup script:
```bash
cd /root/flask-portfolio
chmod +x setup_database.sh
./setup_database.sh
```

This will create:
- Database: `myportfoliodb`
- User: `myportfolio` with password `mypassword`

### 2. Install Systemd Service
```bash
# Copy service file to systemd directory
sudo cp myportfolio.service /etc/systemd/system/

# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable myportfolio

# Start the service
sudo systemctl start myportfolio
```

### 3. Check Service Status
```bash
# Check if service is running
sudo systemctl status myportfolio

# View service logs
sudo journalctl -u myportfolio -f
```

### 4. For Future Deployments
Simply run the redeploy script:
```bash
cd /root/flask-portfolio
chmod +x redeploy-site.sh
./redeploy-site.sh
```

## Database Creation
Yes, the service DOES create the database tables automatically! Here's how:

1. **App starts** → `app/__init__.py` loads
2. **Database connection** → Connects to MySQL using `.env` credentials
3. **Table creation** → `mydb.create_tables([TimelinePost], safe=True)` creates tables
4. **The `safe=True` parameter** → Only creates tables if they don't exist

## Service Configuration
The systemd service (`myportfolio.service`) is configured to:
- Run as `root` user
- Start after network is available
- Automatically restart if the app crashes
- Start on system boot
- Use the virtual environment Python interpreter

## Troubleshooting
If the service fails to start:
1. Check logs: `sudo journalctl -u myportfolio -n 50`
2. Verify MySQL is running: `sudo systemctl status mysql`
3. Check database permissions: Run `setup_database.sh` again
4. Verify virtual environment: `ls -la /root/flask-portfolio/python3-virtualenv/bin/python`
5. Test app manually: 
   ```bash
   cd /root/flask-portfolio
   source python3-virtualenv/bin/activate
   python app/__init__.py
   ```

## Access Your Site
Your portfolio will be available at: `http://your-domain:5001`

The key advantages over tmux:
- ✅ Starts automatically on system reboot
- ✅ Automatically restarts if app crashes
- ✅ Proper logging with journalctl
- ✅ Standard Linux service management
- ✅ Better resource management
