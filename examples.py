"""
Examples of using py_0x0 client.
"""

import asyncio
from pathlib import Path
from py_0x0 import (
    upload_0x0, aupload_0x0, upload_many_0x0, aupload_many_0x0,
    get_0x0, aget_0x0, delete_0x0, adelete_0x0,
    set_expiration_0x0, aset_expiration_0x0
)


# =============================================================================
# Example 1: Simple synchronous upload with file path
# =============================================================================

def example_simple_sync():
    """Upload a single file with its path."""
    response = upload_0x0('readme.md')
    print(f"✓ Uploaded: {response.url}")
    print(f"  Filename: {response.filename}")
    print(f"  Size: {response.size} bytes")


# =============================================================================
# Example 2: Upload with file object
# =============================================================================

def example_file_object():
    """Upload using an open file object."""
    with open('readme.md', 'rb') as f:
        response = upload_0x0(f)
        print(f"✓ Uploaded: {response.url}")


# =============================================================================
# Example 3: Upload bytes directly
# =============================================================================

def example_bytes():
    """Upload bytes directly without writing to disk."""
    content = b"Hello World!"
    response = upload_0x0(content)
    print(f"✓ Uploaded bytes: {response.url}")


# =============================================================================
# Example 4: Upload with expiration
# =============================================================================

def example_expiration():
    """Upload file with custom expiration time."""
    response = upload_0x0(
        'readme.md',
        expiration='1 hour'  # Expires after 1 hour
    )
    print(f"✓ Uploaded with expiration: {response.url}")


# =============================================================================
# Example 5: Upload multiple files synchronously
# =============================================================================

def example_multiple_sync():
    """Upload multiple files (sequential)."""
    files = ['file1.txt', 'file2.pdf', 'image.png']
    responses = upload_many_0x0(files)
    
    for response in responses:
        print(f"✓ {response.filename} -> {response.url}")


# =============================================================================
# Example 6: Simple asynchronous upload
# =============================================================================

async def example_simple_async():
    """Upload a single file asynchronously."""
    response = await aupload_0x0('document.pdf')
    print(f"✓ Async uploaded: {response.url}")


# =============================================================================
# Example 7: Upload with Path object
# =============================================================================

async def example_path_object():
    """Upload using Path object from pathlib."""
    path = Path('data') / 'report.xlsx'
    response = await aupload_0x0(path)
    print(f"✓ Uploaded from Path: {response.url}")


# =============================================================================
# Example 8: Upload multiple files concurrently (truly parallel)
# =============================================================================

async def example_multiple_async():
    """Upload multiple files concurrently."""
    files = ['file1.txt', 'file2.pdf', 'image.png', 'video.mp4']
    responses = await aupload_many_0x0(files)
    
    for response in responses:
        print(f"✓ {response.filename} -> {response.url}")


# =============================================================================
# Example 9: Error handling
# =============================================================================

def example_error_handling():
    """Demonstrate error handling."""
    try:
        response = upload_0x0('nonexistent.txt')
    except FileNotFoundError:
        print("✗ File not found!")
    
    # Or suppress errors and get None
    response = upload_0x0('file.txt', raise_on_error=False)
    if response is None:
        print("✗ Upload failed (returned None)")
    else:
        print(f"✓ {response.url}")


# =============================================================================
# Example 10: Mixed types in batch upload
# =============================================================================

async def example_mixed_types():
    """Upload different types of files together."""
    files = [
        'local_file.txt',           # File path
        Path('data/report.pdf'),    # Path object
        b'Some content',             # Bytes
        open('image.png', 'rb'),    # File object
    ]
    
    responses = await aupload_many_0x0(files)
    for response in responses:
        print(f"✓ {response.filename} -> {response.url}")


# =============================================================================
# Example 11: Upload from remote URL
# =============================================================================

def example_remote_url():
    """Download and upload from a remote URL."""
    remote_file = 'https://example.com/archive.zip'
    response = upload_0x0(remote_file)
    print(f"✓ Downloaded and uploaded: {response.url}")


# =============================================================================
# Example 12: Custom server
# =============================================================================

async def example_custom_server():
    """Upload to a different 0x0 instance."""
    response = await aupload_0x0(
        'file.txt',
        server='https://custom.0x0.server'  # Use custom server
    )
    print(f"✓ Uploaded to custom server: {response.url}")


# =============================================================================
# Example 13: Advanced async with gathering multiple tasks
# =============================================================================

async def example_advanced_async():
    """Advanced async pattern - gather multiple independent uploads."""
    # Create tasks
    task1 = aupload_0x0('file1.txt', expiration='1 day')
    task2 = aupload_0x0('file2.pdf', expiration='7 days')
    task3 = aupload_0x0('file3.zip', expiration='30 days')
    
    # Run all concurrently
    responses = await asyncio.gather(task1, task2, task3)
    
    for response in responses:
        print(f"✓ {response.filename} -> {response.url}")


# =============================================================================
# Example 14: Full example - async with logging
# =============================================================================

async def example_full():
    """Complete example with logging and error handling."""
    files = ['readme.md', 'config.yml', 'data.json']
    
    print("Uploading files...\n")
    responses = await aupload_many_0x0(
        files,
        expiration='7 days',
        raise_on_error=False  # Don't fail on individual errors
    )
    
    for file_path, response in zip(files, responses):
        if response:
            print(f"✅ {file_path}")
            print(f"   URL: {response.url}")
            print(f"   Size: {response.size} bytes\n")
        else:
            print(f"❌ {file_path} failed to upload\n")


# =============================================================================
# Example 15: Configuration - Set default server
# =============================================================================

def example_config_server():
    """Set default server for all uploads."""
    from py_0x0 import set_default_server, get_default_server
    
    # Show current default
    print(f"Current server: {get_default_server()}")
    
    # Change default server
    set_default_server('https://custom-0x0-instance.com')
    print(f"New server: {get_default_server()}")
    
    # Now all uploads use the new server by default
    # response = upload_0x0('file.txt')  # Uses custom server


# =============================================================================
# Example 16: Configuration - Set User-Agent
# =============================================================================

def example_config_user_agent():
    """Set custom User-Agent for all requests."""
    from py_0x0 import set_user_agent, get_user_agent
    
    # Show current User-Agent
    print(f"Current User-Agent: {get_user_agent()}")
    
    # Set custom User-Agent
    set_user_agent('MyApp/2.0 (+https://myapp.com)')
    print(f"New User-Agent: {get_user_agent()}")
    
    # Now all requests use the new User-Agent


# =============================================================================
# Example 17: Configuration - Reset to defaults
# =============================================================================

def example_config_reset():
    """Reset configuration to defaults."""
    from py_0x0 import (
        set_default_server,
        set_user_agent,
        reset_configuration,
        get_default_server,
        get_user_agent,
    )
    
    # Change configuration
    set_default_server('https://custom.server')
    set_user_agent('CustomApp/1.0')
    print(f"Custom server: {get_default_server()}")
    print(f"Custom User-Agent: {get_user_agent()}")
    
    # Reset to defaults
    reset_configuration()
    print(f"Reset server: {get_default_server()}")
    print(f"Reset User-Agent: {get_user_agent()}")


# =============================================================================
# Example 18: Using configured defaults
# =============================================================================

def example_config_usage():
    """Upload using configured defaults."""
    from py_0x0 import set_default_server, upload_0x0
    
    # Configure once
    set_default_server('https://0x0.st')
    
    # Now all uploads use this server without specifying it
    # response = upload_0x0('file1.txt')
    # response = upload_0x0('file2.txt')  # Same server
    # response = upload_0x0('file3.txt')  # Same server


# =============================================================================
# Example 19: Download file from 0x0.st
# =============================================================================

def example_download():
    """Download file from 0x0.st."""
    from py_0x0 import get_0x0
    
    # Download to memory (as bytes)
    # content = get_0x0('abc123.pdf')
    
    # Download and save to disk
    # get_0x0('abc123.pdf', save_to='local_copy.pdf')
    
    print("✓ Download example - download file from 0x0.st")


# =============================================================================
# Example 20: Delete file from 0x0.st
# =============================================================================

def example_delete():
    """Delete file from 0x0.st."""
    from py_0x0 import delete_0x0
    
    # Delete file (requires correct deletion key)
    # success = delete_0x0('abc123.txt')
    # if success:
    #     print("✓ File deleted")
    
    print("✓ Delete example - delete file from 0x0.st")


# =============================================================================
# Example 21: Async download
# =============================================================================

async def example_async_download():
    """Download file asynchronously."""
    from py_0x0 import aget_0x0
    
    # Download to memory (async)
    # content = await aget_0x0('abc123.pdf')
    
    # Download and save to disk (async)
    # await aget_0x0('abc123.pdf', save_to='local_copy.pdf')
    
    print("✓ Async download example - download file asynchronously")


# =============================================================================
# Example 22: Async delete
# =============================================================================

async def example_async_delete():
    """Delete file asynchronously."""
    from py_0x0 import adelete_0x0
    
    # Delete file (async)
    # success = await adelete_0x0('abc123.txt')
    # if success:
    #     print("✓ File deleted")
    
    print("✓ Async delete example - delete file asynchronously")


# =============================================================================
# Example 23: Working with files end-to-end
# =============================================================================

async def example_full_workflow():
    """Complete workflow: upload, download, and delete."""
    from py_0x0 import aupload_0x0, aget_0x0, adelete_0x0
    
    # 1. Upload file
    # response = await aupload_0x0(b'Hello World')
    # file_url = response.url
    # print(f"Uploaded: {file_url}")
    
    # 2. Download file
    # content = await aget_0x0(file_url)
    # print(f"Downloaded: {len(content)} bytes")
    
    # 3. Delete file
    # success = await adelete_0x0(file_url)
    # print(f"Deleted: {success}")
    
    print("✓ Full workflow example - upload, download, and delete")


# =============================================================================
# Example 24: Delete file using token (sync)
# =============================================================================

def example_delete_with_token():
    """Delete a file using management token from upload."""
    from py_0x0 import upload_0x0, delete_0x0
    
    # Upload file and capture the management token
    # response = upload_0x0(b'Temporary file')
    # print(f"Uploaded: {response.url}")
    # print(f"Token: {response.token}")
    
    # Delete using token for proper authorization
    # success = delete_0x0(response.url, token=response.token)
    # print(f"✓ Deleted with token: {success}")
    
    print("✓ Delete with token example - use X-Token header for proper authorization")


# =============================================================================
# Example 25: Modify file expiration (sync)
# =============================================================================

def example_set_expiration():
    """Modify expiration time using management token."""
    from py_0x0 import upload_0x0, set_expiration_0x0
    
    # Upload file and get token
    # response = upload_0x0(b'Important file', expiration='1 hour')
    # print(f"Uploaded: {response.url}")
    
    # Extend expiration to 24 hours before it expires
    # success = set_expiration_0x0(response.url, expiration_time=24, token=response.token)
    # print(f"✓ Expiration updated: {success}")
    
    # Or set to specific time (milliseconds since epoch)
    # success = set_expiration_0x0(response.url, expiration_time=1704067200000, token=response.token)
    # print(f"✓ Expiration set to timestamp: {success}")
    
    print("✓ Expiration modification example - extend file lifetime with token")


# =============================================================================
# Example 26: Delete file using token (async)
# =============================================================================

async def example_async_delete_with_token():
    """Delete a file asynchronously using management token."""
    from py_0x0 import aupload_0x0, adelete_0x0
    
    # Upload file and capture the management token
    # response = await aupload_0x0(b'Temporary async file')
    # print(f"Uploaded: {response.url}")
    
    # Delete using token for proper authorization
    # success = await adelete_0x0(response.url, token=response.token)
    # print(f"✓ Deleted with token (async): {success}")
    
    print("✓ Async delete with token example - proper token-based deletion")


# =============================================================================
# Example 27: Modify file expiration (async)
# =============================================================================

async def example_async_set_expiration():
    """Modify expiration time asynchronously using management token."""
    from py_0x0 import aupload_0x0, aset_expiration_0x0
    
    # Upload file and get token
    # response = await aupload_0x0(b'Important async file', expiration='2 hours')
    # print(f"Uploaded: {response.url}")
    
    # Extend expiration to 48 hours
    # success = await aset_expiration_0x0(response.url, expiration_time=48, token=response.token)
    # print(f"✓ Expiration updated (async): {success}")
    
    print("✓ Async expiration modification - extend file lifetime asynchronously")


# =============================================================================
# Example 28: Complete token-based workflow
# =============================================================================

async def example_token_workflow():
    """Complete workflow using token-based management operations."""
    from py_0x0 import aupload_0x0, aget_0x0, aset_expiration_0x0, adelete_0x0
    
    # 1. Upload file with token
    # response = await aupload_0x0(b'Hello World', expiration='1 hour')
    # file_url = response.url
    # token = response.token
    # print(f"Uploaded: {file_url}")
    # print(f"Token: {token}")
    
    # 2. Download file
    # content = await aget_0x0(file_url)
    # print(f"Downloaded: {len(content)} bytes")
    
    # 3. Extend expiration time before it expires
    # success = await aset_expiration_0x0(file_url, 24, token)
    # print(f"Extended expiration: {success}")
    
    # 4. Delete file using token
    # success = await adelete_0x0(file_url, token=token)
    # print(f"Deleted: {success}")
    
    print("✓ Token workflow example - upload, download, extend lifetime, and delete")


if __name__ == '__main__':
    # Run examples
    print("=" * 70)
    print("PyPI_0x0 Examples")
    print("=" * 70)
    
    # Sync examples
    print("\n[Sync Examples]")
    print("\n1. Simple sync upload:")
    try:
        example_simple_sync()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n2. Upload with expiration:")
    try:
        example_expiration()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    # Async examples
    print("\n\n[Async Examples]")
    print("\n3. Simple async upload:")
    try:
        asyncio.run(example_simple_async())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n4. Multiple async uploads:")
    try:
        asyncio.run(example_multiple_async())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    # Configuration examples
    print("\n\n[Configuration Examples]")
    print("\n5. Set default server:")
    try:
        example_config_server()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n6. Set User-Agent:")
    try:
        example_config_user_agent()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n7. Reset configuration:")
    try:
        example_config_reset()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    # File management examples
    print("\n\n[File Management Examples]")
    print("\n8. Download file:")
    try:
        example_download()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n9. Delete file:")
    try:
        example_delete()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n10. Async download:")
    try:
        asyncio.run(example_async_download())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n11. Async delete:")
    try:
        asyncio.run(example_async_delete())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n12. Full workflow:")
    try:
        asyncio.run(example_full_workflow())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    # Token-based management examples
    print("\n\n[Token-Based Management Examples]")
    print("\n13. Delete with token (sync):")
    try:
        example_delete_with_token()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n14. Set expiration (sync):")
    try:
        example_set_expiration()
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n15. Delete with token (async):")
    try:
        asyncio.run(example_async_delete_with_token())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n16. Set expiration (async):")
    try:
        asyncio.run(example_async_set_expiration())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n17. Complete token workflow:")
    try:
        asyncio.run(example_token_workflow())
    except Exception as e:
        print(f"   (Skipped: {e})")
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
