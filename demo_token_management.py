#!/usr/bin/env python3
"""
Demonstration of X-Token field usage for secure file management.

This shows how the token returned in X-Token HTTP header enables
secure file operations (delete and expiration modification).
"""

from dataclasses import asdict
from py_0x0 import UploadResponse


def demonstrate_token_based_management():
    """Show how tokens enable secure file management."""
    
    print("=" * 70)
    print("X-Token Based File Management")
    print("=" * 70)
    
    # Simulate an upload response with a token
    # In real usage, this comes from the X-Token header
    sample_response = UploadResponse(
        url="https://0x0.st/abc123.pdf",
        filename="document.pdf",
        size=1024000,
        expires_at=None,
        hash=None,
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Example token
    )
    
    print("\n1. Upload Response with Token:")
    print(f"   URL: {sample_response.url}")
    print(f"   Filename: {sample_response.filename}")
    print(f"   Size: {sample_response.size} bytes")
    print(f"   Token: {sample_response.token[:30]}...")
    
    print("\n2. Token-Based Operations:")
    print("\n   a) Delete with Token:")
    print(f"      from py_0x0 import delete_0x0")
    print(f"      success = delete_0x0('{sample_response.url}', token='{sample_response.token}')")
    print(f"      # Secure deletion using the token")
    
    print("\n   b) Modify Expiration with Token:")
    print(f"      from py_0x0 import set_expiration_0x0")
    print(f"      success = set_expiration_0x0('{sample_response.url}', 24, '{sample_response.token}')")
    print(f"      # Extend file lifetime to 24 hours using the token")
    
    print("\n3. Async Versions Available:")
    print("   from py_0x0 import adelete_0x0, aset_expiration_0x0")
    print("   await adelete_0x0(url, token=token)")
    print("   await aset_expiration_0x0(url, 48, token)")
    
    print("\n4. Token-Based Workflow:")
    print("""
   1. Upload file → receive X-Token in response
   2. Use token to delete file securely (POST with token field)
   3. Use token to modify expiration before it expires
   4. All operations are authorized via the token
   
   Example:
   --------
   response = upload_0x0('file.txt', expiration='1 hour')
   token = response.token
   
   # Before file expires, extend its lifetime
   set_expiration_0x0(response.url, 24, token)
   
   # Later, delete using the same token
   delete_0x0(response.url, token=token)
    """)
    
    print("\n" + "=" * 70)
    print("Token Management API - 0x0.st HTTP POST API Support")
    print("=" * 70)
    print("\nAccording to 0x0.st API documentation:")
    print("  POST to file URL with fields:")
    print("    - token:  management token (from X-Token header)")
    print("    - delete: field presence to delete file")
    print("    - expires: hours OR milliseconds since epoch")
    print("\npy_0x0 provides wrapper functions for these operations:")
    print("  - delete_0x0(url, token=token) → DELETE")
    print("  - set_expiration_0x0(url, time, token) → SET EXPIRATION")
    print("=" * 70)


if __name__ == '__main__':
    demonstrate_token_based_management()
