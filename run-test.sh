#!/bin/bash

# This script is used to run tests for the Flask portfolio application
echo "Running Flask Portfolio Tests..."

# Navigate to the project directory
cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

# Set testing environment variable
export TESTING=true

# Activate virtual environment and run tests
echo "Activating virtual environment..."
source /root/flask-portfolio/python3-virtualenv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

echo "Running tests..."
/root/flask-portfolio/python3-virtualenv/bin/python -m unittest discover -s app/tests -v || {
    echo "Error: Tests failed"
    exit 1
}

echo "All tests passed successfully!"