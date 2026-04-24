"""
Build and release information for py_0x0.
"""

__version__ = "1.0.0"
__author__ = "RimMirK"
__email__ = "me@RimMirK.dev"
__description__ = "Minimal Python client for 0x0.st file hosting service"
__url__ = "https://github.com/RimMirK/py_0x0"
__license__ = "GPLv3"

# Project metadata
PROJECT_NAME = "py_0x0"
PYTHON_REQUIRES = ">=3.8"

DEPENDENCIES = [
    "requests>=2.25.0",
    "httpx>=0.23.0",
]

DEV_DEPENDENCIES = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0",
    "flake8>=6.0.0",
    "mypy>=1.0",
    "isort>=5.11.0",
]

# Server defaults
DEFAULT_SERVER = "https://0x0.st"
DEFAULT_TIMEOUT = 300
CHUNK_SIZE = 8192

# Common expiration values
COMMON_EXPIRATIONS = [
    "1 hour",
    "1 day",
    "7 days",
    "30 days",
    "1 year",
]

if __name__ == "__main__":
    print(f"py_0x0 v{__version__}")
    print(f"Author: {__author__} <{__email__}>")
    print(f"URL: {__url__}")
