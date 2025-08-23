# shōmei

> update your github contribution graph to reflect the work you actually did while working from another account

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**shōmei** (証明) is a CLI tool that safely updates your personal github graph to reflect the work you did from a corp github account, without ever exposing proprietary code or company IP.

transforms your commits into safe, sanitized commits, and publishes them to your personal github profile, so your contribution graph reflects your real effort.

**Showcase your contributions without leaking your company's IP.**

## the problem

i'm sure by now you've seen posts like this floating around the web. 

many developers don't use their personal github at work, and when they leave a company and start applying elsewhere, it can look like they didn't do anything the past year, at least to some recruiters. let's be honest, most devs don't really care about this stuff, and it doesn't prove your competency in any real sense, especially since it can easily be faked. this tool is just for those who want to keep everything in order and show that they were active while working from another account.

**shōmei solves this by safely updating your activity graph to reflect your previous work.**

## features

- **IP protection**: replaces all source code with safe placeholders 
- **contribution showcase**: rewrites commits to reflect your personal work
- **smart filtering**: only processes your own commits

## quick start

**🌐 Website**: Visit [petarran.github.io/shomei](https://petarran.github.io/shomei) for the full documentation site with interactive examples and installation guides.

### installation

**From Homebrew (macOS/Linux):**
```bash
# Add our tap and install
brew tap petarran/shomei
brew install shomei
```

**From PyPI (recommended):**
```bash
pip install shomei
```

**One-command Linux install:**
```bash
curl -sSL https://raw.githubusercontent.com/petarran/shomei/main/scripts/install.sh | bash
```

**From source:**
```bash
git clone https://github.com/petarran/shomei.git
cd shomei
make install-user  # or: pip install -e .
```

### first run

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

## usage

### commands

#### `shomei init`
initialize your configuration file with personal details.

```bash
shomei init
# prompts for:
# - Personal name for commits
# - Personal email for commits
# Shows welcome message and contributing info
```

#### `shomei contribute`
Show information about contributing to shōmei.

#### `shomei analyze <repo_path>`
analyze a repository to show what would be processed.

```bash
shomei analyze /path/to/repo
# shows:
# - commit analysis by author
# - files that will be stripped/preserved
# - repository statistics
```

#### `shomei process <repo_paths...>`
process one or more repositories and create sanitized versions.

```bash
# process current directory
shomei process

# process specific repositories
shomei process /path/to/repo1 /path/to/repo2

# dry run (preview only)
shomei process --dry-run /path/to/repo

# override personal details
shomei process --personal-email "you@example.com" --personal-name "Your Name" /path/to/repo
```

### options

- `--dry-run`: Preview changes without applying them
- `--personal-email`: Override personal email from config
- `--personal-name`: Override personal name from config
- `--placeholder-text`: Custom text to replace file contents
- `--output-dir`: Specify output directory for sanitized repo
- `--verbose`: Enable verbose logging
- `--config`: Path to configuration file

## configuration

Configuration is stored in `~/.shomei/config.yml`:

```yaml
personal_name: "Your Name"
personal_email: "you@example.com"
placeholder_text: "[STRIPPED] Corporate content removed for privacy"
keep_branches: ["main", "master"]
strip_file_extensions: [".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".php"]
preserve_file_extensions: [".md", ".txt", ".yml", ".yaml", ".json", ".gitignore"]
```

## how it works

### step 1: repository detection
- verifies `.git` folder exists
- supports multi-repo mode

### step 2: git user detection
- auto-reads `git config user.name` and `git config user.email`
- prompts for confirmation/change

### step 3: commit filtering
- only keeps commits authored by your corporate email
- uses GitPython for robust filtering

### step 4: commit rewriting
- replaces author/committer with your personal info
- optionally sanitizes commit messages

### step 5: content stripping
- replaces every file with `placeholder.txt`
- prevents any corporate IP from leaving the machine

### step 6: cleanup
- keeps only main/master branch
- deletes all other branches and tags

### step 7: output
- creates sanitized repository ready for personal use
- safe to push to public GitHub

## safety features

- **Content Stripping**: all source code is replaced with placeholder text
- **Author Filtering**: only processes your own commits
- **Dry Run Mode**: preview all changes before applying
- **Temporary Processing**: works on copies, never modifies originals
- **Configurable File Types**: choose what gets stripped vs. preserved

## requirements

- Python 3.10+
- Git installed and accessible
- Dependencies: GitPython, Click, Rich, PyYAML

## package distribution

### automated releases

this project uses GitHub Actions for automated releases:

1. **create a release tag:**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically:**
   - run tests on multiple Python versions
   - build distribution packages
   - publish to PyPI
   - create GitHub release with changelog

### adding to package managers

**Homebrew (macOS/Linux):**
```bash
# Add to Homebrew core or create a custom tap
# brew install petarran/shomei/shomei
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

### setup development environment

```bash
# clone and setup
git clone https://github.com/petarran/shomei.git
cd shomei

# install development dependencies
pip install -e ".[dev]"

# run tests
pytest

# format code
black shomei/

# lint code
flake8 shomei/

# type checking
mypy shomei/
```

### project structure

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

## contributing

1. fork the repository
2. create a feature branch (`git checkout -b feature/amazing-feature`)
3. commit your changes (`git commit -m 'Add amazing feature'`)
4. push to the branch (`git push origin feature/amazing-feature`)
5. open a Pull Request

## license

this project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## disclaimer

**shōmei** is designed to help developers showcase their contributions while protecting corporate IP. however:

- always review the output before pushing to ensure no sensitive information remains
- use dry-run mode to preview changes
- consider your company's policies before using this tool
- the authors are not responsible for any data leaks or policy violations

## acknowledgments

- built with [GitPython](https://gitpython.readthedocs.io/) for robust Git operations
- CLI powered by [Click](https://click.palletsprojects.com/) for excellent user experience
- beautiful output thanks to [Rich](https://rich.readthedocs.io/)

---

**made with ❤️ for developers who want to showcase their work safely.**
