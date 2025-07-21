#!/bin/bash

# MySQL Database Setup Script for Portfolio App
echo "Setting up MySQL database for portfolio app..."

# Create database and user (run as MySQL root)
mysql -u root -p << EOF
CREATE DATABASE IF NOT EXISTS myportfoliodb;
CREATE USER IF NOT EXISTS 'myportfolio'@'localhost' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON myportfoliodb.* TO 'myportfolio'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "MySQL database setup completed!"
echo "Database: myportfoliodb"
echo "User: myportfolio" 
echo "The Flask app will automatically create the tables when it starts."
