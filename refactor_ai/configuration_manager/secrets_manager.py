import keyring
from typing import Optional

# The unique service name for the OS keyring to identify our app's keys
APP_SERVICE_ID = "RefactorAI_CLI"

def save_key(provider_id: str, api_key: str) -> None:
    """
    Saves an API key securely to the OS Keychain/Credential Manager.
    
    Args:
        provider_id: The unique ID (e.g., 'openai', 'github').
        api_key: The actual secret key string.
    """
    if api_key and api_key.strip():
        # format: RefactorAI_CLI::openai
        keyring.set_password(APP_SERVICE_ID, provider_id, api_key.strip())

def get_key(provider_id: str) -> Optional[str]:
    """
    Retrieves the API key from the OS Keychain.
    Returns None if the key is not set.
    """
    try:
        return keyring.get_password(APP_SERVICE_ID, provider_id)
    except Exception:
        # In case of keyring errors (e.g., user denied access), return None
        return None

def delete_key(provider_id: str) -> None:
    """
    Removes a specific API key from the system.
    """
    try:
        keyring.delete_password(APP_SERVICE_ID, provider_id)
    except keyring.errors.PasswordDeleteError:
        # Pass silently if the password didn't exist anyway
        pass

def clear_all_keys(provider_list: list) -> None:
    """
    Iterates through all known providers and removes their keys.
    """
    for provider_id in provider_list:
        delete_key(provider_id)

def is_configured(provider_id: str) -> bool:
    """
    Helper to check if a key exists without revealing the key itself.
    Useful for UI status indicators (e.g. showing a checkmark).
    """
    return get_key(provider_id) is not None