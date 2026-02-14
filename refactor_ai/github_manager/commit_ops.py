from typing import Dict, Any, List
from github import InputGitTreeElement
from .utils import get_github_client, standard_response

def commit_multiple_files(
    repo_name: str,
    file_changes: List[Dict[str, str]], 
    branch: str,
    message: str
) -> Dict[str, Any]:
    """
    Commits multiple files in a single commit (Atomic Commit).
    
    Args:
        file_changes: List of dicts [{"path": "dir/file.py", "content": "print('hello')"}, ...]
        branch: The branch name (must exist).
    """
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        
        # 1. Get the latest commit of the branch
        ref = repo.get_git_ref(f"heads/{branch}")
        latest_commit_sha = ref.object.sha
        base_tree = repo.get_git_commit(latest_commit_sha).tree
        
        # 2. Create Tree Elements (The blobs)
        element_list = []
        for file in file_changes:
            # We use '100644' for file (blob), 'type'='blob'
            element = InputGitTreeElement(
                path=file["path"],
                mode='100644',
                type='blob',
                content=file["content"]
            )
            element_list.append(element)
            
        # 3. Create a new Tree
        new_tree = repo.create_git_tree(element_list, base_tree)
        
        # 4. Create the Commit linking to the new Tree
        new_commit = repo.create_git_commit(message, new_tree, [repo.get_git_commit(latest_commit_sha)])
        
        # 5. Update the Branch Reference to point to new commit
        ref.edit(sha=new_commit.sha)
        
        return standard_response(
            "success",
            f"Committed {len(file_changes)} files to branch '{branch}'.",
            {"commit_sha": new_commit.sha, "tree_sha": new_tree.sha}
        )
    except Exception as e:
        return standard_response("error", f"Failed to commit multiple files: {str(e)}")