#!/usr/bin/env python3
"""
shōmei - mirror your work commits to personal GitHub without leaking IP.
super simple, super safe.
"""

import time
from datetime import timezone
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from . import __version__
from .art import print_logo
from .validators import validate_repo_name, validate_github_token, validate_github_username
from .git_utils import get_git_user_email, get_repo_name, get_commits_by_author, get_git_user_name
from .github_api import (
    check_repo_exists,
    create_github_repo,
    get_main_branch_sha,
    create_empty_commit,
    update_branch_ref,
    update_repo_readme
)
from .readme_generator import create_readme_content

console = Console()


@click.command()
@click.option('--private', is_flag=True, help='make the mirror repo private')
@click.option('--dry-run', is_flag=True, help='preview what would happen without actually doing it')
@click.version_option(version=__version__, prog_name='shōmei')
def cli(private, dry_run):
    """
    shōmei - proof of your work

    mirrors your corporate commits to personal GitHub.
    no code, no secrets, just green squares.

    run this from inside any git repo where you've been committing with your
    work email, and it'll create a matching commit history on your personal
    GitHub. your contribution graph gets updated, recruiters stop thinking
    you've been on vacation for a year, everyone's happy.
    """
    # show the logo because it looks sick
    print_logo()

    # figure out where we are
    corporate_email = get_git_user_email()
    if not corporate_email:
        console.print("[red]!!! no git user found. are you in a git repo?[/red]")
        console.print("[dim]try: git config user.email[/dim]")
        return
    
    git_name = get_git_user_name()
    if not git_name:
        console.print("[red]!!! no git user name found. are you in a git repo?[/red]")
        console.print("[dim]try: git config user.name[/dim]")
        return

    repo_name = get_repo_name()

    console.print(f"Hello, [bold]{git_name}[/bold] :wave:\n")
    console.print(f"[bold cyan]current git email:[/bold cyan] {corporate_email}")
    console.print(f"[bold cyan]current repo:[/bold cyan] {repo_name}")
    console.print()
     
    personal_username = None
    while True:
        username = click.prompt("Your personal GitHub username")
        valid, message = validate_github_username(username)

        if not valid:
            console.print(f"[red]{message}[/red]")
            console.print("[dim]Please try again[/dim]\n")
            continue

        console.print(f"[green]{message}[/green]\n")

        if click.confirm(f"Username: {username}, is that correct?", default=True):
            personal_username = username
            break

    # get repo name with validation
    suggested_name = f"{repo_name}-mirror"
    mirror_repo_name = None
    while not mirror_repo_name:
        repo_input = click.prompt("what should we call the mirror repo?", default=suggested_name)
        valid, error = validate_repo_name(repo_input)
        if valid:
            mirror_repo_name = repo_input.strip()
        else:
            console.print(f"[red]x {error}[/red]")
            console.print("[dim]repo names can only contain letters, numbers, hyphens, underscores, and periods[/dim]\n")

    if dry_run:
        console.print("\n[yellow]! DRY RUN MODE - nothing will actually be created ![/yellow]\n")
        token = "dry-run"  # placeholder for dry run
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

    console.print()

    # get all commits by this email
    with console.status("[bold cyan]🔍 scanning commit history...[/bold cyan]"):
        commits = get_commits_by_author(corporate_email)

    if not commits:
        console.print("[yellow]!!! no commits found for your email in this rep !!![/yellow]")
        console.print(f"[dim]make sure you have commits with {corporate_email}[/dim]")
        return

    console.print(f"[green]✨ found {len(commits)} commits by you[/green]\n")

    # show preview and ask for confirmation
    date_start = commits[-1]['date'].strftime('%Y-%m-%d')
    date_end = commits[0]['date'].strftime('%Y-%m-%d')

    console.print(Panel.fit(
        f"[bold]ready to create:[/bold]\n"
        f"• repo: github.com/{personal_username}/{mirror_repo_name}\n"
        f"• commits: {len(commits)} empty commits\n"
        f"• visibility: {'private' if private else 'public'}\n"
        f"• date range: {date_start} to {date_end}",
        title="Summary",
        border_style="cyan"
    ))

    if dry_run:
        console.print("\n[yellow]DRY RUN MODE - nothing will actually be created[/yellow]")
        console.print("[dim]run without --dry-run to actually do it[/dim]")
        return

    # ask for confirmation
    if not click.confirm("\nproceed with creating the mirror repo?", default=True):
        console.print("[yellow]operation cancelled[/yellow]")
        return

    console.print()

    console.print("[cyan]checking if repository exists...[/cyan]")
    exists, has_access, error = check_repo_exists(personal_username, mirror_repo_name, token)

    if exists and has_access:
        console.print(f"[green]✓ found existing repo: github.com/{personal_username}/{mirror_repo_name}[/green]")
        console.print("[dim]will add commits to the existing repository[/dim]\n")
    elif exists and not has_access:
        console.print(f"[red]!!! repository exists but your token doesn't have access to it[/red]")
        console.print(f"[yellow]make sure your token has access to github.com/{personal_username}/{mirror_repo_name}[/yellow]")
        return
    else:
        console.print("[cyan]repository doesn't exist, creating it...[/cyan]")
        if not create_github_repo(personal_username, mirror_repo_name, token, private):
            return

        # GH rate limit, wait for it to catch up
        time.sleep(2)

    # get the initial branch SHA
    parent_sha = get_main_branch_sha(personal_username, mirror_repo_name, token)

    # create all the commits
    console.print(f"\n[cyan]creating {len(commits)} empty commits...[/cyan]")

    success_count = 0
    failed_commits = []

    # sort commits chronologically (oldest first)
    # ensure all datetimes are timezone-aware to avoid comparison errors
    commits_sorted = sorted(
        commits,
        key=lambda x: x['date'].astimezone(timezone.utc) if x['date'].tzinfo else x['date'].replace(tzinfo=timezone.utc)
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("mirroring commits...", total=len(commits_sorted))

        for i, commit in enumerate(commits_sorted):
            new_sha, error = create_empty_commit(
                personal_username,
                mirror_repo_name,
                commit['date'],
                token,
                parent_sha
            )

            if new_sha:
                # update the branch to point to this new commit
                if update_branch_ref(personal_username, mirror_repo_name, token, new_sha):
                    parent_sha = new_sha  # this becomes the parent for the next commit
                    success_count += 1
                else:
                    failed_commits.append((i, error or "couldn't update branch"))
            else:
                failed_commits.append((i, error or "unknown error"))

            progress.update(task, advance=1)

            # be nice to GitHub's API (rate limiting)
            if i % 10 == 0 and i > 0:
                time.sleep(1)

    # create a rich README for the repo
    console.print("\n[cyan]creating README.md...[/cyan]")
    readme_content = create_readme_content(
        username=personal_username,
        repo_name=mirror_repo_name,
        num_commits=success_count,
        date_range_start=date_start,
        date_range_end=date_end,
        original_repo=repo_name
    )

    readme_created = update_repo_readme(personal_username, mirror_repo_name, token, readme_content)
    if readme_created:
        console.print("[green]README created[/green]")
    else:
        console.print("[yellow]couldn't create README (you can add it manually)[/yellow]")

    # show results
    console.print()
    if success_count == len(commits):
        console.print(Panel.fit(
            f"[bold green]SUCCESS![/bold green]\n\n"
            f"mirrored {success_count} commits to your personal GitHub.\n"
            f"check it out: [link=https://github.com/{personal_username}/{mirror_repo_name}]github.com/{personal_username}/{mirror_repo_name}[/link]\n\n"
            f"[dim]your contribution graph should update in a few minutes[/dim]",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            f"[bold yellow]PARTIAL SUCCESS[/bold yellow]\n\n"
            f"created {success_count}/{len(commits)} commits\n"
            f"failed: {len(failed_commits)} commits\n\n"
            f"repo: [link=https://github.com/{personal_username}/{mirror_repo_name}]github.com/{personal_username}/{mirror_repo_name}[/link]",
            border_style="yellow"
        ))

        if failed_commits and len(failed_commits) < 10:
            console.print("\n[dim]failed commits:[/dim]")
            for idx, error in failed_commits[:5]:
                console.print(f"[dim]  • commit {idx + 1}: {error}[/dim]")


if __name__ == '__main__':
    cli()
