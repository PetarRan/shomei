"""
shōmei - a CLI tool that safely updates your personal github graph to reflect
the work you did from another github account, without ever exposing proprietary
code or IP.

transforms your commits into safe, sanitized commits, and publishes them to your
personal github profile, so your contribution graph reflects your real effort.
"""

__version__ = "1.1.0"
__author__ = "shomei contributors"
__description__ = "update your personal github graph to reflect the work you did"

# Expose key functions for programmatic use
from .validators import validate_repo_name, validate_github_token, validate_github_username
from .git_utils import get_git_user_email, get_repo_name, get_commits_by_author
from .github_api import (
    create_github_repo,
    get_main_branch_sha,
    create_empty_commit,
    update_branch_ref,
    update_repo_readme
)
from .readme_generator import create_readme_content

__all__ = [
    # validators
    'validate_repo_name',
    'validate_github_token',
    'validate_github_username',
    # git utilities
    'get_git_user_email',
    'get_repo_name',
    'get_commits_by_author',
    # github api
    'create_github_repo',
    'get_main_branch_sha',
    'create_empty_commit',
    'update_branch_ref',
    'update_repo_readme',
    # readme generator
    'create_readme_content',
]
