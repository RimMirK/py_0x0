# py_0x0 - Minimalistic Python Client for 0x0.st

A simple, minimal, and powerful Python client for uploading files to [0x0.st](https://0x0.st/).

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-green)](./LICENSE)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Full Documentation](#full-documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

✨ **Dead Simple** - No classes, no complex patterns
- 🔄 **Sync & Async** - `upload_0x0()` and `aupload_0x0()`
- 📦 **Multiple Input Types** - Paths, file objects, bytes, URLs
- 🚀 **Concurrent Uploads** - True parallelism with async
- 🎯 **Type-safe** - Full type hints, dataclass responses
- 🛡️ **Error Handling** - Custom exceptions
- 📚 **Fully Documented** - English docstrings throughout

## Installation

```bash
pip install py-0x0
```

## Quick Start

### Synchronous Usage

```python
from py_0x0 import upload_0x0

# Simple path
response = upload_0x0('file.pdf')
print(response.url)  # https://0x0.st/abc123.pdf

# With expiration
response = upload_0x0('secret.txt', expiration='1 hour')

# File object
with open('image.png', 'rb') as f:
    response = upload_0x0(f)

# Bytes
response = upload_0x0(b'content')

# Multiple files
from py_0x0 import upload_many_0x0
responses = upload_many_0x0(['a.txt', 'b.pdf', 'c.zip'])
```

### Asynchronous Usage

```python
from py_0x0 import aupload_0x0, aupload_many_0x0
import asyncio

# Single file
response = await aupload_0x0('document.pdf')

# Multiple files (concurrent - much faster!)
responses = await aupload_many_0x0(['a.txt', 'b.pdf', 'c.zip'])

# Full example
async def main():
    files = ['file1.txt', 'file2.pdf', 'image.png']
    responses = await aupload_many_0x0(
        files,
        expiration='7 days'
    )
    for r in responses:
        print(f"✓ {r.filename} -> {r.url}")

asyncio.run(main())
```

## Full Documentation

### API Functions

#### Synchronous

```python
upload_0x0(
    file_input: Union[str, Path, BinaryIO, bytes, bytearray],
    expiration: Optional[str] = None,
    server: str = "https://0x0.st",
    raise_on_error: bool = True,
) -> Optional[UploadResponse]
```

Upload a single file and get a response with the URL.

```python
upload_many_0x0(
    files: List[Union[str, Path, BinaryIO, bytes, bytearray]],
    expiration: Optional[str] = None,
    server: str = "https://0x0.st",
    raise_on_error: bool = True,
) -> List[Optional[UploadResponse]]
```

Upload multiple files sequentially.

#### Asynchronous

```python
async def aupload_0x0(...)  # Same as upload_0x0()
async def aupload_many_0x0(...)  # Same as upload_many_0x0()
```

Async versions using `httpx` for concurrent uploads.

#### File Management

```python
# Download file
get_0x0(file_url, save_to='local.txt')  # Sync
await aget_0x0(file_url, save_to='local.txt')  # Async

# Delete file  
delete_0x0(file_url)   # Sync - returns bool
await adelete_0x0(file_url)  # Async - returns bool
```

**Download:**
- `get_0x0(file_url, save_to=None)` - Download to disk or memory (sync)
- `aget_0x0(file_url, save_to=None)` - Download asynchronously

**Delete:**
- `delete_0x0(file_url)` - Delete file (sync, requires deletion key)
- `adelete_0x0(file_url)` - Delete file (async, requires deletion key)

### Response Object

```python
@dataclass
class UploadResponse:
    url: str                          # File URL
    filename: str                     # Uploaded filename
    size: int                         # File size in bytes
    expires_at: Optional[datetime]    # Expiration time
    hash: Optional[str]               # File hash
```

### Exceptions

```python
from py_0x0 import (
    Py0x0Error,       # Base
    UploadError,      # Upload failed
    ValidationError,  # Invalid input
    NetworkError,     # Network error
)

try:
    response = upload_0x0('file.txt')
except ValidationError:
    print("File not found")
except UploadError as e:
    print(f"Server error: {e}")
except NetworkError:
    print("Connection error")
```

## Examples

### Example 1: Simple Upload

```python
from py_0x0 import upload_0x0

response = upload_0x0('report.pdf')
print(f"Uploaded: {response.url}")
```

### Example 2: Expiration

```python
response = upload_0x0('secret.txt', expiration='1 hour')
```

### Example 3: Batch Upload (Async)

```python
import asyncio
from py_0x0 import aupload_many_0x0

async def upload_files():
    files = ['a.txt', 'b.pdf', 'c.zip', 'video.mp4']
    responses = await aupload_many_0x0(files)
    
    for r in responses:
        print(f"✓ {r.filename} ({r.size} bytes) -> {r.url}")

asyncio.run(upload_files())
```

### Example 4: Different Input Types

```python
from py_0x0 import upload_0x0
from pathlib import Path

# Path string
upload_0x0('file.txt')

# Path object
upload_0x0(Path('data') / 'file.txt')

# File object
with open('file.txt', 'rb') as f:
    upload_0x0(f)

# Bytes
upload_0x0(b'Hello World')

# Remote URL (download then upload)
upload_0x0('https://example.com/archive.zip')
```

### Example 5: Error Handling

```python
from py_0x0 import upload_0x0, UploadError

# Strict mode (default)
try:
    response = upload_0x0('file.txt')
except UploadError as e:
    print(f"Error: {e}")

# Silent mode
response = upload_0x0('file.txt', raise_on_error=False)
if response is None:
    print("Upload failed")
```

### Example 6: Custom Server

```python
response = upload_0x0(
    'file.txt',
    server='https://custom-0x0-instance.com'
)
```

### Example 7: Full Async Example

```python
import asyncio
from py_0x0 import aupload_many_0x0

async def main():
    # List of files to upload
    files = [
        'README.md',
        'requirements.txt',
        'config.yml',
        'data.json',
    ]
    
    print("Uploading files...")
    responses = await aupload_many_0x0(
        files,
        expiration='7 days',
        raise_on_error=False
    )
    
    print("\nResults:")
    for file, response in zip(files, responses):
        if response:
            print(f"✅ {file}")
            print(f"   URL: {response.url}")
        else:
            print(f"❌ {file} failed")

asyncio.run(main())
```

### Example 8: Download File

```python
from py_0x0 import get_0x0

# Download to memory (returns bytes)
content = get_0x0('abc123.pdf')

# Download and save to disk
get_0x0('abc123.pdf', save_to='local_copy.pdf')
```

### Example 9: Delete File

```python
from py_0x0 import delete_0x0

# Delete file (returns True/False)
success = delete_0x0('abc123.txt')
if success:
    print("File deleted")
else:
    print("Deletion failed")
```

### Example 10: Complete Async Workflow

```python
import asyncio
from py_0x0 import aupload_0x0, aget_0x0, adelete_0x0

async def workflow():
    # Upload
    response = await aupload_0x0(b'Hello World')
    print(f"Uploaded: {response.url}")
    
    # Download
    content = await aget_0x0(response.url)
    print(f"Downloaded: {len(content)} bytes")
    
    # Delete
    success = await adelete_0x0(response.url)
    print(f"Deleted: {success}")

asyncio.run(workflow())
```

### Example 11: Token-Based File Management

The `X-Token` returned after upload enables secure file management:

```python
from py_0x0 import upload_0x0, delete_0x0, set_expiration_0x0

# Upload and capture the management token
response = upload_0x0('document.pdf', expiration='1 hour')
print(f"URL: {response.url}")
print(f"Token: {response.token}")

# Extend expiration using token (before it expires)
success = set_expiration_0x0(response.url, expiration_time=24, token=response.token)
if success:
    print("✓ File lifetime extended to 24 hours")

# Later, delete using token for proper authorization
success = delete_0x0(response.url, token=response.token)
if success:
    print("✓ File deleted securely")
```

### Example 12: Async Token Management

```python
import asyncio
from py_0x0 import aupload_0x0, aget_0x0, aset_expiration_0x0, adelete_0x0

async def secure_workflow():
    # 1. Upload with initial expiration
    response = await aupload_0x0(b'Secret data', expiration='1 hour')
    token = response.token
    
    # 2. Download file
    content = await aget_0x0(response.url)
    print(f"Downloaded: {len(content)} bytes")
    
    # 3. Extend expiration if not done yet
    success = await aset_expiration_0x0(response.url, 48, token)
    if success:
        print("Extended to 48 hours")
    
    # 4. Delete using token
    success = await adelete_0x0(response.url, token=token)
    print(f"Deleted: {success}")

asyncio.run(secure_workflow())
```

### Example 13: Expiration Time Formats

```python
from py_0x0 import upload_0x0, set_expiration_0x0

response = upload_0x0('file.txt')
token = response.token

# Set expiration by hours
set_expiration_0x0(response.url, 24, token)        # 24 hours

# Set expiration by milliseconds since epoch
set_expiration_0x0(response.url, 1704067200000, token)  # Unix timestamp

# Alternative: pass as string
set_expiration_0x0(response.url, '72', token)      # 72 hours
```

## Common Expiration Values

- `'1 hour'`
- `'1 day'`
- `'7 days'`
- `'30 days'`
- `'1 year'`

See [0x0.st documentation](https://0x0.st/) for all options.

## Performance

### Sync vs Async Performance

Uploading 10 files:

- **Sync** (sequential): ~10 seconds
- **Async** (concurrent): ~3-4 seconds ⚡

Use async with `aupload_many_0x0()` for best performance!

## Configuration

### Set Default Server

Set a default server for all uploads without specifying it every time:

```python
from py_0x0 import set_default_server, upload_0x0

# Set default
set_default_server('https://custom-0x0-instance.com')

# Now all uploads use this server by default
response = upload_0x0('file1.txt')
response = upload_0x0('file2.txt')  # Same server
```

### Set User-Agent

Customize the User-Agent header for all requests:

```python
from py_0x0 import set_user_agent

# Set custom User-Agent
set_user_agent('MyApp/1.0 (+https://myapp.com)')

# All requests will now use this User-Agent
response = upload_0x0('file.txt')
```

### Get Current Configuration

```python
from py_0x0 import get_default_server, get_user_agent

print(get_default_server())  # Current server URL
print(get_user_agent())       # Current User-Agent string
```

### Reset Configuration

```python
from py_0x0 import reset_configuration

# Reset to defaults
reset_configuration()
```

### Configuration Functions

- `set_default_server(server: str)` - Set default 0x0 server
- `get_default_server() -> str` - Get current default server
- `set_user_agent(user_agent: str)` - Set custom User-Agent
- `get_user_agent() -> str` - Get current User-Agent
- `reset_configuration()` - Reset all to defaults

## Requirements

- Python 3.8+
- `requests >= 2.25.0`
- `httpx >= 0.23.0`

## Development

### Clone the repository

```bash
git clone https://github.com/RimMirK/py_0x0.git
cd py_0x0
```

### Run examples

```bash
python examples.py
```

### Run tests

```bash
pytest tests/  # (if available)
```

## Contributing

Contributions are welcome! Feel free to:

- Report bugs on [GitHub Issues](https://github.com/RimMirK/py_0x0/issues)
- Submit improvements via [Pull Requests](https://github.com/RimMirK/py_0x0/pulls)
- Suggest features in [Discussions](https://github.com/RimMirK/py_0x0/discussions)

## Related Projects

- [0x0.st](https://0x0.st/) - Official service
- [0x0 source](https://git.0x0.st/mia/0x0) - Server implementation

## License

GNU General Public License v3.0 - See [LICENSE](./LICENSE)

---

**Made with ❤️ for simple file sharing**
