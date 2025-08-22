#!/usr/bin/env python3
"""
Test script to verify PyPI setup for shōmei
Run this to check if your PyPI configuration is correct
"""

import os
import sys
from pathlib import Path

def check_pypi_setup():
    """Check if PyPI setup is configured correctly"""
    print("🔍 Checking PyPI setup for shōmei...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("setup.py").exists():
        print("❌ Error: Run this script from the project root directory")
        return False
    
    # Check setup.py
    print("✅ Found setup.py")
    
    # Check if package can be built
    try:
        import build
        print("✅ build package available")
    except ImportError:
        print("❌ build package not installed. Run: pip install build")
        return False
    
    # Check if twine is available
    try:
        import twine
        print("✅ twine package available")
    except ImportError:
        print("❌ twine package not installed. Run: pip install twine")
        return False
    
    # Check GitHub secrets (informational)
    print("\n📋 GitHub Repository Secrets Required:")
    print("   Name: PYPI_API_TOKEN")
    print("   Value: pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("\n   To add this secret:")
    print("   1. Go to: https://github.com/petarran/shomei/settings/secrets/actions")
    print("   2. Click 'New repository secret'")
    print("   3. Name: PYPI_API_TOKEN")
    print("   4. Value: Your PyPI API token")
    
    # Check if we can build the package
    print("\n🔨 Testing package build...")
    try:
        import subprocess
        # Just check if build command exists and can run
        result = subprocess.run([sys.executable, "-m", "build", "--help"], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print("✅ Package build system ready")
        else:
            print("❌ Package build system failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error testing build: {e}")
        return False
    
    print("\n🎯 Next Steps:")
    print("1. Add PYPI_API_TOKEN to GitHub repository secrets")
    print("2. Create a git tag: git tag -a v0.1.0 -m 'First release'")
    print("3. Push the tag: git push origin v0.1.0")
    print("4. Watch the GitHub Actions workflow run!")
    
    return True

if __name__ == "__main__":
    success = check_pypi_setup()
    sys.exit(0 if success else 1)
