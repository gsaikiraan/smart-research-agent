#!/usr/bin/env python3
"""
Smart Research Agent - Main Entry Point
AI-powered research assistant for gathering and organizing knowledge.
"""

import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Load environment variables
load_dotenv()

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Smart Research Agent - AI-powered research assistant."""
    pass


@cli.command()
@click.argument("topic")
@click.option(
    "--depth",
    "-d",
    type=click.Choice(["quick", "standard", "deep"]),
    default="standard",
    help="Research depth level",
)
@click.option(
    "--max-sources",
    "-m",
    type=int,
    default=5,
    help="Maximum number of sources to analyze",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path for the report",
)
def research(topic, depth, max_sources, output):
    """Conduct research on a given TOPIC."""
    from src.utils.config import Config
    from src.agent.research_agent import ResearchAgent

    console.print(
        Panel.fit(
            f"[bold cyan]Starting research on:[/bold cyan] {topic}\n"
            f"[dim]Depth: {depth} | Max sources: {max_sources}[/dim]",
            title="Research Agent",
        )
    )

    try:
        # Load and validate configuration
        config = Config()
        is_valid, error_msg = config.validate()

        if not is_valid:
            console.print(f"[red]Configuration error: {error_msg}[/red]")
            console.print("[yellow]Please run 'python main.py setup' first[/yellow]")
            sys.exit(1)

        # Create research agent
        agent = ResearchAgent(config)

        # Conduct research
        result = agent.research(topic, depth=depth, max_sources=max_sources)

        # Display results
        console.print("\n[bold green]✓ Research completed![/bold green]")
        console.print(f"\n[cyan]Session ID:[/cyan] {result['session_id']}")
        console.print(f"[cyan]Report saved to:[/cyan] {result['report_path']}")
        console.print(f"[cyan]Sources analyzed:[/cyan] {len(result['sources'])}")
        console.print(f"[cyan]Findings extracted:[/cyan] {len(result['findings'])}")

        # Copy to custom output if specified
        if output:
            import shutil
            shutil.copy(result['report_path'], output)
            console.print(f"[cyan]Copied to:[/cyan] {output}")

    except Exception as e:
        console.print(f"[red]Error during research: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@cli.command()
@click.argument("query")
def search(query):
    """Search for information on a QUERY."""
    from src.search.web_search import WebSearcher

    console.print(f"[cyan]Searching for:[/cyan] {query}")

    try:
        searcher = WebSearcher()
        results = searcher.search(query, max_results=10)

        if not results:
            console.print("[yellow]No results found[/yellow]")
            return

        console.print(f"\n[bold]Found {len(results)} results:[/bold]\n")

        for i, result in enumerate(results, 1):
            console.print(f"[bold cyan]{i}. {result['title']}[/bold cyan]")
            console.print(f"   [dim]{result['url']}[/dim]")
            console.print(f"   {result['snippet'][:150]}...\n")

    except Exception as e:
        console.print(f"[red]Error during search: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option(
    "--limit",
    "-l",
    type=int,
    default=10,
    help="Number of reports to list",
)
def list_reports(limit):
    """List previous research reports."""
    from src.utils.config import Config
    from src.storage.database import ResearchDatabase
    from rich.table import Table

    console.print(f"[cyan]Listing last {limit} reports...[/cyan]\n")

    try:
        config = Config()
        db = ResearchDatabase(config.database_path)
        sessions = db.list_sessions(limit=limit)

        if not sessions:
            console.print("[yellow]No research sessions found[/yellow]")
            return

        # Create table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="dim")
        table.add_column("Topic", style="cyan")
        table.add_column("Depth")
        table.add_column("Status")
        table.add_column("Created")

        for session in sessions:
            status_color = "green" if session["status"] == "completed" else "yellow"
            table.add_row(
                str(session["id"]),
                session["topic"][:50],
                session["depth"],
                f"[{status_color}]{session['status']}[/{status_color}]",
                session["created_at"][:16],
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing reports: {e}[/red]")
        sys.exit(1)


@cli.command()
def setup():
    """Run initial setup and configuration check."""
    from src.utils.config import Config

    console.print(Panel.fit("[bold]Smart Research Agent - Setup[/bold]"))

    # Check for .env file
    if not Path(".env").exists():
        console.print("[yellow]⚠ .env file not found[/yellow]")
        console.print("Please copy .env.example to .env and add your API keys:")
        console.print("  [dim]cp .env.example .env[/dim]")
        return

    console.print("[green]✓[/green] .env file found")

    # Load and validate configuration
    try:
        config = Config()
        is_valid, error_msg = config.validate()

        if not is_valid:
            console.print(f"[red]✗ Configuration error: {error_msg}[/red]")
            return

        console.print(f"[green]✓[/green] Configuration valid")
        console.print(f"[green]✓[/green] AI Provider: {config.ai_provider}")
        console.print(f"[green]✓[/green] Model: {config.get_model()}")
        console.print(f"[green]✓[/green] Search Engine: {config.search_engine}")
        console.print(f"[green]✓[/green] Database: {config.database_path}")
        console.print(f"[green]✓[/green] Reports Directory: {config.report_output_dir}")

        console.print("\n[bold green]Setup complete! You're ready to start researching.[/bold green]")
        console.print("\n[dim]Try: python main.py research \"your topic here\"[/dim]")

    except Exception as e:
        console.print(f"[red]Error during setup: {e}[/red]")


if __name__ == "__main__":
    cli()
