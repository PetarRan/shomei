# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2] - 2025-10-10

### Fixed
- date parsing bug that caused ValueError when running shomei
- was splitting the date string wrong, ended up with just "2025" instead of the full datetime

## [0.3.0] - 2025-10-09

### Major Simplification - Complete Rewrite!

this release is a complete architectural overhaul. shōmei is now much simpler, faster, and more reliable.

### Added
- **GitHub API-based workflow** - no more local git manipulation, everything happens via API
- **dry-run mode** (`--dry-run`) - preview what would happen before actually doing it
- **private repo support** (`--private` flag) - create private mirror repos
- **progress indicators** - beautiful progress bars and status updates
- **better error handling** - clear error messages with suggestions
- **rate limiting** - automatic delays to respect GitHub's API limits
- **branch reference updates** - commits now properly form a chain (fixes orphaned commits bug)

### Changed
- **single command interface** - just run `shomei`, no more `init`, `analyze`, `process` commands
- **interactive prompts** - asks for everything you need, step by step
- **simplified codebase** - went from ~1000 lines across multiple files to ~330 lines in cli.py
- **casual, friendly tone** - comments and messages are more approachable
- **better UX** - uses rich panels, progress bars, and colored output

### Removed
- **configuration files** - no more `config.yml`, everything is interactive now
- **local git manipulation** - no more creating sanitized repos locally
- **complex commands** - removed `init`, `analyze`, `process`, `logo`, `contribute`
- **dependencies** - removed GitPython, PyYAML, colorama (only need click, requests, rich now)

### Fixed
- **orphaned commits bug** - commits now properly update branch refs
- **empty repo handling** - better error messages when no commits found
- **API timeout handling** - graceful handling of network issues
- **GitHub API errors** - clearer error messages with actionable advice

### Documentation
- **completely rewritten README** - casual, friendly tone with examples
- **new CONTRIBUTING.md** - clear guide for contributors
- **updated docs website** - coming in next update

### Breaking Changes
- **no backward compatibility** - v0.3.0 works completely differently than v0.2.x
- **removed commands** - `shomei init`, `shomei analyze`, etc. no longer exist
- **no config files** - if you had a `~/.shomei/config.yml`, it's not used anymore
- **new workflow** - just run `shomei` from any git repo, follow the prompts

### Migration from v0.2.x

if you were using v0.2.x, here's how to migrate:

**old way:**
```bash
shomei init
shomei analyze /path/to/repo
shomei process /path/to/repo
```

**new way:**
```bash
cd /path/to/repo
shomei
```

that's it! much simpler.

### Why the big change?

the old architecture was overengineered. it tried to do too much: config files, local repo sanitization, multiple commands, etc. most users just wanted one thing: mirror my commits to GitHub.

v0.3.0 does exactly that, and nothing more. it's faster, simpler, and harder to mess up.

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
