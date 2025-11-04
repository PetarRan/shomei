"""Input validation functions for shōmei."""

import re
import requests

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
    Validate GitHub token format and check if it has basic authentication.

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

    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get("https://api.github.com/user", headers=headers, timeout=10)

        if response.status_code == 401:
            return False, "token is invalid or expired"
        elif response.status_code == 403:
            # soooo here token might work but has rate limit issues, let it proceed
            console.print("[yellow]warning: rate limit exceeded or token has restrictions[/yellow]\n")
            return True, None
        elif response.status_code != 200:
            console.print(f"[yellow]warning: couldn't verify token (status {response.status_code})[/yellow]")
            console.print("[dim]continuing anyway, but you may encounter issues[/dim]\n")
            return True, None

    except requests.exceptions.Timeout:
        console.print("[yellow]warning: timeout while verifying token[/yellow]")
        console.print("[dim]continuing anyway, but you may have network issues[/dim]\n")
        return True, None
    except Exception:
        pass

    return True, None

def validate_github_username(username):
    """
    Validate whether the given username exists on GitHub.

    Args:
        username: The GitHub username to validate

    Returns:
        tuple: (exists: bool, error_message: str or None)

    Notes:
        Print a warning if given username doesn't exist but don't block.
    """
    if not username or len(username.strip()) == 0:
        return False, "username cannot be empty"

    username = username.strip()
    response = requests.get(f"https://api.github.com/users/{username}", timeout=10)
    if response.status_code == 404:
        return False, f"GitHub user '{username}' does not exist"
    elif response.status_code == 200:
        return True, f"GitHub user '{username}' exists"
    else:
        return False, f"Error checking GitHub user '{username}': {response.status_code}"
        