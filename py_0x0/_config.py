"""
Global configuration for py_0x0 client.
"""

from typing import Optional
from ._models import ValidationError


# ============================================================================
# Global Configuration Storage
# ============================================================================

_DEFAULT_SERVER = "https://0x0.st"
_DEFAULT_USER_AGENT = "py_0x0/0.1.0 (+https://github.com/RimMirK/py_0x0)"


# ============================================================================
# Configuration Functions
# ============================================================================


def set_default_server(server: str) -> None:
    """
    Set the default server for all uploads.
    
    Args:
        server: Server URL (e.g., 'https://0x0.st' or 'https://custom.0x0.server')
    
    Example:
        >>> set_default_server('https://custom-0x0-instance.com')
        >>> response = upload_0x0('file.txt')  # Uses custom server
    """
    global _DEFAULT_SERVER
    if not server.startswith('http'):
        raise ValidationError("Server URL must start with http:// or https://")
    _DEFAULT_SERVER = server


def get_default_server() -> str:
    """
    Get the current default server URL.
    
    Returns:
        Current default server URL
    
    Example:
        >>> print(get_default_server())
        https://0x0.st
    """
    global _DEFAULT_SERVER
    return _DEFAULT_SERVER


def set_user_agent(user_agent: str) -> None:
    """
    Set the User-Agent header for all requests.
    
    Args:
        user_agent: User-Agent string (e.g., 'MyApp/1.0')
    
    Example:
        >>> set_user_agent('MyApp/1.0 (+https://example.com)')
        >>> response = upload_0x0('file.txt')  # Uses custom User-Agent
    """
    global _DEFAULT_USER_AGENT
    if not user_agent or len(user_agent) == 0:
        raise ValidationError("User-Agent cannot be empty")
    _DEFAULT_USER_AGENT = user_agent


def get_user_agent() -> str:
    """
    Get the current User-Agent string.
    
    Returns:
        Current User-Agent string
    
    Example:
        >>> print(get_user_agent())
        py_0x0/0.1.0 (+https://github.com/RimMirK/py_0x0)
    """
    global _DEFAULT_USER_AGENT
    return _DEFAULT_USER_AGENT


def reset_configuration() -> None:
    """
    Reset all configuration to defaults.
    
    Example:
        >>> reset_configuration()
        >>> print(get_default_server())
        https://0x0.st
    """
    global _DEFAULT_SERVER, _DEFAULT_USER_AGENT
    _DEFAULT_SERVER = "https://0x0.st"
    _DEFAULT_USER_AGENT = "py_0x0/0.1.0 (+https://github.com/RimMirK/py_0x0)"
