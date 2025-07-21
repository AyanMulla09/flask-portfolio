#!/bin/bash

# This script is used to run tests for the Flask portfolio application
# Navigate to the project directory
cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

# Activate virtual environment and run tests
/root/flask-portfolio/python3-virtualenv/bin/python -m unittest discover -s app/tests -v || {
    echo "Error: Tests failed"
    exit 1
}

echo "All tests passed successfully!"