from typing import Dict, Any
from .utils import get_github_client, standard_response

def create_new_repo(
    name: str, 
    private: bool = True, 
    description: str = "", 
    auto_init: bool = True
) -> Dict[str, Any]:
    """
    Creates a new repository for the authenticated user.
    """
    try:
        g = get_github_client()
        user = g.get_user()
        
        repo = user.create_repo(
            name=name,
            private=private,
            description=description,
            auto_init=auto_init  # Creates a README automatically
        )
        
        return standard_response(
            "success",
            f"Repository '{repo.full_name}' created successfully.",
            {"name": repo.full_name, "url": repo.html_url, "private": private}
        )
    except Exception as e:
        return standard_response("error", f"Failed to create repo: {str(e)}")