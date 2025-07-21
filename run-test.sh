#!bin/bash

# This script is used to run tests for the Flask portfolio application
$PWD/python3-virtualenv/bin/python -m unittest discover -v /tests || {
    echo "Error: Tests failed"
    exit 1
}