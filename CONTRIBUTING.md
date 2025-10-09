# Contributing to shōmei

hey! thanks for checking this out. we'd love your help making shōmei better 🎉

## how to contribute

there are tons of ways to help:

- 🐛 **found a bug?** open an issue
- 💡 **have an idea?** open an issue
- 📝 **improve docs?** send a PR
- ✨ **add a feature?** let's talk about it first (open an issue)
- ⭐ **just like the project?** star it on GitHub!

## getting started

### 1. fork & clone

```bash
# fork the repo on GitHub, then:
git clone https://github.com/YOUR-USERNAME/shomei.git
cd shomei
```

### 2. set up your environment

```bash
# install in development mode
pip install -e .

# test that it works
shomei --help
```

### 3. create a branch

```bash
git checkout -b feature/your-cool-idea
# or
git checkout -b fix/that-annoying-bug
```

### 4. make your changes

write code, fix bugs, improve docs - whatever you're working on!

**a few guidelines:**
- keep it simple - shōmei is intentionally minimal
- add comments for anything that's not obvious
- use a casual tone (we're not writing academic papers here)
- test your changes locally before pushing

### 5. test it

```bash
# try running shomei with --dry-run to test without making real changes
cd /some/test/repo
shomei --dry-run

# make sure help still works
shomei --help
```

we don't have automated tests yet (contributions welcome!), so just make sure things work manually.

### 6. commit your changes

```bash
git add .
git commit -m "feat: add awesome new feature"
# or
git commit -m "fix: resolve that annoying bug"
```

**commit message format:**
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `chore:` for maintenance stuff

keep it casual but clear.

### 7. push & create a PR

```bash
git push origin feature/your-cool-idea
```

then go to GitHub and open a pull request. explain what you changed and why.

## code style

we're pretty relaxed about code style, but:

- use lowercase function/variable names with underscores: `get_commits_by_author()`
- add comments for complex logic
- keep functions short and focused
- use type hints if you want (but not required)
- **keep the casual tone in comments and docs**

basically: if it looks like the rest of the codebase, you're good.

## what we're looking for

some ideas if you want to contribute but don't know where to start:

### easy wins
- improve error messages
- add more examples to the README
- fix typos or unclear docs
- add validation for user inputs

### medium stuff
- add tests (we need these!)
- improve the GitHub API error handling
- add a `--version` flag
- support for GitLab/Bitbucket

### big ideas
- web UI for non-technical users
- OAuth flow instead of personal access tokens
- scheduled syncing (keep repos in sync automatically)
- analytics/stats on your commit patterns
- support for multiple work accounts

if you want to work on something big, **open an issue first** so we can discuss it. don't want you to spend time on something that won't get merged.

## bug reports

found a bug? open an issue with:

- what you expected to happen
- what actually happened
- how to reproduce it
- your OS and Python version

**example:**
```
**Bug**: shomei crashes when repo has no commits

**Expected**: should show a message like "no commits found"
**Actual**: crashes with a TypeError

**To reproduce**:
1. create an empty git repo
2. run `shomei`
3. boom

**Environment**:
- OS: macOS 14.0
- Python: 3.11.5
- shomei: 0.3.0
```

## feature requests

want a new feature? open an issue with:

- what problem it solves
- how you imagine it working
- any examples or mockups

we're open to ideas, but keep in mind: shōmei is intentionally simple. if a feature adds too much complexity, we might say no. but we'll always explain why!

## questions?

not sure about something? just ask! open an issue with your question. there are no stupid questions.

## code of conduct

just be cool:
- be respectful
- be helpful
- be patient
- don't be a jerk

that's it. we're all here to build something useful.

## license

by contributing, you agree that your contributions will be licensed under the MIT License.

---

thanks for contributing! every bit helps, whether it's code, docs, bug reports, or just spreading the word.

if you're stuck or have questions, open an issue or reach out. we're friendly, promise 😊
