from typing import Dict, Any
from .utils import get_github_client, standard_response

def create_branch(repo_name: str, new_branch: str, source_branch: str = "main") -> Dict[str, Any]:
    """
    Creates a new branch from a source branch.
    
    Args:
        repo_name: "owner/repo"
        new_branch: Name of the new branch (e.g., "feature/ai-fix")
        source_branch: The branch to copy from (default: "main")
    """
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        
        # Get the SHA of the source branch
        source_sha = repo.get_branch(source_branch).commit.sha
        
        # Create the new reference
        ref = repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source_sha)
        
        return standard_response(
            "success", 
            f"Branch '{new_branch}' created successfully from '{source_branch}'.",
            {"branch": new_branch, "sha": ref.object.sha}
        )
    except Exception as e:
        return standard_response("error", f"Failed to create branch: {str(e)}")

def get_branch_info(repo_name: str, branch_name: str) -> Dict[str, Any]:
    """Checks if a branch exists and gets its details."""
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        branch = repo.get_branch(branch_name)
        
        return standard_response(
            "success",
            f"Branch '{branch_name}' found.",
            {"name": branch.name, "sha": branch.commit.sha}
        )
    except Exception:
        return standard_response("error", f"Branch '{branch_name}' not found.")