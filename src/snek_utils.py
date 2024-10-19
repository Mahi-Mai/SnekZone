from pathlib import Path
from typing import List, Union

def clean_path(pth: str) -> str:
    """
    Because windows is mean. Reformat
    filepaths so that they'll be compatible
    with Python.
    """
    pth = pth.replace("\\", "/")
    return pth

def list_files_pathlib(path_obj: Union[str, Path]='.') -> List[str]:
    """
    SOURCE https://www.geeksforgeeks.org/python-list-all-files-in-directory-and-subdirectories/#
    Recursively return a list of all files within
    a diretory.

    Args:
        - path_obj: Could be a string or Path, directory
        you want to inventory.
    Returns:
        List of filenames as strings.
    """
    path_lst = []

    if isinstance(path_obj, str):
        path_obj = Path(path)
    
    for entry in path_obj.iterdir():
        if entry.is_file():
            path_lst.append(str(entry))
        elif entry.is_dir():
            more_files = list_files_pathlib(entry)
            path_lst = path_lst + more_files

    path_lst = [clean_path(x) if '\\' in x else x for x in path_lst]
            
    return path_lst