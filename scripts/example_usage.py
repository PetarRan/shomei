#!/usr/bin/env python3
"""
Example usage of shōmei programmatically.
"""

import sys
from pathlib import Path

# Add the shomei package to the path
sys.path.insert(0, str(Path(__file__).parent))

def example_basic_usage():
    """Example of basic usage."""
    print("🚀 Example: Basic shōmei Usage\n")
    
    try:
        from shomei.config import Config
        from shomei.core import ShomeiProcessor
        
        # Create configuration
        config = Config()
        config.personal_name = "John Doe"
        config.personal_email = "john.doe@personal.com"
        config.placeholder_text = "[SANITIZED] Corporate content removed"
        
        print(f"Configuration created:")
        print(f"  Name: {config.personal_name}")
        print(f"  Email: {config.personal_email}")
        print(f"  Placeholder: {config.placeholder_text}")
        
        # Validate config
        if config.is_valid():
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration is invalid")
        
        print("\nTo use with a repository:")
        print("  processor = ShomeiProcessor('/path/to/repo', config)")
        print("  processor.analyze()  # See what would be processed")
        print("  processor.process()  # Actually process the repo")
        
    except ImportError as e:
        print(f"❌ Could not import shomei: {e}")
        print("Make sure you've installed the package: pip install -e .")

def example_config_management():
    """Example of configuration management."""
    print("\n⚙️  Example: Configuration Management\n")
    
    try:
        from shomei.config import Config
        from shomei.utils import get_default_config_path
        
        # Show default config path
        config_path = get_default_config_path()
        print(f"Default config path: {config_path}")
        
        # Create and save config
        config = Config()
        config.personal_name = "Jane Smith"
        config.personal_email = "jane.smith@example.com"
        config.keep_branches = ["main", "develop"]
        config.strip_file_extensions = [".py", ".js", ".java"]
        
        print(f"\nConfig created with custom settings:")
        print(f"  Keep branches: {config.keep_branches}")
        print(f"  Strip extensions: {config.strip_file_extensions}")
        
        # Save to custom path
        custom_path = Path("example_config.yml")
        config.save(str(custom_path))
        print(f"✅ Config saved to: {custom_path}")
        
        # Load from file
        loaded_config = Config(str(custom_path))
        print(f"✅ Config loaded from: {custom_path}")
        print(f"  Loaded name: {loaded_config.personal_name}")
        
        # Clean up
        custom_path.unlink()
        print(f"✅ Cleaned up example config")
        
    except Exception as e:
        print(f"❌ Configuration example failed: {e}")

def example_git_operations():
    """Example of Git operations."""
    print("\n🔧 Example: Git Operations\n")
    
    try:
        from shomei.git_utils import GitUtils
        
        print("Git utilities provide methods for:")
        print("  - Getting repository information")
        print("  - Analyzing commits by author")
        print("  - Checking branch and tag status")
        print("  - Validating Git installation")
        
        print("\nTo use with a repository:")
        print("  git_utils = GitUtils(Path('/path/to/repo'))")
        print("  info = git_utils.get_repository_info()")
        print("  print(f'Total commits: {info[\"total_commits\"]}')")
        
    except Exception as e:
        print(f"❌ Git operations example failed: {e}")

def main():
    """Run all examples."""
    print("📚 shōmei Usage Examples\n")
    print("=" * 50)
    
    examples = [
        example_basic_usage,
        example_config_management,
        example_git_operations,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"❌ Example failed: {e}")
        
        print("\n" + "=" * 50)
    
    print("\n🎯 To run the actual CLI tool:")
    print("  shomei init                    # Setup configuration")
    print("  shomei analyze /path/to/repo   # Analyze repository")
    print("  shomei process /path/to/repo   # Process repository")

if __name__ == "__main__":
    main()
