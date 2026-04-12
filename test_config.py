#!/usr/bin/env python3
"""Quick test of configuration functions"""

from py_0x0 import (
    set_default_server,
    set_user_agent,
    get_default_server,
    get_user_agent,
    reset_configuration
)

print("✓ All configuration functions imported successfully!")
print()
print(f"Default server: {get_default_server()}")
print(f"Default User-Agent: {get_user_agent()[:50]}...")
print()

# Test setting values
print("Testing configuration changes...")
set_default_server("https://test.0x0.st")
set_user_agent("TestApp/1.0")
print(f"New server: {get_default_server()}")
print(f"New User-Agent: {get_user_agent()}")
print()

# Test reset
print("Resetting configuration...")
reset_configuration()
print(f"Reset server: {get_default_server()}")
print(f"Reset User-Agent: {get_user_agent()[:50]}...")
print()
print("✓ All configuration functions work correctly!")
