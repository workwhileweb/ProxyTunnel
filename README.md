# ProxyTunnel Wrapper

A Python wrapper for proxytunnel.exe that automatically manages the executable and provides a simple interface for port forwarding.

## Installation

```bash
pip install proxytunnel
```

## Features

- Automatic download and management of proxytunnel.exe
- Simple Python interface for port forwarding
- Automatic cleanup of processes
- Find available ports automatically
- Process status monitoring
- Windows support
- Background process management

## Usage

### Basic Port Forwarding

```python
from proxytunnel import ProxyTunnel

# Create a ProxyTunnel instance
# This will automatically download proxytunnel.exe if it's not present
proxy = ProxyTunnel()

# Forward local port 8080 to remote proxy example.com:3128
process = proxy.forward(local_port=8080, remote_proxy="user:pass@example.com:3128")

# The process runs in the background
# To stop it:
process.terminate()
```

### Finding Available Ports

```python
from proxytunnel import ProxyTunnel

proxy = ProxyTunnel()

# Get a random available port
free_port = proxy.free_port()
print(f"Found available port: {free_port}")

# Use the free port for forwarding
process = proxy.forward(local_port=free_port, remote_proxy="http://user:pass@example.com:3128")
```

### Process Management

```python
from proxytunnel import ProxyTunnel

proxy = ProxyTunnel()
process = proxy.forward(local_port=8080, remote_proxy="http://user:pass@example.com:3128")

# Check if the process is running
if proxy.is_running():
    print("Proxy tunnel is active")

# Kill the process
proxy.kill()

# Verify process is stopped
if not proxy.is_running():
    print("Proxy tunnel is stopped")
```

### Automatic Cleanup

The ProxyTunnel wrapper automatically handles process cleanup:
- When the ProxyTunnel object is destroyed
- When the program exits
- When starting a new forward process (kills existing process)

```python
from proxytunnel import ProxyTunnel

# Create proxy instance
proxy = ProxyTunnel()

# Start forwarding
process1 = proxy.forward(local_port=8080, remote_proxy="example.com:3128")

# Starting another forward will automatically kill the previous process
process2 = proxy.forward(local_port=8081, remote_proxy="example.com:3128")

# No need to manually clean up - it's handled automatically when:
# - The program exits
# - The proxy object is destroyed
# - A new forward process is started
```

## Requirements

- Python 3.6 or higher
- Windows operating system
- Internet connection (for downloading proxytunnel.exe)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 