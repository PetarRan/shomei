# shōmei (証明)

> Show off your coding contributions without leaking corporate IP

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**shōmei** is a CLI tool for developers who want to showcase their coding contributions on GitHub—without leaking any proprietary code or IP from their company.

It transforms your private commits into safe, sanitized commits, and publishes them to your personal GitHub profile—so your contribution graph reflects your real effort.

**Showcase your contributions without leaking your company's IP.**

## The Problem

Ever applied for a senior developer position only to have your GitHub contribution graph look like this?

```
[Empty contribution graph - no green squares]
```

Companies want to see your coding activity, but your corporate work is locked away in private repositories. Your GitHub profile looks inactive, even though you're coding 40+ hours a week.

**shōmei solves this by safely transforming your private commits into public contributions.**

> **Note**: Want to add your logo or screenshots? Create an `assets/` folder in your repository and reference images like `![Alt text](assets/your-image.png)`. Perfect for logos, screenshots, and visual examples.

## Features

- **IP Protection**: Replaces all source code with safe placeholders
- **Contribution Showcase**: Rewrites commits to reflect your personal work
- **Smart Filtering**: Only processes your own commits by email
- **Safe Processing**: Works on copies, never modifies originals

## Quick Start

### Installation

**From PyPI (recommended):**
```bash
pip install shomei
```

**One-command Linux install:**
```bash
curl -sSL https://raw.githubusercontent.com/yourusername/shomei/main/install.sh | bash
```

**From Homebrew (macOS/Linux):**
```bash
# Coming soon - will be available via:
# brew install shomei
```

**From source:**
```bash
git clone https://github.com/yourusername/shomei.git
cd shomei
make install-user  # or: pip install -e .
```

### First Run

```bash
# Initialize configuration with your personal details
shomei init

# Analyze a repository to see what would be processed
shomei analyze /path/to/your/repo

# Process a repository (dry run first!)
shomei process /path/to/your/repo --dry-run

# Process for real
shomei process /path/to/your/repo
```

## Usage

### Commands

#### `shomei init`
Initialize your configuration file with personal details.

```bash
shomei init
# Prompts for:
# - Personal name for commits
# - Personal email for commits
# Shows welcome message and contributing info
```

#### `shomei logo`
Display the shōmei ASCII logo.

```bash
shomei logo              # Default text style
shomei logo --style geometric  # Geometric style
```

#### `shomei contribute`
Show information about contributing to shōmei.

#### `shomei analyze <repo_path>`
Analyze a repository to show what would be processed.

```bash
shomei analyze /path/to/repo
# Shows:
# - Commit analysis by author
# - Files that will be stripped/preserved
# - Repository statistics
```

#### `shomei process <repo_paths...>`
Process one or more repositories and create sanitized versions.

```bash
# Process current directory
shomei process

# Process specific repositories
shomei process /path/to/repo1 /path/to/repo2

# Dry run (preview only)
shomei process --dry-run /path/to/repo

# Override personal details
shomei process --personal-email "you@example.com" --personal-name "Your Name" /path/to/repo
```

### Options

- `--dry-run`: Preview changes without applying them
- `--personal-email`: Override personal email from config
- `--personal-name`: Override personal name from config
- `--placeholder-text`: Custom text to replace file contents
- `--output-dir`: Specify output directory for sanitized repo
- `--verbose`: Enable verbose logging
- `--config`: Path to configuration file

## Configuration

Configuration is stored in `~/.shomei/config.yml`:

```yaml
personal_name: "Your Name"
personal_email: "you@example.com"
placeholder_text: "[STRIPPED] Corporate content removed for privacy"
keep_branches: ["main", "master"]
strip_file_extensions: [".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".php"]
preserve_file_extensions: [".md", ".txt", ".yml", ".yaml", ".json", ".gitignore"]
```

## How It Works

### Step 1: Repository Detection
- Verifies `.git` folder exists
- Supports multi-repo mode

### Step 2: Git User Detection
- Auto-reads `git config user.name` and `git config user.email`
- Prompts for confirmation/change

### Step 3: Commit Filtering
- Only keeps commits authored by your corporate email
- Uses GitPython for robust filtering

### Step 4: Commit Rewriting
- Replaces author/committer with your personal info
- Optionally sanitizes commit messages

### Step 5: Content Stripping
- Replaces every file with `placeholder.txt`
- Prevents any corporate IP from leaving the machine

### Step 6: Cleanup
- Keeps only main/master branch
- Deletes all other branches and tags

### Step 7: Output
- Creates sanitized repository ready for personal use
- Safe to push to public GitHub

## Safety Features

- **Content Stripping**: All source code is replaced with placeholder text
- **Author Filtering**: Only processes your own commits
- **Dry Run Mode**: Preview all changes before applying
- **Temporary Processing**: Works on copies, never modifies originals
- **Configurable File Types**: Choose what gets stripped vs. preserved

## Requirements

- Python 3.10+
- Git installed and accessible
- Dependencies: GitPython, Click, Rich, PyYAML

## Package Distribution

### Automated Releases

This project uses GitHub Actions for automated releases:

1. **Create a release tag:**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically:**
   - Run tests on multiple Python versions
   - Build distribution packages
   - Publish to PyPI
   - Create GitHub release with changelog

### Adding to Package Managers

**Homebrew (macOS/Linux):**
```bash
# Add to Homebrew core or create a custom tap
# brew install yourusername/shomei/shomei
```

**Chocolatey (Windows):**
```bash
# choco install shomei
```

**Scoop (Windows):**
```bash
# scoop install shomei
```

**Arch Linux (AUR):**
```bash
# yay -S shomei
```

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/yourusername/shomei.git
cd shomei

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black shomei/

# Lint code
flake8 shomei/

# Type checking
mypy shomei/
```

### Project Structure

```
shomei/
├── shomei/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # CLI entry point
│   ├── core.py          # Main processing logic
│   ├── config.py        # Configuration management
│   ├── git_utils.py     # Git utilities
│   └── utils.py         # Helper functions
├── setup.py             # Package setup
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**shōmei** is designed to help developers showcase their contributions while protecting corporate IP. However:

- Always review the output before pushing to ensure no sensitive information remains
- Use dry-run mode to preview changes
- Consider your company's policies before using this tool
- The authors are not responsible for any data leaks or policy violations

## Acknowledgments

- Built with [GitPython](https://gitpython.readthedocs.io/) for robust Git operations
- CLI powered by [Click](https://click.palletsprojects.com/) for excellent user experience
- Beautiful output thanks to [Rich](https://rich.readthedocs.io/)

---

**Made with ❤️ for developers who want to showcase their work safely.**
