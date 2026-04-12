"""
Core functionality for 0x0.st Python client.

This module provides re-exports from submodules for backward compatibility.
All functionality is split into separate modules for better organization.
"""

# Re-export models and exceptions
from ._models import (
    NetworkError,
    Py0x0Error,
    UploadError,
    UploadResponse,
    ValidationError,
)

# Re-export configuration functions
from ._config import (
    get_default_server,
    get_user_agent,
    reset_configuration,
    set_default_server,
    set_user_agent,
)

# Re-export utility functions (private, but needed for internal use)
from ._utils import _normalize_file_input, _parse_upload_response

# Re-export sync upload functions
from ._upload import upload_0x0, upload_many_0x0

# Re-export sync management functions
from ._manage import delete_0x0, get_0x0, set_expiration_0x0

# Re-export async functions
from ._async_api import (
    adelete_0x0,
    aget_0x0,
    aset_expiration_0x0,
    aupload_0x0,
    aupload_many_0x0,
)

__all__ = [
    # Models
    'UploadResponse',
    # Exceptions
    'Py0x0Error',
    'UploadError',
    'ValidationError',
    'NetworkError',
    # Configuration
    'set_default_server',
    'get_default_server',
    'set_user_agent',
    'get_user_agent',
    'reset_configuration',
    # Upload (sync)
    'upload_0x0',
    'upload_many_0x0',
    # File Management (sync)
    'get_0x0',
    'delete_0x0',
    'set_expiration_0x0',
    # Upload (async)
    'aupload_0x0',
    'aupload_many_0x0',
    # File Management (async)
    'aget_0x0',
    'adelete_0x0',
    'aset_expiration_0x0',
]
