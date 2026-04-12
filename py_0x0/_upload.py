"""
Upload functions for py_0x0 client.
"""

from io import BytesIO
from pathlib import Path
from typing import BinaryIO, List, Optional, Union

import requests

from ._config import get_default_server, get_user_agent
from ._models import NetworkError, Py0x0Error, UploadError, UploadResponse
from ._utils import _normalize_file_input, _parse_upload_response


# ============================================================================
# Synchronous Upload API
# ============================================================================


def upload_0x0(
    file_input: Union[str, Path, BinaryIO, bytes, bytearray],
    expiration: Optional[str] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> Optional[UploadResponse]:
    """
    Upload a file to 0x0.st (synchronous).
    
    Supports multiple input types:
    - Path to file as string: upload_0x0('/path/to/file.txt')
    - Path object: upload_0x0(Path('/path/to/file.txt'))
    - File object: upload_0x0(open('file.txt', 'rb'))
    - Bytes: upload_0x0(b'file content')
    - URL: upload_0x0('https://example.com/file.zip')
    
    Args:
        file_input: File to upload (path, file object, or bytes).
        expiration: Expiration time as readable string (e.g., '1 hour', '7 days').
                   If None, server defaults apply.
        server: 0x0.st server URL. If None, uses default server set via set_default_server().
        raise_on_error: If False, returns None instead of raising exceptions.
    
    Returns:
        UploadResponse with URL and file metadata, or None if error and
        raise_on_error=False.
    
    Raises:
        ValidationError: If input validation fails.
        UploadError: If upload fails (when raise_on_error=True).
        NetworkError: If network communication fails.
    
    Example:
        >>> response = upload_0x0('document.pdf')
        >>> print(response.url)
        https://0x0.st/abc123.pdf
    """
    try:
        # Use default server if not specified
        if server is None:
            server = get_default_server()
        
        # Handle URL input (fetch from remote)
        if isinstance(file_input, str) and file_input.startswith('http'):
            try:
                file_obj = BytesIO()
                headers = {'User-Agent': get_user_agent()}
                with requests.get(file_input, timeout=30, stream=True, headers=headers) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=8192):
                        file_obj.write(chunk)
                file_obj.seek(0)
                filename = file_input.split('/')[-1].split('?')[0] or 'remote_file'
                size = len(file_obj.getvalue())
            except requests.RequestException as e:
                raise NetworkError(f"Failed to fetch remote file: {e}")
        else:
            file_obj, filename, size = _normalize_file_input(file_input)
        
        # Prepare upload
        files = {'file': (filename, file_obj)}
        data = {}
        
        if expiration:
            data['expiration'] = expiration
        
        # Send request
        try:
            headers = {'User-Agent': get_user_agent()}
            response = requests.post(
                f"{server.rstrip('/')}/",
                files=files,
                data=data if data else None,
                headers=headers,
                timeout=300,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise NetworkError(f"Upload request failed: {e}")
        
        # Parse response and extract X-Token from headers
        return _parse_upload_response(response.text, dict(response.headers), raise_on_error)
    
    except Py0x0Error:
        raise
    except Exception as e:
        if raise_on_error:
            raise NetworkError(f"Unexpected error during upload: {e}")
        return None


def upload_many_0x0(
    files: List[Union[str, Path, BinaryIO, bytes, bytearray]],
    expiration: Optional[str] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> List[Optional[UploadResponse]]:
    """
    Upload multiple files to 0x0.st (synchronous).
    
    Args:
        files: List of files to upload (same types as upload_0x0).
        expiration: Expiration time for all files.
        server: 0x0.st server URL. If None, uses default server.
        raise_on_error: If False, errors are ignored and None returned for failed uploads.
    
    Returns:
        List of UploadResponse objects (None for failed uploads if raise_on_error=False).
    
    Raises:
        ValidationError: If input validation fails (when raise_on_error=True).
        UploadError: If any upload fails (when raise_on_error=True).
    
    Example:
        >>> responses = upload_many_0x0(['file1.txt', 'file2.pdf'])
        >>> for r in responses:
        ...     print(r.url)
    """
    results = []
    for file_input in files:
        try:
            result = upload_0x0(
                file_input,
                expiration=expiration,
                server=server,
                raise_on_error=True,
            )
            results.append(result)
        except Py0x0Error as e:
            if raise_on_error:
                raise
            results.append(None)
    
    return results
