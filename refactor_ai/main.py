import typer
from typing import Optional
from rich.console import Console

from refactor_ai.configuration_manager import cli_ui, secrets_manager
from refactor_ai.help_docs import help_utils

# Sub-apps
from refactor_ai.github_manager import github_terminal_controls
from refactor_ai.enhancer import terminal_controls as enhancer_terminal_controls

app = typer.Typer(
    help="RefactorAI: AI-powered code enhancement tool.",
    no_args_is_help=True
)

console = Console()

# =====================================================
# MOUNT SUB COMMANDS
# =====================================================

app.add_typer(github_terminal_controls.app, name="github")
app.add_typer(enhancer_terminal_controls.app, name="enhancer")


# =====================================================
# MAIN CALLBACK
# =====================================================

@app.callback()
def main():
    """RefactorAI CLI Management"""
    pass


# =====================================================
# CONFIGURATION
# =====================================================

@app.command()
def configure(
    provider: Optional[str] = typer.Argument(None, help="Provider name (google, openai, github)"),
    api_key: Optional[str] = typer.Argument(None, help="API Key or Token"),
    default_setting: Optional[str] = typer.Argument(None, help="Default model or access tag")
):
    """
    Manage configuration.

    Interactive:
        refactor configure

    Direct:
        refactor configure google <KEY> gpt-4o
    """

    if not provider:
        cli_ui.run_configuration_ui()
        return

    if not api_key:
        console.print("[red]Error: API key required.[/red]")
        return

    provider = provider.lower()

    secrets_manager.save_key(provider, api_key)
    console.print(f"[green]✔ Key saved for {provider}[/green]")

    if default_setting:
        if provider == "github":
            secrets_manager.save_preference(provider, "access_level", default_setting)
            console.print(f"[green]✔ Access level set: {default_setting}[/green]")
        else:
            secrets_manager.save_preference(provider, "default_model", default_setting)
            console.print(f"[green]✔ Default model set: {default_setting}[/green]")

    elif provider == "github":
        level = secrets_manager.verify_github_access(api_key)
        secrets_manager.save_preference(provider, "access_level", level)
        console.print(f"[green]✔ Verified GitHub access: {level}[/green]")


# =====================================================
# HELP
# =====================================================

@app.command()
def help_tags():
    """Show available tags and commands."""
    help_utils.display_help_tags()


if __name__ == "__main__":
    app()
