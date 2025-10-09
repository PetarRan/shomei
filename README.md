# shōmei (証明)

> your work deserves to be seen

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/shomei.svg)](https://pypi.org/project/shomei/)

**shōmei** (証明, pronounced "shoh-may") means "proof" in Japanese. because sometimes you just need proof that you weren't on vacation for the past year.

this CLI tool mirrors your corporate commits to your personal GitHub. no code, no secrets, just timestamps. your contribution graph gets the credit it deserves, and your company's IP stays safe.

![Hero](https://raw.githubusercontent.com/petarran/shomei/main/assets/hero.png)

## the problem

you've probably seen posts like this:

![problem](https://raw.githubusercontent.com/petarran/shomei/main/assets/screenshot-problem.png)

look, we all know GitHub's green squares don't define you as a developer. but when you're job hunting and your profile looks dead because you've been shipping code from a work account? that's annoying.

lots of developers use separate emails for work, and when they leave a company, their personal profile makes it look like they took a year off. recruiters don't always get it. this tool is for those times when you just want your graph to reflect reality.

**shōmei fixes this. safely.**

## features

- **zero IP leakage** - creates empty commits with just dates, no code
- **dead simple** - one command, that's it
- **contribution proof** - updates your GitHub graph to show you were actually working
- **your commits only** - filters by your email, won't touch anyone else's work
- **dry-run mode** - preview before you commit (pun intended)
- **private repos** - option to mirror to a private repo if you want

## quick start

### installation

```bash
pip install shomei
```

### usage

```bash
# go to any repo where you've been committing with your work email
cd ~/work/cool-project

# run shomei
shomei

# follow the prompts, it'll ask for:
# - your personal GitHub username
# - what to call the mirror repo
# - your GitHub personal access token

# that's it! check your contribution graph in a few minutes
```

#### example session

```bash
$ shomei

███████╗██╗  ██╗ ██████╗ ███╗   ███╗███████╗██╗
██╔════╝██║  ██║██╔═══██╗████╗ ████║██╔════╝██║
███████╗███████║██║   ██║██╔████╔██║█████╗  ██║
╚════██║██╔══██║██║   ██║██║╚██╔╝██║██╔══╝  ██║
███████║██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝

current git user: alice@bigcorp.com
current repo: awesome-app

your personal GitHub username: alicecodes
what should we call the mirror repo? (awesome-app-mirror):
GitHub personal access token (needs 'repo' permissions): [hidden]

scanning commit history...
found 247 commits by you

creating GitHub repository...
repo created: github.com/alicecodes/awesome-app-mirror

creating 247 empty commits...
mirroring commits... ━━━━━━━━━━━━━━━━━━━━━━━━ 100%

SUCCESS!

mirrored 247 commits to your personal GitHub.
check it out: github.com/alicecodes/awesome-app-mirror

your contribution graph should update in a few minutes
```

### options

```bash
# preview what would happen (no changes made)
shomei --dry-run

# create a private mirror repo
shomei --private
```

## how it works

1. scans your git log for commits with your email
2. extracts just the commit dates (nothing else!)
3. creates a new repo on your personal GitHub
4. uses GitHub's API to create empty commits with those dates
5. boom, your contribution graph now shows your real activity

**important**: no code ever leaves your machine. we only send timestamps to GitHub's API. your company's IP stays exactly where it is.

## github token setup

you'll need a GitHub personal access token with `repo` permissions:

1. go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. click "Generate new token (classic)"
3. give it a name like "shomei"
4. check the `repo` checkbox (this lets shomei create repos and commits)
5. generate and copy the token
6. use it when shomei asks for it

**pro tip**: save the token somewhere safe (like a password manager). GitHub only shows it once.

## contributing

got ideas? found a bug? want to add a feature? hell yeah, we'd love your help!

check out [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

quick version:
1. fork it
2. make your changes
3. test it
4. send a PR

we're super chill about contributions. if you're not sure about something, just open an issue and ask!

## development

```bash
# clone
git clone https://github.com/petarran/shomei.git
cd shomei

# install in dev mode
pip install -e .

# run it
shomei --help
```

## faq

**Q: Is this safe?**
A: yes. shomei only sends commit dates to GitHub's API. no code, no commit messages (beyond "work happened here"), no file names. your company's IP never touches the internet.

**Q: Will this get me in trouble?**
A: we're not lawyers, but: you're not exposing any proprietary code or information. just timestamps. that said, check your company's policies if you're worried.

**Q: Does this work with private repos?**
A: yep! use the `--private` flag to create a private mirror repo.

**Q: What if I want to delete everything later?**
A: just delete the mirror repo from GitHub. your original work repo is never touched.

**Q: Can I customize the commit messages?**
A: not yet, but that's a great idea! open an issue or PR if you want to add this.

**Q: Why not just change the git config on my work repos?**
A: because then you'd be committing to company repos with your personal email, which might break things or violate policies. shomei keeps everything separate.

## license

MIT - do whatever you want with it.

## disclaimer

shōmei is a tool to help developers showcase their work. use it responsibly:

- no company code or secrets are exposed (we only send dates)
- always check your employment agreement if you're paranoid
- the authors aren't responsible if you use this in weird ways

## credits

built with:
- [click](https://click.palletsprojects.com/) - cli magic
- [rich](https://rich.readthedocs.io/) - pretty terminal output
- [requests](https://requests.readthedocs.io/) - http for humans

---

made with love for developers who actually ship code

if this helped you, give it a star on GitHub!
