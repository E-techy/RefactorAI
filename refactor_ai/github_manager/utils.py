from github import Github, Auth
from typing import Optional, Dict, Any
from refactor_ai.configuration_manager import secrets_manager

def get_github_client() -> Github:
    """
    Authenticates and returns the PyGithub client using the stored token.
    Raises an error if the token is missing.
    """
    token = secrets_manager.get_key("github")
    if not token:
        raise ValueError("GitHub token not found. Please run 'refactor configure github'.")
    
    auth = Auth.Token(token)
    return Github(auth=auth)

def standard_response(status: str, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """
    Creates a standardized response dictionary for MCP (Model Context Protocol).
    """
    return {
        "status": status,
        "message": message,
        "data": data or {}
    }