from typing import Dict, Any
from .utils import get_github_client, standard_response

def create_file(
    repo_name: str, 
    file_path: str, 
    content: str, 
    branch: str, 
    message: str = "Create file via RefactorAI"
) -> Dict[str, Any]:
    """
    Creates a new file in the repository.
    
    Args:
        repo_name: "owner/repo"
        file_path: "folder/filename.py"
        content: The text content of the file
        branch: The branch to commit to
        message: Commit message
    """
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        
        # PyGithub's create_file handles folder creation automatically if path has slashes
        result = repo.create_file(
            path=file_path,
            message=message,
            content=content,
            branch=branch
        )
        
        return standard_response(
            "success",
            f"File '{file_path}' created on branch '{branch}'.",
            {"commit_sha": result['commit'].sha, "url": result['content'].html_url}
        )
    except Exception as e:
        return standard_response("error", f"Failed to create file: {str(e)}")