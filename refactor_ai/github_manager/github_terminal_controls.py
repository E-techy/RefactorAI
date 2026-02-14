import typer
import os
from rich.console import Console
from typing import Optional

# Import the operations
from . import repo_ops, create_ops
from refactor_ai.help_docs import github_help

app = typer.Typer(help="Manual GitHub controls (create repos, add files).")
console = Console()

@app.command("help")
def help_command(command_name: Optional[str] = typer.Argument(None)):
    """
    Show help for GitHub commands. 
    Example: 'refactor github help add-file'
    """
    topic = command_name if command_name else "main"
    github_help.display_help(topic)

@app.command("create-repo")
def create_repo(
    name: str = typer.Argument(..., help="Name of the new repository"),
    private: bool = typer.Option(True, "--private/--public", help="Visibility of the repo"),
    desc: str = typer.Option("", help="Description of the repository"),
    init: bool = typer.Option(True, "--init/--no-init", help="Initialize with README")
):
    """
    Create a new repository on GitHub.
    """
    with console.status(f"[bold green]Creating repo '{name}'..."):
        result = repo_ops.create_new_repo(name, private, desc, init)
    
    if result["status"] == "success":
        console.print(f"[bold green]✔ Success![/bold green] {result['message']}")
        console.print(f"URL: {result['data']['url']}")
    else:
        console.print(f"[bold red]✖ Error:[/bold red] {result['message']}")

@app.command("add-file")
def add_file(
    repo: str = typer.Argument(..., help="Repository name (owner/repo)"),
    dest_path: str = typer.Argument(..., help="Path inside the repo (e.g., src/main.py)"),
    source: str = typer.Argument(..., help="Local file path OR content string"),
    branch: str = typer.Option("main", help="Branch to commit to"),
    message: str = typer.Option("Add file via RefactorAI", help="Commit message")
):
    """
    Add a file to a repo. Source can be a local path or raw text.
    """
    content_to_upload = source

    # Check if source is a local file
    if os.path.exists(source):
        try:
            with open(source, "r") as f:
                content_to_upload = f.read()
            console.print(f"[dim]Read content from local file: {source}[/dim]")
        except Exception as e:
            console.print(f"[red]Error reading local file: {e}[/red]")
            return
    else:
        console.print("[dim]Treating source as raw text content.[/dim]")

    with console.status(f"[bold green]Uploading to {repo}..."):
        result = create_ops.create_file(
            repo_name=repo,
            file_path=dest_path,
            content=content_to_upload,
            branch=branch,
            message=message
        )

    if result["status"] == "success":
        console.print(f"[bold green]✔ Success![/bold green] {result['message']}")
        console.print(f"Commit SHA: {result['data']['commit_sha']}")
    else:
        console.print(f"[bold red]✖ Error:[/bold red] {result['message']}")