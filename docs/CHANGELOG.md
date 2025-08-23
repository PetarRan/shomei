# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CLI interface with Click
- Repository analysis and processing
- Configuration management
- Git utilities and commit filtering
- Content stripping and IP protection
- Dry-run mode for safe testing
- ASCII art and welcome messages
- Multi-repository support
- Linux installation script
- Homebrew formula support

## [0.2.5] - 2025-08-23

### Added
- Homebrew formula for easy macOS/Linux installation
- Custom tap repository setup
- Automated dependency installation in Homebrew formula

### Fixed
- Homebrew installation now properly installs all Python dependencies
- Formula includes correct SHA256 hash for v0.2.4 release

## [0.2.4] - 2025-08-22

### Added
- GitHub Pages website with modern design
- Interactive documentation site
- Copy-to-clipboard functionality for code blocks
- Responsive design for mobile and desktop
- Integration with GitHub API for star counts

### Changed
- Updated website color scheme to match brand colors
- Improved navigation and user experience
- Streamlined installation instructions

## [0.2.3] - 2025-08-22

### Added
- ASCII art logo with "shōmei" text
- Terminal welcome messages and safety reminders
- Contributing information display
- Logo command for displaying ASCII art

### Changed
- Enhanced CLI user experience with informative messages
- Improved project organization and structure

## [0.2.1] - 2025-08-22

### Added
- GitHub Actions workflow for automated releases
- PyPI publishing automation
- Automated testing on multiple Python versions
- Release workflow triggers on version tags only

### Fixed
- Resolved Python version compatibility issues in CI/CD
- Fixed PyPI authentication and release creation

## [0.2.0] - 2025-08-22

### Added
- Initial release of shōmei CLI tool
- Core functionality for repository sanitization
- CLI commands: init, analyze, process, logo, contribute
- Configuration file support
- Git operations and commit rewriting
- File content stripping with placeholders
- Branch and tag cleanup
- Multi-repository support
- Beautiful ASCII art and user experience
- Comprehensive documentation

### Technical Details
- Python 3.10+ support
- Dependencies: GitPython, Click, Rich, PyYAML
- MIT License
- GitHub Actions CI/CD
- PyPI distribution ready
