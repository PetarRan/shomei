#!/usr/bin/env python3
"""
Main CLI entry point for shōmei.
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .core import ShomeiProcessor
from .config import Config
from .utils import setup_logging
from .art import print_logo, print_welcome, print_contributing, print_safety_reminder, print_version_info

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="shōmei")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to config file")
@click.pass_context
def cli(ctx, verbose, config):
    """
    shōmei - Show off your coding contributions without leaking corporate IP.
    
    Transforms your private commits into safe, sanitized commits and publishes them
    to your personal GitHub profile so your contribution graph reflects your real effort.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = config
    
    # Setup logging
    setup_logging(verbose)
    
    # Display ASCII logo
    print_logo("text")  # You can change to "geometric" if you prefer
    
    # Display banner
    banner = Text("shōmei", style="bold blue")
    subtitle = Text("Show off your coding contributions safely", style="italic")
    console.print(Panel(f"{banner}\n{subtitle}", style="blue"))


@cli.command()
@click.argument('repo_paths', nargs=-1, type=click.Path(exists=True))
@click.option('--personal-email', '-e', help='Your personal email for commits')
@click.option('--personal-name', '-n', help='Your personal name for commits')
@click.option('--placeholder-text', '-p', default='[STRIPPED] Corporate content removed for privacy', 
              help='Text to replace file contents with')
@click.option('--dry-run', is_flag=True, help='Preview changes without applying them')
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for sanitized repo')
@click.pass_context
def process(ctx, repo_paths, personal_email, personal_name, placeholder_text, dry_run, output_dir):
    """
    Process one or more repositories and create sanitized versions.
    
    REPO_PATHS: Paths to repositories to process (defaults to current directory)
    """
    if not repo_paths:
        repo_paths = ['.']
    
    # Load config
    config = Config(ctx.obj.get('config'))
    
    # Override config with CLI options
    if personal_email:
        config.personal_email = personal_email
    if personal_name:
        config.personal_name = personal_name
    if placeholder_text:
        config.placeholder_text = placeholder_text
    
    # Validate config
    if not config.is_valid():
        console.print("[red]Error: Invalid configuration. Please set personal email and name.[/red]")
        console.print("Use --personal-email and --personal-name options or create a config file.")
        sys.exit(1)
    
    # Process each repository
    for repo_path in repo_paths:
        console.print(f"\n[bold]Processing repository:[/bold] {repo_path}")
        
        try:
            processor = ShomeiProcessor(repo_path, config)
            
            if dry_run:
                console.print("[yellow]DRY RUN MODE - No changes will be applied[/yellow]")
                processor.dry_run()
            else:
                processor.process()
                
        except Exception as e:
            console.print(f"[red]Error processing {repo_path}: {e}[/red]")
            if ctx.obj.get('verbose'):
                console.print_exception()
            sys.exit(1)


@cli.command()
@click.option('--config-path', '-c', default='~/.shomei/config.yml', 
              help='Path to config file')
@click.pass_context
def init(ctx, config_path):
    """
    Initialize configuration file with your personal details.
    """
    # Show welcome message for first-time users
    print_welcome()
    print()  # Add spacing
    
    config_path = Path(config_path).expanduser()
    
    if config_path.exists():
        if not click.confirm(f"Config file {config_path} already exists. Overwrite?"):
            return
    
    # Get user input
    personal_name = click.prompt("Enter your personal name for commits")
    personal_email = click.prompt("Enter your personal email for commits")
    
    # Create config
    config = Config()
    config.personal_name = personal_name
    config.personal_email = personal_email
    
    # Save config
    config.save(config_path)
    console.print(f"[green]Configuration saved to {config_path}[/green]")
    
    # Show next steps and contributing info
    print()
    print_contributing()
    print()
    print_safety_reminder()


@cli.command()
def logo():
    """
    Display the shōmei ASCII logo.
    """
    print_logo()


@cli.command()
def contribute():
    """
    Show information about contributing to shōmei.
    """
    print_contributing()


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True))
@click.pass_context
def analyze(ctx, repo_path):
    """
    Analyze a repository to show what would be processed.
    """
    try:
        # Load config from context
        config = Config(ctx.obj.get('config'))
        processor = ShomeiProcessor(repo_path, config)
        processor.analyze()
    except Exception as e:
        console.print(f"[red]Error analyzing {repo_path}: {e}[/red]")
        if ctx.obj.get('verbose'):
            console.print_exception()
        sys.exit(1)


if __name__ == '__main__':
    cli()
