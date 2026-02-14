import keyring
import json
import requests
import os
import stat
from pathlib import Path
from typing import Optional, Dict, Any

# --- Constants ---
APP_NAME = "refactor-ai"
APP_SERVICE_ID = "RefactorAI_CLI"
CONFIG_DIR = Path.home() / f".{APP_NAME}"
PREFS_FILE = CONFIG_DIR / "preferences.json"


def save_key(provider_id: str, api_key: str) -> None:
    """Saves API key securely to OS Keychain."""
    if api_key and api_key.strip():
        keyring.set_password(APP_SERVICE_ID, provider_id, api_key.strip())

def get_key(provider_id: str) -> Optional[str]:
    """Retrieves API key from OS Keychain."""
    try:
        return keyring.get_password(APP_SERVICE_ID, provider_id)
    except Exception:
        return None

def delete_key(provider_id: str) -> None:
    """Removes API key from Keychain."""
    try:
        keyring.delete_password(APP_SERVICE_ID, provider_id)
    except keyring.errors.PasswordDeleteError:
        pass

# --- 2. Preference Storage (JSON) ---

def _ensure_config_exists():
    """Creates the config folder and preferences file if missing."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    
    if not PREFS_FILE.exists():
        with open(PREFS_FILE, "w") as f:
            json.dump({}, f)
        # Set permissions to owner-only (secure)
        os.chmod(PREFS_FILE, stat.S_IREAD | stat.S_IWRITE)

def save_preference(provider_id: str, key: str, value: Any) -> None:
    """
    Saves non-secret data like default_model or access_level to config file.
    Example: save_preference('google', 'default_model', 'gemini-1.5-pro')
    """
    _ensure_config_exists()
    
    try:
        with open(PREFS_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = {}

    if provider_id not in data:
        data[provider_id] = {}
    
    data[provider_id][key] = value

    with open(PREFS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_preference(provider_id: str, key: str) -> Optional[Any]:
    """Retrieves a preference value."""
    if not PREFS_FILE.exists():
        return None
    try:
        with open(PREFS_FILE, "r") as f:
            data = json.load(f)
            return data.get(provider_id, {}).get(key)
    except Exception:
        return None

def clear_all_data(provider_list: list) -> None:
    """Wipes both Keychain secrets and JSON preferences."""
    # 1. Clear Secrets
    for pid in provider_list:
        delete_key(pid)
    
    # 2. Clear Preferences
    if PREFS_FILE.exists():
        os.remove(PREFS_FILE)

# --- 3. Verification Utilities ---

def verify_github_access(token: str) -> str:
    """
    Pings GitHub to check the token's validity and scopes.
    Returns a human-readable access level string.
    """
    try:
        headers = {"Authorization": f"token {token}"}
        response = requests.head("https://api.github.com/user", headers=headers, timeout=5)
        
        if response.status_code == 401:
            return "Invalid Token"
        
        # GitHub returns scopes in the 'X-OAuth-Scopes' header
        scopes_header = response.headers.get("X-OAuth-Scopes", "")
        scopes = [s.strip() for s in scopes_header.split(",")]

        if "repo" in scopes:
            return "Full Access (Private & Public)"
        elif "public_repo" in scopes:
            return "Write Access (Public Only)"
        elif "read:user" in scopes or "user" in scopes:
            return "Read Only (User Data)"
        else:
            return "Limited/Read Only"
            
    except Exception as e:
        return f"Connection Error: {str(e)}"