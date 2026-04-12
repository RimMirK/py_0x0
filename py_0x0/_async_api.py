"""
Asynchronous API functions for py_0x0 client.
"""

import asyncio
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, List, Optional, Union

import httpx

from ._config import get_default_server, get_user_agent
from ._models import NetworkError, Py0x0Error, UploadError, UploadResponse, ValidationError
from ._utils import _normalize_file_input, _parse_upload_response


# ============================================================================
# Asynchronous Upload API
# ============================================================================


async def aupload_0x0(
    file_input: Union[str, Path, BinaryIO, bytes, bytearray],
    expiration: Optional[str] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> Optional[UploadResponse]:
    """
    Upload a file to 0x0.st (asynchronous).
    
    All features same as upload_0x0, but async version using httpx.
    
    Args:
        file_input: File to upload (path, file object, or bytes).
        expiration: Expiration time as readable string.
        server: 0x0.st server URL. If None, uses default server.
        raise_on_error: If False, returns None instead of raising exceptions.
    
    Returns:
        UploadResponse with URL and file metadata.
    
    Raises:
        ValidationError: If input validation fails.
        UploadError: If upload fails.
        NetworkError: If network communication fails.
    
    Example:
        >>> response = await aupload_0x0('document.pdf')
        >>> print(response.url)
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
                async with httpx.AsyncClient(headers=headers) as client:
                    async with client.stream('GET', file_input, timeout=30) as r:
                        r.raise_for_status()
                        async for chunk in r.aiter_bytes(chunk_size=8192):
                            file_obj.write(chunk)
                file_obj.seek(0)
                filename = file_input.split('/')[-1].split('?')[0] or 'remote_file'
                size = len(file_obj.getvalue())
            except httpx.RequestError as e:
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
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(
                    f"{server.rstrip('/')}/",
                    files=files,
                    data=data if data else None,
                    timeout=300,
                )
                response.raise_for_status()
        except httpx.RequestError as e:
            raise NetworkError(f"Upload request failed: {e}")
        
        # Parse response and extract X-Token from headers
        return _parse_upload_response(response.text, dict(response.headers), raise_on_error)
    
    except Py0x0Error:
        raise
    except Exception as e:
        if raise_on_error:
            raise NetworkError(f"Unexpected error during upload: {e}")
        return None


async def aupload_many_0x0(
    files: List[Union[str, Path, BinaryIO, bytes, bytearray]],
    expiration: Optional[str] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> List[Optional[UploadResponse]]:
    """
    Upload multiple files to 0x0.st concurrently (asynchronous).
    
    Args:
        files: List of files to upload.
        expiration: Expiration time for all files.
        server: 0x0.st server URL. If None, uses default server.
        raise_on_error: If False, errors are ignored for individual uploads.
    
    Returns:
        List of UploadResponse objects (or None for failed uploads).
    
    Example:
        >>> responses = await aupload_many_0x0(['file1.txt', 'file2.pdf'])
    """
    tasks = []
    for file_input in files:
        tasks.append(
            aupload_0x0(
                file_input,
                expiration=expiration,
                server=server,
                raise_on_error=raise_on_error,
            )
        )
    
    return await asyncio.gather(*tasks, return_exceptions=not raise_on_error)


# ============================================================================
# Asynchronous File Management API
# ============================================================================


async def aget_0x0(
    file_url: str,
    save_to: Optional[Union[str, Path]] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> Optional[bytes]:
    """
    Download a file from 0x0.st (asynchronous).
    
    Args:
        file_url: URL of the file on 0x0.st (can be full URL or just path like 'abc123.txt')
        save_to: Optional path to save file locally. If None, returns bytes.
        server: 0x0.st server URL. If None, uses default server.
        raise_on_error: If False, returns None instead of raising exceptions.
    
    Returns:
        File content as bytes if save_to is None, else None.
    
    Raises:
        ValidationError: If URL is invalid.
        NetworkError: If download fails.
    
    Example:
        >>> # Download to memory (async)
        >>> content = await aget_0x0('abc123.pdf')
        >>> 
        >>> # Download and save to disk (async)
        >>> await aget_0x0('abc123.pdf', save_to='local_copy.pdf')
    """
    try:
        if server is None:
            server = get_default_server()
        
        # Normalize URL
        if not file_url.startswith('http'):
            file_url = f"{server.rstrip('/')}/{file_url}"
        
        # Download file
        try:
            headers = {'User-Agent': get_user_agent()}
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(file_url, timeout=300)
                response.raise_for_status()
        except httpx.RequestError as e:
            raise NetworkError(f"Failed to download file: {e}")
        
        content = response.content
        
        # Save to disk if requested
        if save_to:
            path = Path(save_to)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            return None
        
        return content
    
    except Py0x0Error:
        raise
    except Exception as e:
        if raise_on_error:
            raise NetworkError(f"Unexpected error during download: {e}")
        return None


async def adelete_0x0(
    file_url: str,
    token: Optional[str] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> bool:
    """
    Delete a file from 0x0.st (asynchronous).
    
    Args:
        file_url: URL of the file (full URL or just path like 'abc123.txt')
        token: Management token from upload response (X-Token header).
               If provided, uses token-based deletion (POST request).
               If None, tries DELETE method.
        server: 0x0.st server URL. If None, uses default server.
        raise_on_error: If False, returns False instead of raising exceptions.
    
    Returns:
        True if deletion was successful, False otherwise.
    
    Raises:
        ValidationError: If URL is invalid.
        UploadError: If deletion fails.
        NetworkError: If request fails.
    
    Example:
        >>> response = await aupload_0x0('file.txt')
        >>> # Delete using token from upload response
        >>> success = await adelete_0x0(response.url, token=response.token)
    """
    try:
        if server is None:
            server = get_default_server()
        
        # Normalize URL
        if not file_url.startswith('http'):
            file_url = f"{server.rstrip('/')}/{file_url}"
        
        # Try to delete
        try:
            headers = {'User-Agent': get_user_agent()}
            async with httpx.AsyncClient(headers=headers) as client:
                if token:
                    # Use token-based deletion (POST with delete field)
                    data = {
                        'token': token,
                        'delete': '',  # Field presence is enough
                    }
                    response = await client.post(
                        file_url,
                        data=data,
                        timeout=300,
                    )
                else:
                    # Try HTTP DELETE method
                    response = await client.delete(
                        file_url,
                        timeout=300,
                    )
                
                response.raise_for_status()
            return True
        except httpx.RequestError as e:
            # Check if it's a 404 (file not found)
            if '404' in str(e):
                if raise_on_error:
                    raise UploadError(f"File not found: {file_url}")
                return False
            raise NetworkError(f"Failed to delete file: {e}")
    
    except Py0x0Error:
        if raise_on_error:
            raise
        return False
    except Exception as e:
        if raise_on_error:
            raise NetworkError(f"Unexpected error during deletion: {e}")
        return False


async def aset_expiration_0x0(
    file_url: str,
    expiration_time: Union[int, str],
    token: str,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> bool:
    """
    Set or modify expiration time for a file on 0x0.st (asynchronous).
    
    Args:
        file_url: URL of the file (full URL or just path like 'abc123.txt').
        expiration_time: Expiration time in hours (int) or milliseconds since epoch (int),
                        or readable string like '24' (hours) or '1704067200000' (ms).
        token: Management token from upload response (X-Token header).
        server: 0x0.st server URL. If None, uses default server.
        raise_on_error: If False, returns False instead of raising exceptions.
    
    Returns:
        True if expiration was set successfully, False otherwise.
    
    Raises:
        ValidationError: If inputs are invalid.
        UploadError: If operation fails.
        NetworkError: If request fails.
    
    Example:
        >>> response = await aupload_0x0('file.txt')
        >>> # Extend expiration to 24 hours
        >>> success = await aset_expiration_0x0(response.url, 24, response.token)
    """
    try:
        if not token:
            raise ValidationError("Token is required for expiration management")
        
        if server is None:
            server = get_default_server()
        
        # Normalize URL
        if not file_url.startswith('http'):
            file_url = f"{server.rstrip('/')}/{file_url}"
        
        # Prepare data
        data = {
            'token': token,
            'expires': str(expiration_time),
        }
        
        # Send POST request to manage file
        try:
            headers = {'User-Agent': get_user_agent()}
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(
                    file_url,
                    data=data,
                    timeout=300,
                )
                response.raise_for_status()
            return True
        except httpx.RequestError as e:
            if '404' in str(e):
                if raise_on_error:
                    raise UploadError(f"File not found: {file_url}")
                return False
            raise NetworkError(f"Failed to set expiration: {e}")
    
    except Py0x0Error:
        if raise_on_error:
            raise
        return False
    except Exception as e:
        if raise_on_error:
            raise NetworkError(f"Unexpected error during expiration update: {e}")
        return False
