from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

GITHUB_DOCS = {
    "main": """
# GitHub Terminal Controls 🐙

Directly manage your GitHub repositories from the command line without AI interference.

## Available Commands

* `download`    - Download a repo/folder and generate AI metadata.
* `create-repo` - Create a new public or private repository.
* `add-file`    - Create or upload a file to a repository.
* `help`        - Show this help message or details for a specific command.

## Usage Examples

**Download a repo for AI analysis:**
`refactor github download https://github.com/owner/repo ./my_local_copy metadata.json`

**Create a private repository:**
`refactor github create-repo my-new-project --private`

**Upload a local file:**
`refactor github add-file owner/repo src/main.py ./local_script.py`
    """,
    
    "download": """
# Command: download

Downloads a repository (or a specific folder within it) and generates a metadata JSON file. This is crucial for giving the AI context about the project structure.

## Syntax
`refactor github download [URL] [OUTPUT_FOLDER] [METADATA_FILE]`

## Arguments
* `URL`: The GitHub URL (e.g., `https://github.com/owner/repo` or `.../tree/main/src`).
* `OUTPUT_FOLDER`: The local folder where files will be saved.
* `METADATA_FILE`: (Optional) Name of the JSON file containing the file tree (default: `repo_metadata.json`).

## Example
`refactor github download https://github.com/user/project ./analysis custom_tree.json`
    """,
    
    "create-repo": """
# Command: create-repo

Creates a new repository under your authenticated user account.

## Syntax
`refactor github create-repo [NAME] [OPTIONS]`

## Arguments
* `NAME`: The name of the new repository (e.g., `my-tool`).

## Options
* `--private / --public`: Visibility of the repo (Default: private).
* `--desc "Description"`: Add a description text.
* `--init / --no-init`: Create an initial README (Default: init).
    """,
    
    "add-file": """
# Command: add-file

Creates a new file in a GitHub repository. You can provide raw text content OR a path to a local file.

## Syntax
`refactor github add-file [REPO] [DEST_PATH] [SOURCE] [OPTIONS]`

## Arguments
* `REPO`: The full repository name (e.g., `username/project`).
* `DEST_PATH`: Where to save the file in the repo (e.g., `src/utils.py`).
* `SOURCE`: Either a local file path (`./main.py`) OR raw text content (`"print('hello')"`)

## Options
* `--branch`: The branch to commit to (Default: main).
* `--message`: The commit message.
    """
}

def display_help(topic: str = "main"):
    """Displays the requested help topic."""
    content = GITHUB_DOCS.get(topic, GITHUB_DOCS["main"])
    console.print(Panel(Markdown(content), title=f"GitHub Help: {topic}", border_style="cyan"))