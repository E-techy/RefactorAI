import typer
import os
from rich.console import Console
from typing import Optional

# Import the operations
from . import repo_ops, create_ops, repo_files_loader
from refactor_ai.help_docs import github_help

app = typer.Typer(help="Manual GitHub controls (create repos, add files).")
console = Console()

@app.command("help")
def help_command(command_name: Optional[str] = typer.Argument(None)):
    """
    Show help for GitHub commands. 
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
    dest_path: str = typer.Argument(..., help="Path inside the repo"),
    source: str = typer.Argument(..., help="Local file path OR content string"),
    branch: str = typer.Option("main", help="Branch to commit to"),
    message: str = typer.Option("Add file via RefactorAI", help="Commit message")
):
    """
    Add a file to a repo.
    """
    content_to_upload = source
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
        result = create_ops.create_file(repo, dest_path, content_to_upload, branch, message)

    if result["status"] == "success":
        console.print(f"[bold green]✔ Success![/bold green] {result['message']}")
    else:
        console.print(f"[bold red]✖ Error:[/bold red] {result['message']}")

@app.command("download")
def download(
    url: str = typer.Argument(..., help="GitHub URL (Repo or Folder)"),
    output_folder: str = typer.Argument(..., help="Local destination folder"),
    metadata_file: str = typer.Argument("repo_metadata.json", help="Metadata filename"),
    branch: Optional[str] = typer.Option(None, "--branch", help="Override branch (e.g. 'dev')"),
    metadata_scope: str = typer.Option("current", "--metadata-scope", help="'current' (folder only) or 'all' (entire repo tree)")
):
    """
    Download files from GitHub and generate AI context.
    
    Example:
    refactor github download https://github.com/owner/repo/tree/main/docs ./docs --metadata-scope all
    """
    console.print(f"[dim]Source:[/dim] {url}")
    console.print(f"[dim]Branch:[/dim] {branch if branch else 'Default'}")
    console.print(f"[dim]Scope:[/dim] {metadata_scope}")
    
    with console.status("[bold green]Downloading..."):
        result = repo_files_loader.download_repo_content(
            url=url, 
            output_folder=output_folder,
            metadata_filename=metadata_file,
            branch=branch,
            metadata_scope=metadata_scope
        )
    
    if result["status"] == "success":
        console.print(f"[bold green]✔ Download Complete![/bold green]")
        console.print(f"Downloaded: {result['data']['download_count']} files to [cyan]{result['data']['local_path']}[/cyan]")
        console.print(f"Total Context: {result['data']['total_scope_count']} files in metadata")
        console.print(f"Metadata File: [cyan]{result['data']['metadata']}[/cyan]")
    else:
        console.print(f"[bold red]✖ Error:[/bold red] {result['message']}")