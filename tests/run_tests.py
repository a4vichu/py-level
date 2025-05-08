"""
Test runner for PyLevel framework
"""
import unittest
import sys
from pathlib import Path

def run_tests():
    """Run all tests"""
    # Add project root and config directory to Python path
    project_root = Path(__file__).parent.parent
    config_dir = project_root / 'config'
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(config_dir))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return non-zero exit code if tests failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 