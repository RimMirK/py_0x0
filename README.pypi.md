# py_0x0 - Python Client for 0x0.st

[![PyPI](https://img.shields.io/pypi/v/py-0x0)](https://pypi.org/project/py-0x0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-green)](./LICENSE)

A **minimal**, **simple**, and **powerful** Python client for [0x0.st](https://0x0.st/) - the temporary file hosting service.

## Features

✨ **Simple API** - One function, multiple input types
- 🔄 **Sync & Async** - Both `upload_0x0()` and `aupload_0x0()` 
- 📦 **Flexible Input** - Paths, file objects, bytes, URLs, and more
- 🚀 **Concurrent Uploads** - True parallel uploads with async
- 🎯 **Type-safe** - Dataclass responses with full type hints
- 🛡️ **Error Handling** - Custom exceptions for precise error handling
- 📝 **Full Documentation** - Docstrings with comprehensive examples
- ⚡ **Zero Dependencies Hassle** - Just `requests` and `httpx`

## Installation

```bash
pip install py-0x0
```

## Quick Start

### Synchronous

```python
from py_0x0 import upload_0x0

# Upload from file path
response = upload_0x0('document.pdf')
print(response.url)  # https://0x0.st/abc123.pdf

# Upload from file object
with open('image.png', 'rb') as f:
    response = upload_0x0(f)

# Upload bytes directly
response = upload_0x0(b'Hello World')

# With expiration
response = upload_0x0('secret.txt', expiration='1 hour')

# Multiple files
from py_0x0 import upload_many_0x0
responses = upload_many_0x0(['file1.txt', 'file2.pdf'])
```

### Asynchronous

```python
from py_0x0 import aupload_0x0
import asyncio

# Single file
response = await aupload_0x0('document.pdf')

# Multiple files (concurrent)
from py_0x0 import aupload_many_0x0
responses = await aupload_many_0x0(['file1.txt', 'file2.pdf'])
```

## Supported Input Types

All functions support these input types seamlessly:

| Type | Example |
|------|---------|
| **File path** (str) | `upload_0x0('file.txt')` |
| **Path object** | `upload_0x0(Path('dir/file.txt'))` |
| **File object** | `upload_0x0(open('file.txt', 'rb'))` |
| **Bytes** | `upload_0x0(b'content')` |
| **BytesIO** | `upload_0x0(BytesIO(b'data'))` |
| **Remote URL** | `upload_0x0('https://example.com/file.zip')` |

## API Reference

### Main Functions

```python
# Sync API - Upload
from py_0x0 import upload_0x0, upload_many_0x0

response = upload_0x0('file.txt', expiration='7 days')
responses = upload_many_0x0(['file1.txt', 'file2.pdf'])

# Sync API - Manage
from py_0x0 import get_0x0, delete_0x0

content = get_0x0('abc123.pdf')          # Download
get_0x0('abc123.pdf', save_to='copy.pdf')  # Download & save
delete_0x0('abc123.txt')                 # Delete

# Async API - Upload
from py_0x0 import aupload_0x0, aupload_many_0x0

response = await aupload_0x0('file.txt')
responses = await aupload_many_0x0(['file1.txt', 'file2.pdf'])

# Async API - Manage
from py_0x0 import aget_0x0, adelete_0x0

content = await aget_0x0('abc123.pdf')
await aget_0x0('abc123.pdf', save_to='copy.pdf')
await adelete_0x0('abc123.txt')
```

### Functions Summary

| Function | Purpose |
|----------|---------|
| `upload_0x0()` | Upload single file (sync) |
| `upload_many_0x0()` | Upload multiple files (sync) |
| `get_0x0()` | Download file (sync) |
| `delete_0x0()` | Delete file (sync) |
| `set_expiration_0x0()` | Modify file expiration (sync) |
| `aupload_0x0()` | Upload single file (async) |
| `aupload_many_0x0()` | Upload multiple files (async) |
| `aget_0x0()` | Download file (async) |
| `adelete_0x0()` | Delete file (async) |
| `aset_expiration_0x0()` | Modify file expiration (async) |

### Response Object

All upload functions return `UploadResponse`:

```python
@dataclass
class UploadResponse:
    url: str                          # Direct URL to file
    filename: str                     # Uploaded filename
    size: int                         # File size in bytes
    expires_at: Optional[datetime]    # Expiration time
    hash: Optional[str]               # File hash
    token: Optional[str]              # Management token (for delete/expiration control)
```

### Exceptions

```python
from py_0x0 import (
    Py0x0Error,       # Base exception
    UploadError,      # Upload failed
    ValidationError,  # Bad input
    NetworkError,     # Connection error
)
```

## Examples

### Simple Upload

```python
from py_0x0 import upload_0x0

response = upload_0x0('report.pdf')
print(f"✓ Uploaded: {response.url}")
```

### Batch Upload

```python
from py_0x0 import upload_many_0x0

files = ['doc1.pdf', 'doc2.pdf', 'image.png']
responses = upload_many_0x0(files, expiration='7 days')

for response in responses:
    print(f"✓ {response.filename}: {response.url}")
```

### Concurrent Async Upload

```python
import asyncio
from py_0x0 import aupload_many_0x0

async def main():
    files = ['file1.txt', 'file2.pdf', 'video.mp4']
    responses = await aupload_many_0x0(files)
    for r in responses:
        print(f"✓ {r.url}")

asyncio.run(main())
```

### Upload from URL

```python
from py_0x0 import upload_0x0

response = upload_0x0('https://example.com/file.zip')
print(response.url)
```

### Error Handling

```python
from py_0x0 import upload_0x0, UploadError

try:
    response = upload_0x0('file.txt')
except UploadError as e:
    print(f"Upload failed: {e}")

# Or silent mode
response = upload_0x0('file.txt', raise_on_error=False)
```

### Download File

```python
from py_0x0 import get_0x0

# Download to memory
content = get_0x0('abc123.pdf')

# Download and save
get_0x0('abc123.pdf', save_to='local.pdf')
```

### Delete File

```python
from py_0x0 import delete_0x0

success = delete_0x0('abc123.txt')
print(f"Deleted: {success}")
```

### Secure File Management with Tokens

The `X-Token` returned after upload enables secure file operations:

```python
from py_0x0 import upload_0x0, delete_0x0, set_expiration_0x0

# Upload and capture the management token
response = upload_0x0('document.pdf', expiration='1 hour')
print(f"URL: {response.url}")
print(f"Token: {response.token}")

# Extend expiration time using token
success = set_expiration_0x0(response.url, expiration_time=24, token=response.token)
if success:
    print("✓ File lifetime extended to 24 hours")

# Delete using token for secure authorization
success = delete_0x0(response.url, token=response.token)
if success:
    print("✓ File deleted")
```

### Token Management (Async)

```python
import asyncio
from py_0x0 import aupload_0x0, aset_expiration_0x0, adelete_0x0

async def manage_file():
    # Upload with token
    response = await aupload_0x0(b'Secret data')
    token = response.token
    
    # Extend expiration (before expiry)
    await aset_expiration_0x0(response.url, 48, token)
    
    # Delete with token
    await adelete_0x0(response.url, token=token)

asyncio.run(manage_file())
```

### Complete Workflow

```python
import asyncio
from py_0x0 import aupload_0x0, aget_0x0, adelete_0x0

async def workflow():
    # Upload
    response = await aupload_0x0(b'Hello')
    
    # Download
    content = await aget_0x0(response.url)
    
    # Delete
    await adelete_0x0(response.url)

asyncio.run(workflow())
```

## Performance Tips

**Concurrent uploads are much faster:**

```python
import asyncio
from py_0x0 import aupload_many_0x0

# Uploading 10 files
# - Sync: ~10 seconds (sequential)
# - Async: ~3-4 seconds (concurrent) ⚡
responses = await aupload_many_0x0(files)
```

## Configuration

Configure default server and User-Agent once:

```python
from py_0x0 import set_default_server, set_user_agent, upload_0x0

# Set defaults
set_default_server('https://custom-0x0.server')
set_user_agent('MyApp/1.0 (+https://myapp.com)')

# Now all uploads use these defaults
response = upload_0x0('file.txt')
```

**Configuration Functions:**
- `set_default_server(server)` - Set default 0x0 server
- `get_default_server()` - Get current server
- `set_user_agent(user_agent)` - Set User-Agent
- `get_user_agent()` - Get current User-Agent
- `reset_configuration()` - Reset to defaults

## Requirements

- Python 3.8+
- `requests >= 2.25.0`
- `httpx >= 0.23.0`

## License

GNU General Public License v3.0

## Links

- [GitHub Repository](https://github.com/RimMirK/py_0x0)
- [0x0.st](https://0x0.st/)
- [PyPI](https://pypi.org/project/py-0x0/)