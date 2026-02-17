import os
import json
import re
import shutil
from pathlib import Path
from typing import Optional, Tuple

from rich.console import Console
from rich.prompt import Confirm

# AI SDKs
import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic

# Internal Modules
from refactor_ai.configuration_manager import secrets_manager
from refactor_ai.github_manager import repo_files_loader, update_ops

console = Console()

CURRENT_DIR = Path(__file__).parent
PROMPTS_FILE = CURRENT_DIR / "system_prompt.json"

VALID_MODES = {"add_comments", "improve_code", "enhance"}

BINARY_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif",
    ".ico", ".pyc", ".exe",
    ".dll", ".so", ".lock"
)

MAX_FILE_SIZE = 40000


# =====================================================
# PROMPT LOADING
# =====================================================

def _load_system_prompt(mode_key: str) -> str:
    if mode_key not in VALID_MODES:
        mode_key = "enhance"

    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    base = data["base_instruction"]
    mode_data = data["modes"][mode_key]

    return (
        f"{base}\n\n"
        f"MODE: {mode_key}\n"
        f"ROLE: {mode_data['role']}\n"
        f"INSTRUCTIONS: {mode_data['instruction']}"
    )


# =====================================================
# RESPONSE PARSER
# =====================================================

def _strip_markdown_fence(code: str) -> str:
    if code.startswith("```"):
        lines = code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return code.strip()


def _parse_ai_response(response_text: str) -> Tuple[str, str]:

    code_match = re.search(
        r"\[CODE_START\](.*?)\[CODE_END\]",
        response_text,
        re.DOTALL,
    )

    msg_match = re.search(
        r"\[COMMIT_MESSAGE\](.*)",
        response_text,
        re.DOTALL,
    )

    if not code_match:
        raise ValueError("Missing [CODE_START] block.")

    code_content = _strip_markdown_fence(code_match.group(1))

    commit_msg = (
        msg_match.group(1).strip()
        if msg_match and msg_match.group(1).strip()
        else "refactor: automated enhancement by RefactorAI"
    )

    return code_content, commit_msg


# =====================================================
# AI CALLER
# =====================================================

def _call_ai_provider(provider: str, model: Optional[str], system: str, code: str):

    api_key = secrets_manager.get_key(provider)
    if not api_key:
        raise ValueError(f"No API key for {provider}")

    user_prompt = f"Please process this file:\n\n{code}"

    if provider == "google":
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(
            model_name=model or "gemini-1.5-flash",
            system_instruction=system,
        )
        return m.generate_content(user_prompt).text

    if provider == "openai":
        client = OpenAI(api_key=api_key)
        res = client.chat.completions.create(
            model=model or "gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
        )
        return res.choices[0].message.content

    if provider == "anthropic":
        client = Anthropic(api_key=api_key)
        res = client.messages.create(
            model=model or "claude-3-5-sonnet-20240620",
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return res.content[0].text

    raise ValueError("Unknown provider")


# =====================================================
# MAIN WORKFLOW
# =====================================================

def process_repo(
    provider: str,
    repo_url: str,
    mode: str,
    auto_commit: bool,
    metadata_file: Optional[str] = None,
):

    mode = mode if mode in VALID_MODES else "enhance"
    model = secrets_manager.get_preference(provider, "default_model")

    console.print(f"[bold cyan]RefactorAI[/bold cyan]: Using {provider} ({model})")

    temp_dir = "./.refactor_ai_temp"
    meta_name = metadata_file or "repo_metadata.json"

    with console.status("[green]Downloading repository..."):
        dl_result = repo_files_loader.download_repo_content(
            url=repo_url,
            output_folder=temp_dir,
            metadata_filename=meta_name,
        )

    if dl_result["status"] != "success":
        console.print(f"[red]{dl_result['message']}[/red]")
        return

    # ===== FIXED PART =====

    data = dl_result["data"]

    meta_path = data["metadata"]      # <-- FIXED
    local_root = data["local_path"]

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    files_list = metadata.get("downloaded_files", [])  # <-- FIXED
    repo_name = metadata["repo_name"]
    branch = metadata["branch"]
    base_path = metadata.get("base_path", "")

    system_prompt = _load_system_prompt(mode)

    # ===== FILE LOOP =====

    for rel_path in files_list:

        if rel_path.endswith(BINARY_EXTENSIONS):
            continue

        file_path = os.path.join(local_root, rel_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original = f.read()
        except Exception:
            continue

        if len(original) > MAX_FILE_SIZE:
            continue

        console.print(f"\n[bold]Processing:[/bold] {rel_path}")

        try:
            raw = _call_ai_provider(
                provider, model, system_prompt, original
            )
            new_code, commit_msg = _parse_ai_response(raw)

            # 🔥 NEW: Skip unchanged files
            if new_code.strip() == original.strip():
                console.print("[yellow]No changes generated — skipped[/yellow]")
                continue

        except Exception as e:
            console.print(f"[red]Failed: {e}[/red]")
            continue

        console.print(f"[green]{commit_msg}[/green]")

        if auto_commit or Confirm.ask("Apply and push?"):

            repo_path = (
                f"{base_path}/{rel_path}".replace("//", "/")
                if base_path else rel_path
            )

            result = update_ops.update_file_content(
                repo_name=repo_name,
                file_path=repo_path,
                new_content=new_code,
                branch=branch,
                message=commit_msg,
            )

            if result["status"] == "success":
                console.print("[bold green]✔ Pushed[/bold green]")
            else:
                console.print(f"[red]{result['message']}[/red]")

    shutil.rmtree(temp_dir, ignore_errors=True)

    console.print("\n[bold green]Job Complete[/bold green]")
