import json
import os
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path

# Import our secrets manager
from . import secrets_manager

console = Console()

# Path to the JSON file we created earlier
CURRENT_DIR = Path(__file__).parent
PROVIDERS_FILE = CURRENT_DIR / "providers.json"

def load_providers():
    """Loads the JSON configuration of supported providers."""
    with open(PROVIDERS_FILE, "r") as f:
        data = json.load(f)
    return data["providers"]

def show_header():
    """Displays the branded header for the CLI."""
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]RefactorAI Configuration Manager[/bold cyan]\n"
        "[dim]Securely manage your API keys and GitHub tokens[/dim]",
        border_style="cyan"
    ))

def show_status_table(providers):
    """
    Prints a beautiful table showing which keys are currently set.
    """
    table = Table(title="Current Configuration Status", show_header=True, header_style="bold magenta")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", justify="center")
    
    for pid, details in providers.items():
        # Check if the key exists in the secure vault
        is_set = secrets_manager.is_configured(pid)
        status = "[green]✔ Configured[/green]" if is_set else "[red]✖ Missing[/red]"
        table.add_row(details["name"], status)
    
    console.print(table)
    console.print("\n")

def run_configuration_ui():
    """
    The main UI loop. This is what runs when user types 'refactor configure'.
    """
    providers = load_providers()

    while True:
        show_header()
        show_status_table(providers)

        # 1. Main Menu Options
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Configure/Update a Key",
                "Delete a Key",
                "Clear ALL Data",
                "Exit"
            ],
            style=questionary.Style([('answer', 'fg:cyan bold')])
        ).ask()

        # 2. Handle Actions
        if action == "Exit":
            console.print("[green]Configuration saved. Exiting...[/green]")
            break

        elif action == "Configure/Update a Key":
            # Let user choose which provider to set
            # We create a list of nice names like "Google Gemini"
            choices = [{"name": p_data["name"], "value": p_id} for p_id, p_data in providers.items()]
            
            target_provider = questionary.select(
                "Select provider to configure:",
                choices=choices
            ).ask()
            
            # Prompt for the API Key (Password mode hides input but allows paste)
            new_key = questionary.password(
                f"Enter your API Key for {providers[target_provider]['name']}:",
                validate=lambda text: True if len(text) > 5 else "Key looks too short to be valid."
            ).ask()
            
            if new_key:
                secrets_manager.save_key(target_provider, new_key)
                console.print(f"[bold green]✔ Key for {providers[target_provider]['name']} saved securely![/bold green]")
                questionary.press_any_key_to_continue().ask()

        elif action == "Delete a Key":
            choices = [{"name": p_data["name"], "value": p_id} for p_id, p_data in providers.items()]
            target_provider = questionary.select("Select key to remove:", choices=choices).ask()
            
            confirm = questionary.confirm(f"Are you sure you want to delete the key for {providers[target_provider]['name']}?").ask()
            if confirm:
                secrets_manager.delete_key(target_provider)
                console.print(f"[yellow]✔ Key removed.[/yellow]")
                questionary.press_any_key_to_continue().ask()

        elif action == "Clear ALL Data":
            confirm = questionary.confirm(
                "WARNING: This will delete ALL API keys and tokens. Continue?",
                default=False
            ).ask()
            
            if confirm:
                secrets_manager.clear_all_keys(list(providers.keys()))
                console.print(f"[bold red]✔ All configuration data has been wiped.[/bold red]")
                questionary.press_any_key_to_continue().ask()