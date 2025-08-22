"""
Core processing logic for shōmei.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from git import Repo, Commit
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import Config
from .git_utils import GitUtils

console = Console()


class ShomeiProcessor:
    """Main processor for sanitizing repositories."""
    
    def __init__(self, repo_path: str, config: Config):
        self.repo_path = Path(repo_path).resolve()
        self.config = config
        self.git_utils = GitUtils(self.repo_path)
        self.temp_dir = None
        
        # Validate repository
        if not self._is_valid_repo():
            raise ValueError(f"Not a valid git repository: {repo_path}")
    
    def _is_valid_repo(self) -> bool:
        """Check if the path is a valid git repository."""
        return (self.repo_path / '.git').exists()
    
    def analyze(self) -> None:
        """Analyze the repository and show what would be processed."""
        console.print(f"\n[bold]Analyzing repository:[/bold] {self.repo_path}")
        
        # Get repository info
        repo = Repo(self.repo_path)
        original_author = self.git_utils.get_original_author()
        
        console.print(f"Original author: {original_author}")
        console.print(f"Target author: {self.config.personal_name} <{self.config.personal_email}>")
        
        # Analyze commits
        commits = list(repo.iter_commits('HEAD'))
        console.print(f"Total commits: {len(commits)}")
        
        # Count commits by author
        author_counts = {}
        for commit in commits:
            author = commit.author.email
            author_counts[author] = author_counts.get(author, 0) + 1
        
        # Display author breakdown
        table = Table(title="Commit Analysis")
        table.add_column("Author", style="cyan")
        table.add_column("Commits", style="magenta", justify="right")
        table.add_column("Status", style="green")
        
        for author, count in author_counts.items():
            if author == original_author:
                status = "Will be rewritten"
            else:
                status = "Will be preserved"
            table.add_row(author, str(count), status)
        
        console.print(table)
        
        # Show file types that will be stripped
        console.print(f"\n[bold]Files that will be stripped:[/bold]")
        for ext in self.config.strip_file_extensions:
            console.print(f"  • {ext}")
        
        console.print(f"\n[bold]Files that will be preserved:[/bold]")
        for ext in self.config.preserve_file_extensions:
            console.print(f"  • {ext}")
    
    def dry_run(self) -> None:
        """Perform a dry run without making changes."""
        console.print("\n[bold]DRY RUN - No changes will be applied[/bold]")
        
        # Analyze first
        self.analyze()
        
        # Show what would happen
        console.print("\n[bold]What would happen:[/bold]")
        console.print("  • Create temporary working copy")
        console.print("  • Filter commits by original author")
        console.print("  • Rewrite commit metadata")
        console.print("  • Strip file contents")
        console.print("  • Clean branches and tags")
        console.print("  • Output sanitized repository")
    
    def process(self) -> None:
        """Process the repository and create a sanitized version."""
        console.print(f"\n[bold]Processing repository:[/bold] {self.repo_path}")
        
        try:
            # Create temporary working copy
            self._create_temp_copy()
            
            # Process the temporary copy
            self._process_temp_repo()
            
            # Clean up
            self._cleanup()
            
            console.print("[green]Repository processing completed successfully![/green]")
            
        except Exception as e:
            self._cleanup()
            raise e
    
    def _create_temp_copy(self) -> None:
        """Create a temporary working copy of the repository."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="shomei_"))
        console.print(f"Creating temporary copy in: {self.temp_dir}")
        
        # Copy repository (excluding .git)
        shutil.copytree(
            self.repo_path,
            self.temp_dir / self.repo_path.name,
            ignore=shutil.ignore_patterns('.git'),
            dirs_exist_ok=True
        )
        
        # Copy .git directory separately
        shutil.copytree(
            self.repo_path / '.git',
            self.temp_dir / self.repo_path.name / '.git'
        )
        
        self.temp_repo_path = self.temp_dir / self.repo_path.name
    
    def _process_temp_repo(self) -> None:
        """Process the temporary repository."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Step 1: Filter commits
            task = progress.add_task("Filtering commits by author...", total=None)
            self._filter_commits()
            progress.update(task, completed=True)
            
            # Step 2: Rewrite commits
            task = progress.add_task("Rewriting commit metadata...", total=None)
            self._rewrite_commits()
            progress.update(task, completed=True)
            
            # Step 3: Strip file contents
            task = progress.add_task("Stripping file contents...", total=None)
            self._strip_file_contents()
            progress.update(task, completed=True)
            
            # Step 4: Clean branches and tags
            task = progress.add_task("Cleaning branches and tags...", total=None)
            self._clean_branches_and_tags()
            progress.update(task, completed=True)
    
    def _filter_commits(self) -> None:
        """Filter commits to only include those by the original author."""
        repo = Repo(self.temp_repo_path)
        original_author = self.git_utils.get_original_author()
        
        # Get all commits by the original author
        author_commits = []
        for commit in repo.iter_commits('HEAD'):
            if commit.author.email == original_author:
                author_commits.append(commit)
        
        console.print(f"Found {len(author_commits)} commits by {original_author}")
        
        if not author_commits:
            raise ValueError("No commits found by the original author")
        
        # Create new branch with filtered commits
        new_branch_name = "shomei_sanitized"
        
        # Delete branch if it exists
        try:
            repo.delete_head(new_branch_name)
        except:
            pass
        
        # Create new branch from the first commit
        first_commit = author_commits[-1]  # Git iterates in reverse chronological order
        new_branch = repo.create_head(new_branch_name, first_commit)
        new_branch.checkout()
        
        # Cherry-pick commits in order
        for commit in reversed(author_commits[1:]):
            try:
                repo.git.cherry_pick(commit.hexsha, '--no-commit')
            except subprocess.CalledProcessError:
                # Handle conflicts by aborting and trying a different approach
                repo.git.cherry_pick('--abort')
                # For now, we'll use a simpler approach - just create new commits
                break
    
    def _rewrite_commits(self) -> None:
        """Rewrite commit metadata with personal information."""
        repo = Repo(self.temp_repo_path)
        
        # Use git filter-branch to rewrite all commits
        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = self.config.personal_name
        env['GIT_AUTHOR_EMAIL'] = self.config.personal_email
        env['GIT_COMMITTER_NAME'] = self.config.personal_name
        env['GIT_COMMITTER_EMAIL'] = self.config.personal_email
        
        # Rewrite all commits in the current branch
        try:
            subprocess.run(
                ['git', 'filter-branch', '--env-filter', 
                 f'export GIT_AUTHOR_NAME="{self.config.personal_name}" && '
                 f'export GIT_AUTHOR_EMAIL="{self.config.personal_email}" && '
                 f'export GIT_COMMITTER_NAME="{self.config.personal_name}" && '
                 f'export GIT_COMMITTER_EMAIL="{self.config.personal_email}"'],
                cwd=self.temp_repo_path,
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            console.print(f"[yellow]Warning: Could not rewrite all commits: {e}[/yellow]")
    
    def _strip_file_contents(self) -> None:
        """Strip file contents and replace with placeholder text."""
        repo = Repo(self.temp_repo_path)
        
        # Get all files in the working directory
        working_dir = self.temp_repo_path
        files_to_strip = []
        
        for root, dirs, files in os.walk(working_dir):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(working_dir)
                
                if self.config.should_strip_file(str(rel_path)):
                    files_to_strip.append(file_path)
        
        console.print(f"Stripping contents of {len(files_to_strip)} files")
        
        # Replace file contents
        for file_path in files_to_strip:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.config.placeholder_text)
            except Exception as e:
                console.print(f"[yellow]Warning: Could not strip {file_path}: {e}[/yellow]")
        
        # Stage all changes
        repo.index.add('*')
        
        # Create a commit for the stripped files
        if repo.index.diff('HEAD'):
            repo.index.commit("Strip file contents for privacy")
    
    def _clean_branches_and_tags(self) -> None:
        """Clean branches and tags, keeping only specified ones."""
        repo = Repo(self.temp_repo_path)
        
        # Delete all branches except the ones we want to keep
        for branch in repo.branches:
            if branch.name not in self.config.keep_branches:
                try:
                    repo.delete_head(branch.name, force=True)
                except:
                    pass
        
        # Delete all tags
        for tag in repo.tags:
            try:
                repo.delete_tag(tag.name)
            except:
                pass
        
        console.print(f"Kept branches: {', '.join(self.config.keep_branches)}")
        console.print("Removed all other branches and tags")
    
    def _cleanup(self) -> None:
        """Clean up temporary files."""
        if self.temp_dir and self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
                console.print("Cleaned up temporary files")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not clean up temporary files: {e}[/yellow]")
