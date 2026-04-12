"""
Data models and exceptions for py_0x0 client.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# ============================================================================
# Exceptions
# ============================================================================


class Py0x0Error(Exception):
    """Base exception for py_0x0 client."""
    pass


class UploadError(Py0x0Error):
    """Raised when file upload fails."""
    pass


class ValidationError(Py0x0Error):
    """Raised when input validation fails."""
    pass


class NetworkError(Py0x0Error):
    """Raised when network communication fails."""
    pass


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class UploadResponse:
    """
    Response from 0x0.st upload.
    
    Attributes:
        url (str): Direct URL to the uploaded file.
        filename (str): Name of the uploaded file.
        size (int): File size in bytes.
        expires_at (datetime or None): When the file will expire (if available).
        hash (str or None): File hash (if available).
        token (str or None): Management token for file operations (delete, modify expiration).
                            Returned in X-Token HTTP header after upload.
    """
    url: str
    filename: str
    size: int
    expires_at: Optional[datetime] = None
    hash: Optional[str] = None
    token: Optional[str] = None
    
    def __repr__(self) -> str:
        return f"UploadResponse(url='{self.url}', filename='{self.filename}', size={self.size})"
