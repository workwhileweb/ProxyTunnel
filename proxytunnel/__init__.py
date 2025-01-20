import os
import sys
import subprocess
import requests
import atexit
import socket
from pathlib import Path


class ProxyTunnel:
    def __init__(self):
        self.exe_path = None
        self.process = None
        self._ensure_executable()
        # Register cleanup on program exit
        atexit.register(self.kill)

    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.kill()

    @staticmethod
    def free_port() -> int:
        """
        Find a free port on localhost.

        Returns:
            int: An available port number
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))  # Bind to any available port
            s.listen(1)
            port = s.getsockname()[1]
            return port

    def _ensure_executable(self):
        """Ensures proxytunnel.exe exists, downloads if not present."""
        # Get the user's home directory
        home = str(Path.home())
        exe_dir = os.path.join(home, ".proxytunnel")
        self.exe_path = os.path.join(exe_dir, "proxytunnel.exe")

        # Create directory if it doesn't exist
        os.makedirs(exe_dir, exist_ok=True)

        # Check if executable exists
        if not os.path.exists(self.exe_path):
            print("Downloading proxytunnel.exe...")
            # URL for the proxytunnel executable
            url = "https://github.com/proxytunnel/proxytunnel/releases/latest/download/proxytunnel.exe"
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(self.exe_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Successfully downloaded proxytunnel.exe")
            except Exception as e:
                raise RuntimeError(f"Failed to download proxytunnel.exe: {str(e)}")

    def kill(self):
        """Kill the running proxytunnel process if it exists"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)  # Wait up to 5 seconds for process to terminate
            except subprocess.TimeoutExpired:
                self.process.kill()  # Force kill if it doesn't terminate
            finally:
                self.process = None

    def forward(self, local_port: int, remote_proxy: str):
        """
        Forward local port to remote proxy using proxytunnel.exe

        Args:
            local_port (int): Local port to forward from
            remote_proxy (str): Remote proxy address in format host:port
        """
        # Kill any existing process before starting a new one
        self.kill()

        if not self.exe_path or not os.path.exists(self.exe_path):
            raise RuntimeError("proxytunnel.exe not found")

        cmd = [self.exe_path, "-L", str(local_port), "-P", remote_proxy]

        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return self.process
        except Exception as e:
            self.process = None
            raise RuntimeError(f"Failed to start proxytunnel: {str(e)}")

    def is_running(self) -> bool:
        """Check if the proxytunnel process is currently running"""
        if self.process:
            return self.process.poll() is None
        return False
