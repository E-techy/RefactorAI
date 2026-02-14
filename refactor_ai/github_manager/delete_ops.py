from typing import Dict, Any
from .utils import get_github_client, standard_response

def delete_file(
    repo_name: str, 
    file_path: str, 
    branch: str, 
    message: str = "Delete file via RefactorAI"
) -> Dict[str, Any]:
    """
    Deletes a specific file.
    """
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        
        contents = repo.get_contents(file_path, ref=branch)
        
        result = repo.delete_file(
            path=file_path,
            message=message,
            sha=contents.sha,
            branch=branch
        )
        
        return standard_response(
            "success", 
            f"File '{file_path}' deleted.",
            {"commit_sha": result['commit'].sha}
        )
    except Exception as e:
        return standard_response("error", f"Failed to delete file: {str(e)}")