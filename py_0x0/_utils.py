"""
Utility functions for py_0x0 client.
"""

from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Dict, Optional, Union

from ._models import UploadError, UploadResponse, ValidationError


# ============================================================================
# Utility Functions
# ============================================================================


def _normalize_file_input(
    file_input: Union[str, Path, BinaryIO, bytes, bytearray]
) -> tuple[BinaryIO, str, int]:
    """
    Normalize various file input types to (file_object, filename, size).
    
    Args:
        file_input: File path (str/Path), file object, or bytes.
    
    Returns:
        Tuple of (file_object, filename, size).
    
    Raises:
        ValidationError: If input is invalid.
    """
    # Handle file path (str or Path)
    if isinstance(file_input, (str, Path)):
        path = Path(file_input)
        if not path.exists():
            raise ValidationError(f"File not found: {path}")
        if not path.is_file():
            raise ValidationError(f"Path is not a file: {path}")
        
        size = path.stat().st_size
        return open(path, 'rb'), path.name, size
    
    # Handle file-like object
    if hasattr(file_input, 'read'):
        # Get filename if available
        if hasattr(file_input, 'name'):
            filename = Path(file_input.name).name
        else:
            filename = 'upload'
        
        # Get size
        if hasattr(file_input, 'seek') and hasattr(file_input, 'tell'):
            current_pos = file_input.tell()
            file_input.seek(0, 2)  # Seek to end
            size = file_input.tell()
            file_input.seek(current_pos)  # Restore position
        else:
            size = 0
        
        return file_input, filename, size
    
    # Handle bytes
    if isinstance(file_input, (bytes, bytearray)):
        file_obj = BytesIO(file_input)
        return file_obj, 'upload', len(file_input)
    
    raise ValidationError(
        f"Unsupported file input type: {type(file_input)}. "
        "Supported: str, Path, file object, bytes, bytearray"
    )


def _parse_upload_response(
    response_text: str,
    response_headers: Optional[Dict] = None,
    raise_on_error: bool = True
) -> Optional[UploadResponse]:
    """
    Parse response from 0x0.st upload.
    
    Args:
        response_text: Response body text.
        response_headers: Response headers dict (to extract X-Token).
        raise_on_error: If True, raise exception on error. If False, return None.
    
    Returns:
        UploadResponse or None if parsing fails.
    
    Raises:
        UploadError: If response indicates error and raise_on_error=True.
    """
    response_text = response_text.strip()
    
    # Check for error responses
    if response_text.startswith('error:'):
        error_msg = response_text.replace('error:', '').strip()
        if raise_on_error:
            raise UploadError(f"Upload failed: {error_msg}")
        return None
    
    # Response should be a URL
    if not response_text.startswith('http'):
        if raise_on_error:
            raise UploadError(f"Invalid response from server: {response_text}")
        return None
    
    # Extract filename from URL
    url_parts = response_text.rstrip('/').split('/')
    filename = url_parts[-1] if url_parts else 'unknown'
    
    # Extract X-Token from response headers
    token = None
    if response_headers:
        # Try case-insensitive header lookup
        token = response_headers.get('x-token') or response_headers.get('X-Token')
    
    return UploadResponse(
        url=response_text,
        filename=filename,
        size=0,  # 0x0.st doesn't return size in response
        token=token,
    )
