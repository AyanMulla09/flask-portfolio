#!/usr/bin/env python3
import os
import sys
import unittest

# Set up test environment before importing anything
os.environ['TESTING'] = 'true'

# Now we can safely import the test module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    # Import the test module
    from app.tests.test_app import AppTestCase
    
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(AppTestCase)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
