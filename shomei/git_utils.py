"""
Git utilities for shōmei.
"""

import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from git import Repo


class GitUtils:
    """Utility class for Git operations."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
    
    def get_original_author(self) -> str:
        """Get the original author email from the repository."""
        try:
            # Try to get from git config first
            result = subprocess.run(
                ['git', 'config', 'user.email'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            # Fall back to the most recent commit author
            try:
                latest_commit = next(self.repo.iter_commits('HEAD', max_count=1))
                return latest_commit.author.email
            except StopIteration:
                raise ValueError("No commits found in repository")
    
    def get_original_name(self) -> str:
        """Get the original author name from the repository."""
        try:
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            # Fall back to the most recent commit author
            try:
                latest_commit = next(self.repo.iter_commits('HEAD', max_count=1))
                return latest_commit.author.name
            except StopIteration:
                raise ValueError("No commits found in repository")
    
    def get_remote_url(self) -> Optional[str]:
        """Get the remote URL for the repository."""
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def get_branch_name(self) -> str:
        """Get the current branch name."""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "main"  # Default fallback
    
    def get_all_branches(self) -> List[str]:
        """Get all branch names."""
        try:
            result = subprocess.run(
                ['git', 'branch', '--format=%(refname:short)'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def get_all_tags(self) -> List[str]:
        """Get all tag names."""
        try:
            result = subprocess.run(
                ['git', 'tag'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def get_commit_count(self, author_email: Optional[str] = None) -> int:
        """Get the total number of commits, optionally filtered by author."""
        try:
            if author_email:
                result = subprocess.run(
                    ['git', 'rev-list', '--count', 'HEAD', '--author', author_email],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
            else:
                result = subprocess.run(
                    ['git', 'rev-list', '--count', 'HEAD'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
            return int(result.stdout.strip())
        except (subprocess.CalledProcessError, ValueError):
            return 0
    
    def get_file_count(self) -> int:
        """Get the total number of files in the repository."""
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return len([line for line in result.stdout.splitlines() if line.strip()])
        except subprocess.CalledProcessError:
            return 0
    
    def is_clean_working_directory(self) -> bool:
        """Check if the working directory is clean (no uncommitted changes)."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return not result.stdout.strip()
        except subprocess.CalledProcessError:
            return False
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get comprehensive repository information."""
        return {
            'path': str(self.repo_path),
            'original_author': self.get_original_author(),
            'original_name': self.get_original_name(),
            'remote_url': self.get_remote_url(),
            'current_branch': self.get_branch_name(),
            'all_branches': self.get_all_branches(),
            'all_tags': self.get_all_tags(),
            'total_commits': self.get_commit_count(),
            'author_commits': self.get_commit_count(self.get_original_author()),
            'file_count': self.get_file_count(),
            'is_clean': self.is_clean_working_directory()
        }
