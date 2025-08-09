#!/bin/bash

# This script is used to run tests for the Flask portfolio application
echo "Running Flask Portfolio Tests..."

# Get the current working directory
PROJECT_DIR="$(pwd)"
echo "Project directory: $PROJECT_DIR"

# Navigate to the project directory (we should already be there in GitHub Actions)
cd "$PROJECT_DIR" || {
    echo "Error: Could not navigate to project directory: $PROJECT_DIR"
    exit 1
}

# Set testing environment variable
export TESTING=true

# Activate virtual environment and run tests
echo "Activating virtual environment..."
if [ -f "python3-virtualenv/bin/activate" ]; then
    source python3-virtualenv/bin/activate || {
        echo "Error: Failed to activate virtual environment"
        exit 1
    }
    PYTHON_CMD="python3-virtualenv/bin/python"
else
    echo "Error: Virtual environment not found"
    exit 1
fi

echo "Running tests..."
$PYTHON_CMD -m unittest discover -s app/tests -v || {
    echo "Error: Tests failed"
    exit 1
}

echo "All tests passed successfully!"