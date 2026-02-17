from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

ENHANCER_DOCS = {
    "main": """
# AI Enhancer Controls 🤖

Use RefactorAI enhancer to automatically improve repository code using AI.

## Available Commands

* `google`     - Use Google Gemini models
* `openai`     - Use OpenAI models
* `anthropic`  - Use Anthropic Claude models

## Enhancement Modes

* `--enhance` (default)  
  Adds comments + improves code structure.

* `--add-comments`  
  Adds documentation only (no logic changes).

* `--improve-code`  
  Optimizes code while preserving behavior.

## Common Options

* `--auto`           - Auto-commit without confirmation.
* `--metadata-file`  - Use custom metadata JSON.

## Example Usage

**Full enhancement (default):**
`refactor enhancer openai https://github.com/user/repo`

**Only add comments:**
`refactor enhancer google https://github.com/user/repo --add-comments`

**Improve performance only:**
`refactor enhancer anthropic https://github.com/user/repo --improve-code`

**Auto commit all files:**
`refactor enhancer openai https://github.com/user/repo --auto`
""",

    "modes": """
# Enhancement Modes

## --enhance (Default)

- Adds useful comments
- Improves structure
- Removes dead code
- Preserves external behaviour

## --add-comments

- Documentation only
- No logic or algorithm changes
- Safe for production codebases

## --improve-code

- Optimize internals
- Improve readability
- Remove unused imports
- Function signatures remain unchanged
""",

    "auto": """
# Auto Mode

Using `--auto` skips confirmation prompts.

Example:

`refactor enhancer openai https://github.com/user/repo --auto`

⚠️ Recommended only after testing.
""",

    "metadata": """
# Custom Metadata

You can provide your own metadata file:

`--metadata-file custom_meta.json`

If not provided, default metadata generated during download is used.
"""
}


def display_help(topic: str = "main"):
    """Display enhancer help docs."""
    content = ENHANCER_DOCS.get(topic, ENHANCER_DOCS["main"])
    console.print(
        Panel(
            Markdown(content),
            title=f"Enhancer Help: {topic}",
            border_style="green"
        )
    )
