import os

__all__ = [
    'BASE_DIR',
    'base_path',
]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def base_path(*args):
    """Path relative to project base directory"""
    return os.path.join(BASE_DIR, *args)
