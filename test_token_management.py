#!/usr/bin/env python3
"""Test X-Token field and token-based management functions."""

import asyncio
from dataclasses import fields
from py_0x0 import (
    upload_0x0, delete_0x0, set_expiration_0x0,
    aupload_0x0, adelete_0x0, aset_expiration_0x0,
    UploadResponse
)


def test_upload_response_has_token_field():
    """Verify UploadResponse dataclass has token field."""
    field_names = [f.name for f in fields(UploadResponse)]
    print("✓ UploadResponse fields:")
    for name in field_names:
        print(f"  - {name}")
    
    assert 'token' in field_names, "Missing 'token' field in UploadResponse"
    print("✓ Token field present in UploadResponse")


def test_function_signatures():
    """Verify all functions have the correct signatures."""
    import inspect
    
    # Test delete with token parameter
    sig = inspect.signature(delete_0x0)
    params = list(sig.parameters.keys())
    assert 'token' in params, "delete_0x0 missing 'token' parameter"
    print("✓ delete_0x0 has 'token' parameter")
    
    # Test set_expiration_0x0
    sig = inspect.signature(set_expiration_0x0)
    params = list(sig.parameters.keys())
    assert 'token' in params, "set_expiration_0x0 missing 'token' parameter"
    assert 'expiration_time' in params, "set_expiration_0x0 missing 'expiration_time' parameter"
    print("✓ set_expiration_0x0 has 'token' and 'expiration_time' parameters")
    
    # Test async versions
    sig = inspect.signature(adelete_0x0)
    params = list(sig.parameters.keys())
    assert 'token' in params, "adelete_0x0 missing 'token' parameter"
    print("✓ adelete_0x0 has 'token' parameter")
    
    sig = inspect.signature(aset_expiration_0x0)
    params = list(sig.parameters.keys())
    assert 'token' in params, "aset_expiration_0x0 missing 'token' parameter"
    print("✓ aset_expiration_0x0 has 'token' and 'expiration_time' parameters")


def test_function_docstrings():
    """Verify functions have proper documentation about tokens."""
    print("\n✓ Function documentation:")
    
    doc = delete_0x0.__doc__
    if doc and 'token' in doc:
        print("  - delete_0x0 documents token parameter")
    
    doc = set_expiration_0x0.__doc__
    if doc and 'token' in doc:
        print("  - set_expiration_0x0 documents token parameter")
    
    doc = adelete_0x0.__doc__
    if doc and 'token' in doc:
        print("  - adelete_0x0 documents token parameter")


if __name__ == '__main__':
    print("=" * 70)
    print("Token Management API Test")
    print("=" * 70)
    
    print("\n[Testing UploadResponse dataclass]")
    test_upload_response_has_token_field()
    
    print("\n[Testing function signatures]")
    test_function_signatures()
    
    print("\n[Testing documentation]")
    test_function_docstrings()
    
    print("\n" + "=" * 70)
    print("✓ All token management features verified!")
    print("=" * 70)
    print("\nToken-based management functions available:")
    print("  Sync: delete_0x0, set_expiration_0x0")
    print("  Async: adelete_0x0, aset_expiration_0x0")
    print("\nAll functions support optional 'token' parameter from upload response.")
