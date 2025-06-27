import os
import shutil
import logging

logger = logging.getLogger(__name__)


def read_text(path, default=None):
    """Return the contents of a text file or ``default`` on error."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("File not found: %s", path)
    except Exception as e:
        logger.error("Error reading file %s: %s", path, e)
    return default


def write_text(path, text):
    """Write ``text`` to ``path``. Returns ``True`` if successful."""
    try:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        logger.error("Error writing file %s: %s", path, e)
        return False


def list_dir(path):
    """Return a list of entries in ``path`` or an empty list on error."""
    try:
        return os.listdir(path)
    except FileNotFoundError:
        logger.error("Directory not found: %s", path)
    except Exception as e:
        logger.error("Error listing directory %s: %s", path, e)
    return []


def remove_path(path):
    """Remove a file or directory tree. Returns ``True`` if successful."""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except FileNotFoundError:
        logger.warning("Path not found for removal: %s", path)
    except PermissionError as e:
        logger.error("Permission error removing %s: %s", path, e)
    except Exception as e:
        logger.error("Error removing %s: %s", path, e)
    return False

__all__ = [
    "read_text",
    "write_text",
    "list_dir",
    "remove_path",
]
