"""
Configuration management for shōmei.
"""

import yaml
from pathlib import Path
from typing import Optional


class Config:
    """Configuration class for shōmei settings."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.personal_name: Optional[str] = None
        self.personal_email: Optional[str] = None
        self.placeholder_text: str = "[STRIPPED] Corporate content removed for privacy"
        self.keep_branches: list = ["main", "master"]
        self.strip_file_extensions: list = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".php"]
        self.preserve_file_extensions: list = [".md", ".txt", ".yml", ".yaml", ".json", ".gitignore"]
        
        if config_path:
            self.load(config_path)
    
    def load(self, config_path: str) -> None:
        """Load configuration from file."""
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    self.personal_name = config_data.get('personal_name')
                    self.personal_email = config_data.get('personal_email')
                    self.placeholder_text = config_data.get('placeholder_text', self.placeholder_text)
                    self.keep_branches = config_data.get('keep_branches', self.keep_branches)
                    self.strip_file_extensions = config_data.get('strip_file_extensions', self.strip_file_extensions)
                    self.preserve_file_extensions = config_data.get('preserve_file_extensions', self.preserve_file_extensions)
        except FileNotFoundError:
            pass  # Use defaults if file doesn't exist
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")
    
    def save(self, config_path: str) -> None:
        """Save configuration to file."""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_data = {
            'personal_name': self.personal_name,
            'personal_email': self.personal_email,
            'placeholder_text': self.placeholder_text,
            'keep_branches': self.keep_branches,
            'strip_file_extensions': self.strip_file_extensions,
            'preserve_file_extensions': self.preserve_file_extensions,
        }
        
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
    
    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return bool(self.personal_name and self.personal_email)
    
    def should_strip_file(self, filename: str) -> bool:
        """Determine if a file should have its contents stripped."""
        if not filename:
            return False
        
        # Check if file should be preserved
        for ext in self.preserve_file_extensions:
            if filename.endswith(ext):
                return False
        
        # Check if file should be stripped
        for ext in self.strip_file_extensions:
            if filename.endswith(ext):
                return True
        
        # Default to stripping unknown file types
        return True
