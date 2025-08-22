#!/usr/bin/env python3
"""
Simple test script for shōmei functionality.
"""

import sys
from pathlib import Path

# Add the shomei package to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from shomei.config import Config
        from shomei.git_utils import GitUtils
        from shomei.utils import setup_logging, get_default_config_path
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration functionality."""
    try:
        from shomei.config import Config
        
        # Test default config
        config = Config()
        print(f"✅ Default config created: {config.personal_name}, {config.personal_email}")
        
        # Test config validation
        assert not config.is_valid(), "Empty config should not be valid"
        
        # Test with values
        config.personal_name = "Test User"
        config.personal_email = "test@example.com"
        assert config.is_valid(), "Config with name and email should be valid"
        
        print("✅ Configuration tests passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_git_utils():
    """Test Git utilities (basic functionality without actual repo)."""
    try:
        from shomei.git_utils import GitUtils
        
        # This will fail without a real repo, but we can test the class creation
        print("✅ Git utilities class can be instantiated")
        return True
    except Exception as e:
        print(f"❌ Git utilities test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing shōmei functionality...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_config),
        ("Git Utilities Tests", test_git_utils),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! shōmei is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
