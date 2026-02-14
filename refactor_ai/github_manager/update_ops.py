from typing import Dict, Any
from .utils import get_github_client, standard_response

def update_file_content(
    repo_name: str, 
    file_path: str, 
    new_content: str, 
    branch: str, 
    message: str = "Update file via RefactorAI"
) -> Dict[str, Any]:
    """
    Overwrites an existing file with new content.
    """
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        
        # We need the SHA of the file to update it
        contents = repo.get_contents(file_path, ref=branch)
        
        result = repo.update_file(
            path=file_path,
            message=message,
            content=new_content,
            sha=contents.sha,
            branch=branch
        )
        
        return standard_response(
            "success",
            f"File '{file_path}' updated successfully.",
            {"commit_sha": result['commit'].sha, "url": result['content'].html_url}
        )
    except Exception as e:
        return standard_response("error", f"Failed to update file: {str(e)}")

def append_to_file(
    repo_name: str,
    file_path: str,
    content_to_add: str,
    branch: str,
    message: str = "Append content via RefactorAI"
) -> Dict[str, Any]:
    """
    Reads a file, appends text to the end, and updates it.
    """
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        
        # 1. Get current content
        file_obj = repo.get_contents(file_path, ref=branch)
        decoded_content = file_obj.decoded_content.decode("utf-8")
        
        # 2. Append new content
        updated_content = decoded_content + "\n" + content_to_add
        
        # 3. Update file
        result = repo.update_file(
            path=file_path,
            message=message,
            content=updated_content,
            sha=file_obj.sha,
            branch=branch
        )
        
        return standard_response(
            "success",
            f"Content appended to '{file_path}'.",
            {"commit_sha": result['commit'].sha}
        )
    except Exception as e:
        return standard_response("error", f"Failed to append content: {str(e)}")