# ProxyTunnel Wrapper

A Python wrapper for proxytunnel.exe that automatically manages the executable and provides a simple interface for port forwarding.

## Installation

```bash
pip install proxytunnel-wrapper
```

## Usage

```python
from proxytunnel import ProxyTunnel

# Create a ProxyTunnel instance
# This will automatically download proxytunnel.exe if it's not present
proxy = ProxyTunnel()

# Forward local port 8080 to remote proxy example.com:3128
process = proxy.forward(local_port=8080, remote_proxy="example.com:3128")

# The process runs in the background
# To stop it:
process.terminate()
```

## Features

- Automatic download of proxytunnel.exe
- Simple Python interface for port forwarding
- Background process management
- Windows support

## Requirements

- Python 3.6 or higher
- Windows operating system
- Internet connection (for downloading proxytunnel.exe)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 