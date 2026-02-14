from rich.console import Console
from rich.table import Table

console = Console()

def display_help_tags():
    """Displays a cheat sheet of available commands and tags."""
    
    table = Table(title="RefactorAI Command Reference", border_style="cyan")
    table.add_column("Command / Tag", style="bold yellow")
    table.add_column("Description", style="white")

    # Core Commands
    table.add_row("refactor configure", "Open the interactive menu")
    table.add_row("refactor configure [provider] [key]", "Quickly set a key (Direct Mode)")
    table.add_row("refactor configure [provider] [key] [model]", "Set key AND default model")

    # Future Commands (Placeholders for your next steps)
    table.add_section()
    table.add_row("--dry-run", "Preview changes without modifying files")
    table.add_row("--model <name>", "Override the default model for this run")
    table.add_row("--access <level>", "Force a specific GitHub access check")

    console.print(table)