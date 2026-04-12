"""
py_0x0: Python client for 0x0.st file hosting service.

Simple, minimal, and powerful:
    >>> from py_0x0 import upload_0x0, aupload_0x0
    >>> response = upload_0x0('file.txt')
    >>> print(response.url)
    
    >>> response = await aupload_0x0(open('file.txt', 'rb'))
    >>> print(response.url)

Supports multiple input types:
    - File paths: upload_0x0('/path/to/file.txt')
    - File objects: upload_0x0(open('file.txt', 'rb'))
    - Bytes: upload_0x0(b'content')
    - URLs: upload_0x0('https://example.com/file.zip')
    - Multiple files: upload_many_0x0([...])

For asynchronous: aupload_0x0, aupload_many_0x0
"""

from ._version import __version__

from ._core import (
    # Sync API - Upload
    upload_0x0,
    upload_many_0x0,
    # Sync API - Download & Manage
    get_0x0,
    delete_0x0,
    set_expiration_0x0,
    # Async API - Upload
    aupload_0x0,
    aupload_many_0x0,
    # Async API - Download & Manage
    aget_0x0,
    adelete_0x0,
    aset_expiration_0x0,
    # Data model
    UploadResponse,
    # Exceptions
    Py0x0Error,
    UploadError,
    ValidationError,
    NetworkError,
    # Configuration
    set_default_server,
    get_default_server,
    set_user_agent,
    get_user_agent,
    reset_configuration,
)

__all__ = [
    '__version__',
    'upload_0x0',
    'upload_many_0x0',
    'get_0x0',
    'delete_0x0',
    'set_expiration_0x0',
    'aupload_0x0',
    'aupload_many_0x0',
    'aget_0x0',
    'adelete_0x0',
    'aset_expiration_0x0',
    'UploadResponse',
    'Py0x0Error',
    'UploadError',
    'ValidationError',
    'NetworkError',
    'set_default_server',
    'get_default_server',
    'set_user_agent',
    'get_user_agent',
    'reset_configuration',
]