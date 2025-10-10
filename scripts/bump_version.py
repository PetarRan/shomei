#!/usr/bin/env python3
"""
Version bumping script for shōmei
Usage: python scripts/bump_version.py [patch|minor|major]
"""

import re
import sys
from pathlib import Path

def get_current_version():
    """Get current version from __init__.py"""
    init_file = Path("shomei/__init__.py")
    with open(init_file, "r") as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    raise ValueError("Could not find version in __init__.py")

def bump_version(version, bump_type):
    """Bump version according to semantic versioning"""
    parts = [int(x) for x in version.split('.')]
    
    if bump_type == "patch":
        parts[2] += 1
    elif bump_type == "minor":
        parts[1] += 1
        parts[2] = 0
    elif bump_type == "major":
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    else:
        raise ValueError("bump_type must be patch, minor, or major")
    
    return '.'.join(map(str, parts))

def update_version_file(new_version):
    """Update version in __init__.py"""
    init_file = Path("shomei/__init__.py")
    with open(init_file, "r") as f:
        content = f.read()
    
    # Replace version
    content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(init_file, "w") as f:
        f.write(content)
    
    print(f"Updated version to {new_version} in shomei/__init__.py")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/bump_version.py [patch|minor|major]")
        print("\nExamples:")
        print("  python scripts/bump_version.py patch  # 0.2.3 -> 0.2.4")
        print("  python scripts/bump_version.py minor  # 0.2.3 -> 0.3.0")
        print("  python scripts/bump_version.py major  # 0.2.3 -> 1.0.0")
        sys.exit(1)
    
    bump_type = sys.argv[1].lower()
    if bump_type not in ["patch", "minor", "major"]:
        print("Error: bump_type must be patch, minor, or major")
        sys.exit(1)
    
    try:
        current_version = get_current_version()
        new_version = bump_version(current_version, bump_type)
        
        print(f"Current version: {current_version}")
        print(f"Bumping {bump_type}: {current_version} -> {new_version}")
        
        update_version_file(new_version)
        
        print(f"\n >> Next steps:")
        print(f"1. Commit the version change: git add shomei/__init__.py && git commit -m 'Bump version to {new_version}'")
        print(f"2. Create tag: git tag -a v{new_version} -m 'Release {new_version}'")
        print(f"3. Push tag: git push origin v{new_version}")
        print(f"4. Watch GitHub Actions run!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
