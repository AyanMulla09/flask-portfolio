#!/usr/bin/env python3
"""
Simple test runner for the Flask portfolio application.
This script sets up the testing environment properly and runs all tests.
"""
import subprocess
import sys
import os

def run_tests():
    """Run the test suite with proper environment setup."""
    # Set the testing environment variable
    env = os.environ.copy()
    env['TESTING'] = 'true'
    
    # Run the tests using the test file directly
    cmd = [sys.executable, '-m', 'app.tests.test_app']
    
    try:
        result = subprocess.run(cmd, env=env, cwd=os.path.dirname(__file__), 
                              capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
