"""
File Tools for Collider Agent

Basic file operations: read, write, edit.
Following the pattern from AgentXploit analysis_agent.
"""

import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Constants
DEFAULT_MAX_LINES = 2000
MAX_LINE_LENGTH = 2000


def read(file_path: str, offset: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Reads a file from the local filesystem.

    Usage:
    - The file_path parameter must be an absolute path, not a relative path
    - By default, it reads up to 2000 lines starting from the beginning of the file
    - You can optionally specify a line offset and limit (especially handy for long files)
    - Any lines longer than 2000 characters will be truncated
    - Results are returned using cat -n format, with line numbers starting at 1

    Args:
        file_path: The absolute path to the file to read
        offset: The line number to start reading from (0-indexed internally, but output shows 1-indexed)
        limit: The number of lines to read

    Returns:
        dict: {
            "success": bool,
            "file_path": str,
            "content": str,
            "message": str
        }
    """
    try:
        abs_path = os.path.abspath(file_path)

        if not os.path.exists(abs_path):
            return {
                "success": False,
                "file_path": abs_path,
                "content": "",
                "message": f"File not found: {abs_path}"
            }

        if os.path.isdir(abs_path):
            return {
                "success": False,
                "file_path": abs_path,
                "content": "",
                "message": f"Path is a directory, not a file: {abs_path}"
            }

        with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)

        # Handle empty file
        if total_lines == 0:
            return {
                "success": True,
                "file_path": abs_path,
                "content": "[File is empty]",
                "message": f"File exists but has no content: {abs_path}"
            }

        # Apply offset and limit
        start_line = offset if offset is not None else 0
        max_lines = limit if limit is not None else DEFAULT_MAX_LINES

        # Clamp start_line to valid range
        start_line = max(0, min(start_line, total_lines - 1))

        # Select lines
        end_line = min(start_line + max_lines, total_lines)
        selected_lines = all_lines[start_line:end_line]

        # Format as cat -n output (line numbers starting at 1)
        formatted_lines = []
        for i, line in enumerate(selected_lines, start=start_line + 1):
            # Truncate long lines
            line = line.rstrip('\n\r')
            if len(line) > MAX_LINE_LENGTH:
                line = line[:MAX_LINE_LENGTH] + "... [truncated]"
            formatted_lines.append(f"{i:6}\t{line}")

        content = '\n'.join(formatted_lines)

        # Build message
        lines_read = len(selected_lines)
        if lines_read < total_lines:
            message = f"Read lines {start_line + 1}-{end_line} of {total_lines} from {abs_path}"
        else:
            message = f"Read {total_lines} lines from {abs_path}"

        return {
            "success": True,
            "file_path": abs_path,
            "content": content,
            "message": message
        }

    except Exception as e:
        logger.error(f"Read error: {e}", exc_info=True)
        return {
            "success": False,
            "file_path": os.path.abspath(file_path),
            "content": "",
            "message": f"Error: {str(e)}"
        }


def write(file_path: str, content: str) -> Dict[str, Any]:
    """
    Writes content to a file, creating directories if needed.

    Usage:
    - The file_path parameter must be an absolute path
    - This will overwrite existing files
    - Parent directories will be created if they don't exist

    Args:
        file_path: The absolute path to the file to write
        content: The content to write to the file

    Returns:
        dict: {
            "success": bool,
            "file_path": str,
            "bytes_written": int,
            "message": str
        }
    """
    try:
        abs_path = os.path.abspath(file_path)

        # Create parent directories if needed
        parent_dir = os.path.dirname(abs_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            logger.info(f"Created directory: {parent_dir}")

        # Write the file
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)

        bytes_written = len(content.encode('utf-8'))

        return {
            "success": True,
            "file_path": abs_path,
            "bytes_written": bytes_written,
            "message": f"Successfully wrote {bytes_written} bytes to {abs_path}"
        }

    except Exception as e:
        logger.error(f"Write error: {e}", exc_info=True)
        return {
            "success": False,
            "file_path": os.path.abspath(file_path),
            "bytes_written": 0,
            "message": f"Error: {str(e)}"
        }


def edit(file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> Dict[str, Any]:
    """
    Performs exact string replacement in a file.

    Usage:
    - The file_path parameter must be an absolute path
    - old_string must exist in the file (and be unique unless replace_all=True)
    - The edit will FAIL if old_string is not found or not unique (when replace_all=False)
    - Use replace_all=True to replace all occurrences

    Args:
        file_path: The absolute path to the file to modify
        old_string: The text to replace (must be different from new_string)
        new_string: The text to replace it with
        replace_all: If True, replace all occurrences; if False, old_string must be unique

    Returns:
        dict: {
            "success": bool,
            "file_path": str,
            "replacements": int,
            "message": str
        }
    """
    try:
        abs_path = os.path.abspath(file_path)

        if not os.path.exists(abs_path):
            return {
                "success": False,
                "file_path": abs_path,
                "replacements": 0,
                "message": f"File not found: {abs_path}"
            }

        if os.path.isdir(abs_path):
            return {
                "success": False,
                "file_path": abs_path,
                "replacements": 0,
                "message": f"Path is a directory, not a file: {abs_path}"
            }

        if old_string == new_string:
            return {
                "success": False,
                "file_path": abs_path,
                "replacements": 0,
                "message": "old_string and new_string must be different"
            }

        # Read the file
        with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Count occurrences
        count = content.count(old_string)

        if count == 0:
            return {
                "success": False,
                "file_path": abs_path,
                "replacements": 0,
                "message": f"old_string not found in file: {old_string[:100]}..."
            }

        if not replace_all and count > 1:
            return {
                "success": False,
                "file_path": abs_path,
                "replacements": 0,
                "message": f"old_string found {count} times. Use replace_all=True or provide more context to make it unique."
            }

        # Perform replacement
        if replace_all:
            new_content = content.replace(old_string, new_string)
            replacements = count
        else:
            new_content = content.replace(old_string, new_string, 1)
            replacements = 1

        # Write back
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return {
            "success": True,
            "file_path": abs_path,
            "replacements": replacements,
            "message": f"Successfully replaced {replacements} occurrence(s) in {abs_path}"
        }

    except Exception as e:
        logger.error(f"Edit error: {e}", exc_info=True)
        return {
            "success": False,
            "file_path": os.path.abspath(file_path),
            "replacements": 0,
            "message": f"Error: {str(e)}"
        }


__all__ = ["read", "write", "edit"]
