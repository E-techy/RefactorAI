import os
import json
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional
from .utils import get_github_client, standard_response

def parse_github_url(url: str) -> Dict[str, str]:
    """
    Parses a GitHub URL to extract owner, repo, branch, and path.
    """
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL. Must be at least 'owner/repo'.")
    
    owner = parts[0]
    repo_name = parts[1]
    branch = None
    path = ""
    
    # Handle /tree/branch/path/to/folder
    if len(parts) > 3 and parts[2] == "tree":
        branch = parts[3]
        if len(parts) > 4:
            path = "/".join(parts[4:])
    elif len(parts) > 3 and parts[2] == "blob":
        branch = parts[3]
        if len(parts) > 4:
            path = "/".join(parts[4:])
    elif len(parts) > 2:
        # Fallback for URLs without 'tree' explicitly
        path = "/".join(parts[2:])

    return {
        "owner": owner,
        "repo": repo_name,
        "branch": branch,  # None implies default branch
        "path": path       # "" implies root
    }

def _build_tree_string(file_list: List[str], root_name: str = ".") -> str:
    """Generates a visual tree structure string."""
    tree_str = f"{root_name}/\n"
    sorted_files = sorted(file_list)
    
    for i, file_path in enumerate(sorted_files):
        is_last = (i == len(sorted_files) - 1)
        prefix = "└── " if is_last else "├── "
        tree_str += f"{prefix}{file_path}\n"
        
    return tree_str

def download_repo_content(
    url: str, 
    output_folder: str,
    metadata_filename: str = "repo_metadata.json",
    branch: Optional[str] = None,
    metadata_scope: str = "current"
) -> Dict[str, Any]:
    """
    Downloads files and generates metadata.
    """
    try:
        client = get_github_client()
        details = parse_github_url(url)
        
        full_repo_name = f"{details['owner']}/{details['repo']}"
        repo = client.get_repo(full_repo_name)
        
        if branch:
            details['branch'] = branch
        
        if not details['branch']:
            details['branch'] = repo.default_branch
            
        target_dir = os.path.abspath(output_folder)
        os.makedirs(target_dir, exist_ok=True)
        
        # --- Download Logic ---
        downloaded_files = []
        contents_queue = []
        
        root_contents = repo.get_contents(details['path'], ref=details['branch'])
        
        if isinstance(root_contents, list):
            contents_queue.extend(root_contents)
        else:
            contents_queue.append(root_contents)
            
        while contents_queue:
            file_content = contents_queue.pop(0)
            
            if file_content.type == "dir":
                contents_queue.extend(repo.get_contents(file_content.path, ref=details['branch']))
            else:
                if details['path']:
                    rel_path = os.path.relpath(file_content.path, details['path'])
                else:
                    rel_path = file_content.path
                
                local_path = os.path.join(target_dir, rel_path)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, "wb") as f:
                    f.write(file_content.decoded_content)
                
                downloaded_files.append(rel_path)

        # --- Metadata Logic ---
        files_for_tree = []
        tree_root_name = ""
        
        if metadata_scope == "all":
            try:
                # Fetch FULL git tree
                git_tree = repo.get_git_tree(sha=details['branch'], recursive=True)
                files_for_tree = [e.path for e in git_tree.tree if e.type == 'blob']
                tree_root_name = f"{details['repo']} (Full Repo)"
            except Exception:
                files_for_tree = downloaded_files
                tree_root_name = f"{os.path.basename(target_dir)} (Partial)"
        else:
            files_for_tree = downloaded_files
            tree_root_name = os.path.basename(target_dir)

        tree_view = _build_tree_string(files_for_tree, root_name=tree_root_name)
        
        metadata = {
            "source_url": url,
            "repo_name": full_repo_name,
            "branch": details['branch'],
            "base_path": details['path'],
            "metadata_scope": metadata_scope,
            # Visual Tree
            "structure_tree": tree_view,
            # Files available locally in this folder
            "downloaded_files": downloaded_files,
            # All files known in the scope (useful for AI context)
            "repo_all_files": files_for_tree,
            "local_root": target_dir
        }
        
        meta_path = os.path.join(target_dir, metadata_filename)
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        return standard_response(
            "success",
            f"Downloaded {len(downloaded_files)} files.",
            {
                "local_path": target_dir, 
                "metadata": meta_path, 
                "download_count": len(downloaded_files),
                "total_scope_count": len(files_for_tree)
            }
        )

    except Exception as e:
        return standard_response("error", f"Download failed: {str(e)}")