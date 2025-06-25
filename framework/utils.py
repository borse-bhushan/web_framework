from pathlib import Path


def get_base_dir():
    """Get the base directory of the application."""
    return Path(__file__).resolve().parent.parent
