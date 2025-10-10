# shōmei v1.0.1 - Documentation & Code Cleanup -- 10th Oct. 2025

### what's changed?

### documentation updates

- **updated README.md** - added new features (input validation, auto-README generation)
- **updated example session** - shows confirmation prompt and README creation steps
- **updated docs.html** - added `--version` flag, updated "how it works" section

### no breaking changes

- this is a documentation and cleanup release
- all functionality from v1.0.0 works the same

---

# shōmei v1.0.0 - First Stable Release! -- 10th Oct. 2025

### what's changed?

### input validation

- **repository name validation**
- **token format validation**
- **confirmation prompts**

### automatic README.md generation

- every mirrored repository now gets a **beautiful README**.

This means **every user becomes a promoter** of shōmei! :)

### Arch changes

- **cli.py** reduced from 570 to 223 lines
- split into 6 modules (validators, git_utils, github_api, readme_generator)
- easy for new contributors to understand and extend

### new features

- `--version` flag to check your shōmei version

### code quality

- removed 97 lines of dead code
- a bit more maintainable codebase

## breaking Cchanges

- nada

### installation

```bash
pip install shomei
```

### quick start

```
cd ~/work/your-repo
shomei
```

---

# shōmei v0.3.2 - Data parsing patch -- 9th Oct. 2025

## fix: v0.3.2 - date parsing error fixed a bug where shomei crashed with a ValueError when parsing commit dates.

the date parsing logic was doing an extra split that left just the year instead of the full datetime. what changed:

- removed the bad .split('-')[0] that was breaking things
- dates now parse correctly

---

# shōmei v0.3.1 - CI/CD patch -- 9th Oct. 2025

## what's changed

just a simple patch to fix the CI/CD and a quick cleanup of the `docs/` folder.

### fixes

- **Fixed CI/CD** - Unified workflow would cause errors
- **New conditions for Release workflow** - Only runs when pushing to main, meaning, when a PR is merged
- **New conditions for Deploy workflow** - Deploy to GH pages only when changes were made in the `/docs` folder and pushed to main

---

# shōmei v0.3.0 - big refactor -- 9th Oct. 2025

## what's changed

this is a complete architectural overhaul. shōmei is now way simpler, faster, and more reliable.

### new features

- **GitHub API-based workflow** - everything via API
- **dry-run mode** (`--dry-run`) - preview before you commit (pun intended)
- **private repo support** (`--private` flag) - create private mirror repos
- **progress indicators** - beautiful progress bars showing real-time status
- **better error handling** - clear messages with actionable suggestions
- **rate limiting** - automatic delays to respect GitHub's API
- **proper branch refs** - commits now form a proper chain (fixes orphaned commits bug)

### changes

- **single command** - just run `shomei`, no more `init`/`analyze`/`process`
- **interactive prompts** - asks for everything step by step
- **70% less code** - went from ~1000 lines to ~330 lines in cli.py
- **better UX** - I think that at least, if you think I'm wrong, feel free to contribute

### à la poubelle

- **config files** - no more `config.yml`, everything is interactive through the terminal
- **local git manipulation** - no more creating sanitized repos locally
- **complex commands** - removed `init`, `analyze`, `process`, `logo`, `contribute`
- **dependencies** - removed GitPython, PyYAML, colorama (not needed!!!)

### fixes

- **orphaned commits bug** - commits now properly update branch refs
- **API timeout handling** - graceful network error handling
- **empty repo handling** - better error messages
- **GitHub API errors** - clearer messages with help

### Documentation

- **rewrote README**
- **new CONTRIBUTING.md**
- **modernized docs site** - separated CSS/JS, I'll come back to this later

### Breaking Changes

**yes, this is a breaking release.** v0.3.0 works completely differently than v0.2.x.

**old way (v0.2.x):**

```bash
cd /path/to/repo

shomei init
shomei analyze /path/to/repo
shomei process /path/to/repo
```

new way (v0.3.0):

```bash
cd /path/to/repo
shomei
```

---

# Release v0.2.5 -- 22nd Aug. 2025

### What's New in v0.2.5

- Automated release from GitHub Actions
- Package published to PyPI
- All tests passed successfully

### Installation

```
pip install shomei
```

### What's Changed

- Initial release of shōmei CLI tool
- Safe repository sanitization for GitHub contributions
- IP protection without losing contribution history

---
