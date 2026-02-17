import typer
from typing import Optional

from refactor_ai.enhancer.code_enhancer import code_enhancer

app = typer.Typer(help="Run AI-powered repository enhancement.")

VALID_PROVIDERS = {"google", "openai", "anthropic"}


# =====================================================
# INTERNAL MODE RESOLVER
# =====================================================

def _resolve_mode(
    add_comments: bool,
    improve_code: bool,
    enhance: bool,
) -> str:
    """
    Determine enhancement mode.

    Priority:
    --add-comments > --improve-code > --enhance (default)
    """

    if add_comments:
        return "add_comments"

    if improve_code:
        return "improve_code"

    return "enhance"


def _run_enhancement_command(
    provider: str,
    repo_url: str,
    add_comments: bool,
    improve_code: bool,
    enhance: bool,
    auto: bool,
    metadata_file: Optional[str],
):
    """Unified enhancement runner."""

    if provider not in VALID_PROVIDERS:
        raise typer.BadParameter(f"Invalid provider: {provider}")

    mode = _resolve_mode(add_comments, improve_code, enhance)

    code_enhancer.process_repo(
        provider=provider,
        repo_url=repo_url,
        mode=mode,
        auto_commit=auto,
        metadata_file=metadata_file,
    )


# =====================================================
# PROVIDER COMMANDS
# =====================================================

@app.command("google")
def google_enhance(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    add_comments: bool = typer.Option(False, "--add-comments", help="Only add documentation"),
    improve_code: bool = typer.Option(False, "--improve-code", help="Only improve code structure/performance"),
    enhance: bool = typer.Option(True, "--enhance/--no-enhance", help="Full enhancement (default)"),
    auto: bool = typer.Option(False, "--auto", help="Auto-commit all changes"),
    metadata_file: Optional[str] = typer.Option(None, help="Custom metadata file"),
):
    """Use Google Gemini for enhancement."""
    _run_enhancement_command(
        "google",
        repo_url,
        add_comments,
        improve_code,
        enhance,
        auto,
        metadata_file,
    )


@app.command("openai")
def openai_enhance(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    add_comments: bool = typer.Option(False, "--add-comments", help="Only add documentation"),
    improve_code: bool = typer.Option(False, "--improve-code", help="Only improve code structure/performance"),
    enhance: bool = typer.Option(True, "--enhance/--no-enhance", help="Full enhancement (default)"),
    auto: bool = typer.Option(False, "--auto", help="Auto-commit all changes"),
    metadata_file: Optional[str] = typer.Option(None, help="Custom metadata file"),
):
    """Use OpenAI GPT for enhancement."""
    _run_enhancement_command(
        "openai",
        repo_url,
        add_comments,
        improve_code,
        enhance,
        auto,
        metadata_file,
    )


@app.command("anthropic")
def anthropic_enhance(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    add_comments: bool = typer.Option(False, "--add-comments", help="Only add documentation"),
    improve_code: bool = typer.Option(False, "--improve-code", help="Only improve code structure/performance"),
    enhance: bool = typer.Option(True, "--enhance/--no-enhance", help="Full enhancement (default)"),
    auto: bool = typer.Option(False, "--auto", help="Auto-commit all changes"),
    metadata_file: Optional[str] = typer.Option(None, help="Custom metadata file"),
):
    """Use Anthropic Claude for enhancement."""
    _run_enhancement_command(
        "anthropic",
        repo_url,
        add_comments,
        improve_code,
        enhance,
        auto,
        metadata_file,
    )
