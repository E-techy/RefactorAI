import keyring
import json
import requests
import os
import stat
from pathlib import Path
from typing import Optional, Dict, Any

# --- Constants ---
# Name of the application, used for configuration directory and service ID.
APP_NAME = "refactor-ai"
# Service ID used by keyring to identify stored credentials for this application.
APP_SERVICE_ID = "RefactorAI_CLI"
# Base directory for application configuration, typically ~/.refactor-ai.
CONFIG_DIR = Path.home() / f".{APP_NAME}"
# Path to the JSON file storing user preferences.
PREFS_FILE = CONFIG_DIR / "preferences.json"


def save_key(provider_id: str, api_key: str) -> None:
    """
    Saves API key securely to the OS Keychain.
    API keys are stored per provider (e.g., 'openai', 'google').
    """
    # Only save if the API key is not empty or just whitespace.
    if api_key and api_key.strip():
        keyring.set_password(APP_SERVICE_ID, provider_id, api_key.strip())

def get_key(provider_id: str) -> Optional[str]:
    """
    Retrieves API key from the OS Keychain.
    Returns None if the key is not found or an error occurs.
    """
    try:
        return keyring.get_password(APP_SERVICE_ID, provider_id)
    except Exception:
        # Catch any exceptions during retrieval (e.g., keyring not available, key not found)
        return None

def delete_key(provider_id: str) -> None:
    """
    Removes API key from Keychain for a specific provider.
    Handles cases where the password might not exist, preventing errors.
    """
    try:
        keyring.delete_password(APP_SERVICE_ID, provider_id)
    except keyring.errors.PasswordDeleteError:
        # If the password doesn't exist, an error is raised. We can safely ignore it.
        pass

# --- 2. Preference Storage (JSON) ---

def _ensure_config_exists():
    """
    Ensures that the application's configuration directory and preferences file exist.
    If the directory or file are missing, they are created.
    The preferences file is also secured with owner-only read/write permissions.
    """
    # Create the configuration directory if it doesn't already exist.
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    
    # Create an empty preferences file if it doesn't exist.
    if not PREFS_FILE.exists():
        with open(PREFS_FILE, "w") as f:
            json.dump({}, f)
        # Set permissions to owner-only (secure): read and write for the owner.
        os.chmod(PREFS_FILE, stat.S_IREAD | stat.S_IWRITE)

def save_preference(provider_id: str, key: str, value: Any) -> None:
    """
    Saves non-secret data like default_model or access_level to the config file.
    Preferences are stored in a nested structure: {provider_id: {key: value}}.
    Example: save_preference('google', 'default_model', 'gemini-1.5-pro')
    """
    _ensure_config_exists()
    
    try:
        # Load existing preferences from the file.
        with open(PREFS_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # If the file is empty, corrupted, or not found, initialize data as an empty dictionary.
        data = {}

    # Ensure the provider_id key exists in the data dictionary.
    if provider_id not in data:
        data[provider_id] = {}
    
    # Set or update the specific preference for the given provider.
    data[provider_id][key] = value

    # Write the updated preferences back to the file with a human-readable indentation.
    with open(PREFS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_preference(provider_id: str, key: str) -> Optional[Any]:
    """
    Retrieves a preference value for a specific provider and key.
    Returns None if the file, provider, or key is not found, or if an error occurs.
    """
    # If the preferences file doesn't exist, there are no preferences to retrieve.
    if not PREFS_FILE.exists():
        return None
    try:
        # Load preferences and attempt to retrieve the specific value.
        with open(PREFS_FILE, "r") as f:
            data = json.load(f)
            # Use .get() with default empty dicts to safely navigate nested structure without KeyError.
            return data.get(provider_id, {}).get(key)
    except Exception:
        # Catch any errors during file reading or JSON parsing.
        return None

def clear_all_data(provider_list: list) -> None:
    """
    Wipes both Keychain secrets and JSON preferences for a list of given providers.
    This function performs a complete cleanup of all stored user data.
    """
    # 1. Clear Secrets: Iterate through the list of providers and delete their API keys.
    for pid in provider_list:
        delete_key(pid)
    
    # 2. Clear Preferences: Remove the entire preferences file if it exists.
    if PREFS_FILE.exists():
        os.remove(PREFS_FILE)

# --- 3. Verification Utilities ---

def verify_github_access(token: str) -> str:
    """
    Pings GitHub's API to check the validity of a given token and its associated scopes.
    Returns a human-readable string indicating the access level granted by the token.
    """
    try:
        # Prepare headers with the Authorization token for GitHub API.
        headers = {"Authorization": f"token {token}"}
        # Send a HEAD request to the user endpoint to check authentication without fetching data.
        response = requests.head("https://api.github.com/user", headers=headers, timeout=5)
        
        # If the status code is 401, the token is invalid or expired.
        if response.status_code == 401:
            return "Invalid Token"
        
        # GitHub returns granted scopes in the 'X-OAuth-Scopes' header.
        scopes_header = response.headers.get("X-OAuth-Scopes", "")
        # Parse the comma-separated scopes into a list.
        scopes = [s.strip() for s in scopes_header.split(",")]

        # Determine access level based on the presence of specific scopes.
        if "repo" in scopes:
            return "Full Access (Private & Public)"
        elif "public_repo" in scopes:
            return "Write Access (Public Only)"
        elif "read:user" in scopes or "user" in scopes:
            return "Read Only (User Data)"
        else:
            # If no specific high-level scopes are found, assume limited or read-only access.
            return "Limited/Read Only"
            
    except Exception as e:
        # Catch any network or request-related errors.
        return f"Connection Error: {str(e)}"