import os
import subprocess
import requests
import atexit
import socket
import zipfile
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
        """Ensures proxytunnel.exe exists, downloads and extracts if not present."""
        # Get the user's home directory
        home = str(Path.home())
        exe_dir = os.path.join(home, ".proxytunnel")
        bin_dir = os.path.join(exe_dir, "bin")
        self.exe_path = os.path.join(bin_dir, "proxytunnel.exe")

        # Create directories if they don't exist
        os.makedirs(bin_dir, exist_ok=True)

        # Check if executable exists
        if not os.path.exists(self.exe_path):
            print("Downloading proxytunnel zip...")
            # URL for the proxytunnel zip file
            home = "https://github.com/proxytunnel/proxytunnel/"
            url = home + "releases/download/v1.12.2/proxytunnel-v1.12.2-x86_64-windows-msys.zip"
            zip_path = os.path.join(exe_dir, "proxytunnel.zip")

            try:
                # Download zip file
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Extract zip file
                print("Extracting proxytunnel.exe...")
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(bin_dir)

                # Remove zip file after extraction
                # os.remove(zip_path)
                print("Successfully installed proxytunnel.exe")
            except Exception as e:
                raise RuntimeError(f"Failed to install proxytunnel.exe: {str(e)}")

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

    def parse_proxy(self, proxy: str) -> tuple[str, str | None, str]:
        """
        Parse the proxy string into components.

        Args:
            proxy (str): Proxy string in format http://user:pass@host:port

        Returns:
            tuple: (proxy_type, auth, address) where:
                - proxy_type: The proxy protocol (e.g., 'http')
                - auth: Basic auth string 'user:pass' or None if no auth
                - address: The proxy address in format 'host:port'
        """
        # Split protocol and rest
        if "://" in proxy:
            proxy_type, rest = proxy.split("://", 1)
        else:
            proxy_type, rest = "http", proxy

        # Split auth and address
        if "@" in rest:
            auth, address = rest.split("@", 1)
        else:
            auth, address = None, rest

        return proxy_type.lower(), auth, address

    def forward(self, local_port: int, remote_proxy: str) -> subprocess.Popen:
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

        local = f"127.0.0.1:{local_port}"
        _, auth, address = self.parse_proxy(remote_proxy)

        if auth:
            cmd = [self.exe_path, f"--standalone={local}", f"--proxyauth={auth}", f"--proxy={address}"]
        else:
            cmd = [self.exe_path, f"--standalone={local}", f"--proxy={address}"]

        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Proxy tunnel {self.process.pid} : {cmd}")
            return self.process
        except Exception as e:
            self.process = None
            raise RuntimeError(f"Failed to start proxytunnel: {str(e)}")

    def is_running(self) -> bool:
        """Check if the proxytunnel process is currently running"""
        if self.process:
            return self.process.poll() is None
        return False
