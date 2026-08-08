#!/usr/bin/env python3
"""
shōmei - mirror your work commits to personal GitHub without leaking IP.
super simple, super safe.
"""

import sys
import time
from contextlib import nullcontext
from datetime import timezone
from pathlib import Path
from urllib.parse import urlsplit
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from . import __version__
from .art import print_logo
from .validators import validate_repo_name, validate_github_token, validate_github_username
from .git_utils import (
    get_git_remote_url,
    get_git_root,
    get_git_user_email,
    get_repo_name,
    get_commits_by_author,
    get_git_user_name,
)
from .github_api import (
    check_repo_exists,
    create_github_repo,
    get_main_branch_sha,
    get_mirrored_commit_dates,
    create_empty_commit,
    update_branch_ref,
    update_repo_readme
)
from .readme_generator import create_readme_content
from .sync_state import (
    SyncStateError,
    get_state_path,
    get_sync_record,
    load_state,
    mark_commit_synced,
    save_state,
)

console = Console()


def _as_utc(commit_date):
    """Make a commit date safe to compare with other Git dates."""
    if commit_date.tzinfo:
        return commit_date.astimezone(timezone.utc)
    return commit_date.replace(tzinfo=timezone.utc)


def _split_legacy_mirror_commits(commits, mirrored_dates):
    """Match old mirror timestamps without collapsing duplicate timestamps."""
    remaining_dates = list(mirrored_dates)
    new_commits = []
    already_mirrored = []

    for commit in commits:
        source_date = commit['date']
        source_utc = _as_utc(source_date).replace(microsecond=0)
        source_wall_time = source_date.replace(tzinfo=None).replace(microsecond=0)

        match_index = next(
            (
                index for index, mirrored_date in enumerate(remaining_dates)
                if (
                    _as_utc(mirrored_date).replace(microsecond=0) == source_utc
                    or _as_utc(mirrored_date).replace(tzinfo=None).replace(microsecond=0)
                    == source_wall_time
                )
            ),
            None,
        )
        if match_index is None:
            new_commits.append(commit)
        else:
            already_mirrored.append(commit)
            remaining_dates.pop(match_index)

    return new_commits, already_mirrored


def _source_repository_identity(remote_url, repo_name, repo_root):
    """Keep credentials out of the source identity stored in local state."""
    if not remote_url:
        return f"local:{repo_root or repo_name}"

    parsed_url = urlsplit(remote_url)
    if parsed_url.scheme and parsed_url.hostname:
        return f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"
    if "@" in remote_url:
        return remote_url.split("@", 1)[1]
    return remote_url


def _die(message, hint=None):
    """Print an error and exit with a non-zero status."""
    console.print(f"[red]!!! {message}[/red]")
    if hint:
        console.print(f"[dim]{hint}[/dim]")
    sys.exit(1)


@click.command()
@click.option('--private', is_flag=True, help='make the mirror repo private')
@click.option('--dry-run', is_flag=True, help='preview what would happen without actually doing it')
@click.option('-u', '--username', help='your personal GitHub username')
@click.option('-r', '--repo-name', 'mirror_repo_name', help='name for the mirror repo (default: <repo>-mirror)')
@click.option('-t', '--token', envvar='SHOMEI_GITHUB_TOKEN',
              help="GitHub personal access token (needs 'repo' scope). "
                   "can also be set via the SHOMEI_GITHUB_TOKEN env var")
@click.option('-e', '--email', help='git author email to filter commits (default: git config user.email)')
@click.option('-n', '--name', 'display_name', help='your name for the greeting (default: git config user.name)')
@click.option('-y', '--yes', is_flag=True, help='skip all confirmation prompts (assume yes)')
@click.option('--non-interactive', is_flag=True,
              help='never prompt; fail if any required value is missing. implies --yes')
@click.version_option(version=__version__, prog_name='shōmei')
def cli(private, dry_run, username, mirror_repo_name, token, email, display_name, yes, non_interactive):
    """
    shōmei - proof of your work

    mirrors your corporate commits to personal GitHub.
    no code, no secrets, just green squares.

    run this from inside any git repo where you've been committing with your
    work email, and it'll create a matching commit history on your personal
    GitHub. your contribution graph gets updated, recruiters stop thinking
    you've been on vacation for a year, everyone's happy.

    for CI / scripted use, pass everything up front, e.g.:

        shomei -u me -r work-mirror -t ghp_xxx --non-interactive
    """
    # a real terminal we can talk to, or a pipe/CI environment?
    can_prompt = sys.stdin.isatty() and not non_interactive
    # simplify output (no logo/panels/spinners) when there's no interactive terminal
    plain = non_interactive or not sys.stdout.isatty()
    # non-interactive runs never wait on a confirmation
    assume_yes = yes or non_interactive or not can_prompt

    # show the logo because it looks sick (but not when piped/scripted)
    if not plain:
        print_logo()

    # figure out where we are
    corporate_email = email or get_git_user_email()
    if not corporate_email:
        _die("no git user email found. are you in a git repo?",
             "try: git config user.email  (or pass --email)")

    git_name = display_name or get_git_user_name()
    if not git_name:
        if can_prompt:
            _die("no git user name found. are you in a git repo?",
                 "try: git config user.name  (or pass --name)")
        # a name is only cosmetic; don't block a scripted run over it
        git_name = corporate_email

    repo_name = get_repo_name()

    if plain:
        console.print(f"git email: {corporate_email}")
        console.print(f"repo: {repo_name}")
    else:
        console.print(f"Hello, [bold]{git_name}[/bold] :wave:\n")
        console.print(f"[bold cyan]current git email:[/bold cyan] {corporate_email}")
        console.print(f"[bold cyan]current repo:[/bold cyan] {repo_name}")
        console.print()

    # --- personal GitHub username ---
    if username:
        username = username.strip()
        valid, message = validate_github_username(username)
        if not valid:
            _die(message)
        if not plain:
            console.print(f"[green]{message}[/green]\n")
    elif not can_prompt:
        _die("missing personal GitHub username", "pass --username / -u")
    else:
        while True:
            candidate = click.prompt("Your personal GitHub username")
            valid, message = validate_github_username(candidate)
            if not valid:
                console.print(f"[red]{message}[/red]")
                console.print("[dim]Please try again[/dim]\n")
                continue
            console.print(f"[green]{message}[/green]\n")
            if click.confirm(f"Username: {candidate}, is that correct?", default=True):
                username = candidate.strip()
                break

    # --- mirror repo name ---
    suggested_name = f"{repo_name}-mirror"
    if mirror_repo_name:
        valid, error = validate_repo_name(mirror_repo_name)
        if not valid:
            _die(error,
                 "repo names can only contain letters, numbers, hyphens, underscores, and periods")
        mirror_repo_name = mirror_repo_name.strip()
    elif not can_prompt:
        # a sensible default is fine for scripted runs
        valid, error = validate_repo_name(suggested_name)
        if not valid:
            _die(f"could not derive a valid mirror repo name ('{suggested_name}')",
                 "pass --repo-name / -r")
        mirror_repo_name = suggested_name
    else:
        while not mirror_repo_name:
            repo_input = click.prompt("what should we call the mirror repo?", default=suggested_name)
            valid, error = validate_repo_name(repo_input)
            if valid:
                mirror_repo_name = repo_input.strip()
            else:
                console.print(f"[red]x {error}[/red]")
                console.print("[dim]repo names can only contain letters, numbers, hyphens, underscores, and periods[/dim]\n")

    # --- token ---
    if dry_run:
        if not plain:
            console.print("\n[yellow]! DRY RUN MODE - nothing will actually be created ![/yellow]\n")
        else:
            console.print("dry-run: nothing will be created")
        token = "dry-run"  # placeholder for dry run
    elif token:
        valid, error = validate_github_token(token)
        if not valid:
            _die(error)
        token = token.strip()
    elif not can_prompt:
        _die("missing GitHub token",
             "pass --token / -t or set the SHOMEI_GITHUB_TOKEN env var")
    else:
        token = None
        while not token:
            token_input = click.prompt("GitHub personal access token (needs 'repo' permissions)", hide_input=True)
            valid, error = validate_github_token(token_input)
            if valid:
                token = token_input.strip()
            else:
                console.print(f"[red]!!! {error}[/red]")
                console.print("[dim]please try again[/dim]\n")

    if not plain:
        console.print()

    # get all commits by this email
    scan_ctx = nullcontext() if plain else console.status("[bold cyan]🔍 scanning commit history...[/bold cyan]")
    with scan_ctx:
        commits = get_commits_by_author(corporate_email)

    if not commits:
        _die(f"no commits found for {corporate_email} in this repo",
             f"make sure you have commits with {corporate_email}")

    # Keep source commit hashes locally so a later invocation only mirrors
    # commits that were not completed by an earlier invocation.  The state is
    # kept per source/email/target combination because one source repository
    # can legitimately be mirrored to multiple personal repositories.
    repo_root = get_git_root()
    state_path = get_state_path(Path(repo_root) if repo_root else Path.cwd())
    source_repository = _source_repository_identity(
        get_git_remote_url(),
        repo_name,
        repo_root,
    )
    target_repository = f"{username}/{mirror_repo_name}"
    try:
        sync_state = load_state(state_path)
        sync_record = get_sync_record(
            sync_state,
            target_repository,
            source_repository,
            corporate_email,
        )
    except SyncStateError as error:
        _die(str(error))

    synced_hashes = set(sync_record["commits"])
    commits_to_mirror = [
        commit for commit in commits if commit["hash"] not in synced_hashes
    ]

    if plain:
        console.print(f"found {len(commits)} commits by {corporate_email}")
        if synced_hashes:
            console.print(
                f"already mirrored {len(synced_hashes)} commits; "
                f"{len(commits_to_mirror)} new commits to sync"
            )
    else:
        console.print(f"[green]✨ found {len(commits)} commits by you[/green]\n")
        if synced_hashes:
            console.print(
                f"[dim]already mirrored {len(synced_hashes)} commits; "
                f"{len(commits_to_mirror)} new commits to sync[/dim]\n"
            )

    # show preview and ask for confirmation
    preview_commits = commits_to_mirror or commits
    preview_dates = sorted((commit['date'] for commit in preview_commits), key=_as_utc)
    date_start = preview_dates[0].strftime('%Y-%m-%d')
    date_end = preview_dates[-1].strftime('%Y-%m-%d')

    if plain:
        if commits_to_mirror:
            console.print(
                f"plan: {len(commits_to_mirror)} new empty commits -> "
                f"github.com/{username}/{mirror_repo_name} "
                f"({'private' if private else 'public'}), {date_start} to {date_end}"
            )
        else:
            console.print(
                f"plan: already up to date -> "
                f"github.com/{username}/{mirror_repo_name} "
                f"({len(commits)} commits mirrored)"
            )
    else:
        summary = (
            f"[bold]ready to create:[/bold]\n"
            f"• repo: github.com/{username}/{mirror_repo_name}\n"
            f"• commits: {len(commits_to_mirror)} new empty commits\n"
            f"• visibility: {'private' if private else 'public'}\n"
            f"• date range: {date_start} to {date_end}"
            if commits_to_mirror
            else (
                f"[bold]nothing new to sync:[/bold]\n"
                f"• repo: github.com/{username}/{mirror_repo_name}\n"
                f"• commits: {len(commits)} already mirrored"
            )
        )
        console.print(Panel.fit(summary, title="Summary", border_style="cyan"))

    if dry_run:
        if plain:
            console.print("dry-run complete; run without --dry-run to actually do it")
        else:
            console.print("\n[yellow]DRY RUN MODE - nothing will actually be created[/yellow]")
            console.print("[dim]run without --dry-run to actually do it[/dim]")
        return

    # ask for confirmation
    if not assume_yes:
        if not click.confirm("\nproceed with creating the mirror repo?", default=True):
            console.print("[yellow]operation cancelled[/yellow]")
            return

    if not plain:
        console.print()

    console.print("[cyan]checking if repository exists...[/cyan]")
    exists, has_access, error = check_repo_exists(username, mirror_repo_name, token)

    if exists and has_access:
        console.print(f"[green]✓ found existing repo: github.com/{username}/{mirror_repo_name}[/green]")

        # Repositories created by older shōmei versions have no local state.
        # Use their generated commit timestamps once to seed the hash-based
        # state, while keeping duplicate timestamps as separate commits.
        if not synced_hashes and commits_to_mirror:
            legacy_dates = get_mirrored_commit_dates(
                username,
                mirror_repo_name,
                token,
            )
            if legacy_dates is not None:
                commits_to_mirror, legacy_commits = _split_legacy_mirror_commits(
                    commits_to_mirror,
                    legacy_dates,
                )
                if legacy_commits:
                    for commit in legacy_commits:
                        mark_commit_synced(
                            sync_state,
                            target_repository,
                            source_repository,
                            corporate_email,
                            commit['hash'],
                            commit['date'],
                            None,
                        )
                    try:
                        save_state(state_path, sync_state)
                    except SyncStateError as error:
                        _die(f"couldn't save migrated sync state: {error}")
                    console.print(
                        f"[dim]migrated {len(legacy_commits)} existing mirror commits "
                        "into local sync state[/dim]"
                    )

        if not commits_to_mirror:
            console.print("[dim]already up to date; no new commits to add[/dim]")
            return
        console.print("[dim]will add new commits to the existing repository[/dim]\n")
    elif exists and not has_access:
        _die("repository exists but your token doesn't have access to it",
             f"make sure your token has access to github.com/{username}/{mirror_repo_name}")
    else:
        console.print("[cyan]repository doesn't exist, creating it...[/cyan]")
        if not create_github_repo(username, mirror_repo_name, token, private):
            sys.exit(1)

        # GH rate limit, wait for it to catch up
        time.sleep(2)

        # A local state file can outlive a deleted mirror repository.  The
        # replacement repository has no mirrored history, so rebuild it.
        if not commits_to_mirror:
            commits_to_mirror = list(commits)

    # get the initial branch SHA
    parent_sha = get_main_branch_sha(username, mirror_repo_name, token)

    # create all the commits
    total_to_mirror = len(commits_to_mirror)
    console.print(f"\n[cyan]creating {total_to_mirror} empty commits...[/cyan]")

    success_count = 0
    failed_commits = []

    def _mirror_commit(commit):
        """Create one empty commit and advance the branch. Returns True on success."""
        new_sha, err = create_empty_commit(
            username,
            mirror_repo_name,
            commit['date'],
            token,
            parent_sha
        )
        if new_sha:
            if update_branch_ref(username, mirror_repo_name, token, new_sha):
                try:
                    mark_commit_synced(
                        sync_state,
                        target_repository,
                        source_repository,
                        corporate_email,
                        commit['hash'],
                        commit['date'],
                        new_sha,
                    )
                    save_state(state_path, sync_state)
                except SyncStateError as error:
                    _die(
                        f"mirrored commit {commit['hash'][:12]}, but couldn't persist "
                        f"sync state: {error}",
                        "the remote branch was updated; restore the state file before retrying",
                    )
                return new_sha, None
            return None, err or "couldn't update branch"
        return None, err or "unknown error"

    commits_sorted = sorted(
        commits_to_mirror,
        key=lambda x: _as_utc(x['date'])
    )

    if plain:
        # no animated progress bar for pipes/CI; emit periodic plain updates instead
        total = total_to_mirror
        for i, commit in enumerate(commits_sorted):
            new_sha, err = _mirror_commit(commit)
            if new_sha:
                parent_sha = new_sha
                success_count += 1
            else:
                failed_commits.append((i, err))

            # progress heartbeat so long runs aren't silent
            if (i + 1) % 25 == 0 or (i + 1) == total:
                console.print(f"  {i + 1}/{total} commits mirrored")

            # be nice to GitHub's API (rate limiting)
            if i % 10 == 0 and i > 0:
                time.sleep(1)
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("mirroring commits...", total=len(commits_sorted))

            for i, commit in enumerate(commits_sorted):
                new_sha, err = _mirror_commit(commit)
                if new_sha:
                    parent_sha = new_sha
                    success_count += 1
                else:
                    failed_commits.append((i, err))

                progress.update(task, advance=1)

                # be nice to GitHub's API (rate limiting)
                if i % 10 == 0 and i > 0:
                    time.sleep(1)

    # create a rich README for the repo
    console.print("\n[cyan]creating README.md...[/cyan]")
    synced_count = len(sync_record["commits"])
    source_dates = sorted((commit['date'] for commit in commits), key=_as_utc)
    readme_content = create_readme_content(
        username=username,
        repo_name=mirror_repo_name,
        num_commits=synced_count,
        date_range_start=source_dates[0].strftime('%Y-%m-%d'),
        date_range_end=source_dates[-1].strftime('%Y-%m-%d'),
        original_repo=repo_name
    )

    readme_created = update_repo_readme(username, mirror_repo_name, token, readme_content)
    if readme_created:
        console.print("[green]README created[/green]")
    else:
        console.print("[yellow]couldn't create README (you can add it manually)[/yellow]")

    # show results
    repo_url = f"github.com/{username}/{mirror_repo_name}"
    if not plain:
        console.print()
    if success_count == total_to_mirror:
        if plain:
            console.print(
                f"success: mirrored {success_count} new commits to {repo_url} "
                f"({synced_count} total)"
            )
        else:
            console.print(Panel.fit(
                f"[bold green]SUCCESS![/bold green]\n\n"
                f"mirrored {success_count} new commits to your personal GitHub.\n"
                f"{synced_count} commits mirrored in total.\n"
                f"check it out: [link=https://{repo_url}]{repo_url}[/link]\n\n"
                f"[dim]your contribution graph should update in a few minutes[/dim]",
                border_style="green"
            ))
    else:
        if plain:
            console.print(
                f"partial: created {success_count}/{total_to_mirror} new commits, "
                f"{len(failed_commits)} failed -> {repo_url}"
            )
        else:
            console.print(Panel.fit(
                f"[bold yellow]PARTIAL SUCCESS[/bold yellow]\n\n"
                f"created {success_count}/{total_to_mirror} new commits\n"
                f"failed: {len(failed_commits)} commits\n\n"
                f"repo: [link=https://{repo_url}]{repo_url}[/link]",
                border_style="yellow"
            ))

        if failed_commits and len(failed_commits) < 10:
            console.print("\n[dim]failed commits:[/dim]")
            for idx, err in failed_commits[:5]:
                console.print(f"[dim]  • commit {idx + 1}: {err}[/dim]")

        # signal failure to callers/CI
        sys.exit(1)


if __name__ == '__main__':
    cli()
