"""
File utility functions for the XCUI Test Agent
"""

from pathlib import Path
from typing import List, Optional


def find_swift_files(
    directory: str,
    exclude_patterns: Optional[List[str]] = None
) -> List[Path]:
    """
    Find all Swift files in a directory
    
    Args:
        directory: Directory to search
        exclude_patterns: List of patterns to exclude (e.g., '*Tests.swift')
    
    Returns:
        List of Path objects for Swift files
    """
    exclude_patterns = exclude_patterns or []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    swift_files = []
    
    for swift_file in directory_path.rglob("*.swift"):
        # Check if file matches any exclude pattern
        should_exclude = False
        for pattern in exclude_patterns:
            if swift_file.match(pattern):
                should_exclude = True
                break
        
        if not should_exclude:
            swift_files.append(swift_file)
    
    return swift_files


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        path: Directory path
    
    Returns:
        Path object
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def read_file_content(file_path: str) -> str:
    """
    Read file content with proper encoding
    
    Args:
        file_path: Path to file
    
    Returns:
        File content as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file_content(file_path: str, content: str) -> None:
    """
    Write content to file with proper encoding
    
    Args:
        file_path: Path to file
        content: Content to write
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_relative_path(file_path: str, base_path: str) -> str:
    """
    Get relative path from base path
    
    Args:
        file_path: Full file path
        base_path: Base directory path
    
    Returns:
        Relative path as string
    """
    return str(Path(file_path).relative_to(base_path))

# Made with Bob
