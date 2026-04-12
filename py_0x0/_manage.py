"""
File management functions for py_0x0 client (download, delete, expiration control).
"""

from pathlib import Path
from typing import Optional, Union

import requests

from ._config import get_default_server, get_user_agent
from ._models import NetworkError, Py0x0Error, UploadError, ValidationError


# ============================================================================
# File Management API (Sync)
# ============================================================================


def get_0x0(
    file_url: str,
    save_to: Optional[Union[str, Path]] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> Optional[bytes]:
    """
    Download a file from 0x0.st.
    
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
        >>> # Download to memory
        >>> content = get_0x0('abc123.pdf')
        >>> 
        >>> # Download and save to disk
        >>> get_0x0('abc123.pdf', save_to='local_copy.pdf')
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
            response = requests.get(file_url, timeout=300, stream=True, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
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


def delete_0x0(
    file_url: str,
    token: Optional[str] = None,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> bool:
    """
    Delete a file from 0x0.st.
    
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
        >>> response = upload_0x0('file.txt')
        >>> # Delete using token from upload response
        >>> success = delete_0x0(response.url, token=response.token)
        >>> 
        >>> # Or just delete without token (may not work for some servers)
        >>> success = delete_0x0('abc123.txt')
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
            
            if token:
                # Use token-based deletion (POST with delete field)
                data = {
                    'token': token,
                    'delete': '',  # Field presence is enough
                }
                response = requests.post(
                    file_url,
                    data=data,
                    headers=headers,
                    timeout=300,
                )
            else:
                # Try HTTP DELETE method
                response = requests.delete(
                    file_url,
                    timeout=300,
                    headers=headers,
                )
            
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            # Check if it's a 404 (file not found) which could mean already deleted
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


def set_expiration_0x0(
    file_url: str,
    expiration_time: Union[int, str],
    token: str,
    server: Optional[str] = None,
    raise_on_error: bool = True,
) -> bool:
    """
    Set or modify expiration time for a file on 0x0.st.
    
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
        >>> response = upload_0x0('file.txt')
        >>> # Extend expiration to 24 hours
        >>> success = set_expiration_0x0(response.url, 24, response.token)
        >>> # Or set to specific timestamp (milliseconds since epoch)
        >>> success = set_expiration_0x0(response.url, 1704067200000, response.token)
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
            response = requests.post(
                file_url,
                data=data,
                headers=headers,
                timeout=300,
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
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


# Import Union type
from typing import Union  # noqa: E402, F401
