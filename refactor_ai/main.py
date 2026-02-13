import typer
from rich.console import Console
from refactor_ai.configuration_manager import cli_ui

# Initialize the Typer application
app = typer.Typer(
    help="RefactorAI: AI-powered code enhancement tool.",
    no_args_is_help=True
)
console = Console()

# --- VITAL FIX: This tells Typer that 'refactor' is the main group ---
@app.callback()
def main():
    """
    RefactorAI CLI - Manage your AI coding tools.
    """
    pass
# ---------------------------------------------------------------------

@app.command()
def configure():
    """
    Opens the interactive configuration menu to manage API keys.
    """
    try:
        cli_ui.run_configuration_ui()
    except KeyboardInterrupt:
        console.print("\n[bold red]✖ Operation cancelled by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]✖ An unexpected error occurred:[/bold red] {e}")

if __name__ == "__main__":
    app()