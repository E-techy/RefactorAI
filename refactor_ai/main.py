import typer
from typing import Optional
from rich.console import Console
from refactor_ai.configuration_manager import cli_ui, secrets_manager
from refactor_ai import help_docs

app = typer.Typer(help="RefactorAI: AI-powered code enhancement tool.", no_args_is_help=True)
console = Console()

@app.callback()
def main():
    """RefactorAI CLI Management"""
    pass

@app.command()
def configure(
    provider: Optional[str] = typer.Argument(None, help="Provider name (google, openai, github)"),
    api_key: Optional[str] = typer.Argument(None, help="The API Key or Token"),
    default_setting: Optional[str] = typer.Argument(None, help="Default model name OR access tag")
):
    """
    Manage configuration. 
    Run without arguments for interactive UI.
    Run WITH arguments for direct setup: 'refactor configure google <KEY> gemini-1.5-flash'
    """
    # 1. Interactive Mode
    if not provider:
        cli_ui.run_configuration_ui()
        return

    # 2. Direct Command Mode
    if not api_key:
        console.print("[red]Error: You must provide an API key in direct mode.[/red]")
        return

    # Normalize provider name
    provider = provider.lower()
    
    # Save Secret
    secrets_manager.save_key(provider, api_key)
    console.print(f"[green]✔ Key saved for {provider}[/green]")

    # Save Setting (Model or Access Level)
    if default_setting:
        if provider == "github":
            # For GitHub, we verify first, then save user tag if provided, 
            # but usually verification is better. We'll save the tag provided by user.
            secrets_manager.save_preference(provider, 'access_level', default_setting)
            console.print(f"[green]✔ Access level set to: {default_setting}[/green]")
        else:
            secrets_manager.save_preference(provider, 'default_model', default_setting)
            console.print(f"[green]✔ Default model set to: {default_setting}[/green]")
    elif provider == "github":
        # If no tag provided, auto-verify
        level = secrets_manager.verify_github_access(api_key)
        secrets_manager.save_preference(provider, 'access_level', level)
        console.print(f"[green]✔ Verified Access Level: {level}[/green]")

@app.command()
def help_tags():
    """Show available tags and commands."""
    help_docs.help_utils.display_help_tags()

if __name__ == "__main__":
    app()