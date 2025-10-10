"""Input validation functions for shōmei."""

import re


def validate_repo_name(name):
    r"""
    Validate GitHub repo name according to GitHub's rules.

    Args:
        name: The repository name to validate

    Returns:
        tuple: (is_valid: bool, error_message: str or None)

    Rules:
        - Can contain alphanumeric chars, hyphens, underscores, and periods
        - Cannot start with a period, slash, or hyphen
        - Must be 1-100 chars
        - Cannot contain spaces or special chars like /\[]'";:
    """
    if not name or len(name.strip()) == 0:
        return False, "repo name cannot be empty"

    name = name.strip()

    if len(name) > 100:
        return False, "repo name must be 100 characters or less"

    if name[0] in './-':
        return False, "repo name cannot start with '.', '/', or '-'"

    # check for invalid characters
    if not re.match(r'^[a-zA-Z0-9._-]+$', name):
        return False, "repo name can only contain letters, numbers, hyphens, underscores, and periods"

    return True, None


def validate_github_token(token):
    """
    Validate GitHub token format.

    Args:
        token: The GitHub personal access token to validate

    Returns:
        tuple: (is_valid: bool, error_message: str or None)

    Note:
        Prints a warning if token format is unexpected but doesn't block.
        GitHub token formats:
        - classic tokens start with 'ghp_'
        - fine-grained tokens start with 'github_pat_'
    """
    from rich.console import Console
    console = Console()

    if not token or len(token.strip()) == 0:
        return False, "token cannot be empty"

    token = token.strip()

    # GitHub token formats:
    # - classic tokens start with 'ghp_'
    # - fine-grained tokens start with 'github_pat_'
    if not (token.startswith('ghp_') or token.startswith('github_pat_')):
        console.print("[yellow]!!! warning: token doesn't match expected format (ghp_* or github_pat_*)[/yellow]")
        console.print("[dim]continuing anyway, but double-check if you get auth errors[/dim]\n")

    return True, None
