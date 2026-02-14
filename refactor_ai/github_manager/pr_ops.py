from typing import Dict, Any
from .utils import get_github_client, standard_response

def create_pull_request(
    repo_name: str,
    title: str,
    body: str,
    head: str,
    base: str = "main"
) -> Dict[str, Any]:
    """
    Creates a Pull Request.
    
    Args:
        head: The name of the branch where your changes are (e.g., "feature/ai-fix").
        base: The branch you want to merge into (e.g., "main").
    """
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head,
            base=base
        )
        
        return standard_response(
            "success",
            f"Pull Request created: {pr.html_url}",
            {"pr_number": pr.number, "url": pr.html_url, "state": pr.state}
        )
    except Exception as e:
        return standard_response("error", f"Failed to create PR: {str(e)}")