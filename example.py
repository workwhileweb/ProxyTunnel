#!/usr/bin/env python3

import asyncio
import time
import requests
from proxytunnel import ProxyTunnel
import os


async def main():
    # Example with HTTP proxy
    proxy = ProxyTunnel()

    proxy.forward(8080, os.getenv("PROXY"))

    # Wait a moment for proxy to start
    time.sleep(1)

    # Configure requests to use local proxy
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

    # Make request through proxy to get IP
    try:
        response = requests.get("https://api.ipify.org?format=json", proxies=proxies)
        print(f"Current IP: {response.json()['ip']}")
    except Exception as e:
        print(f"Failed to get IP: {e}")

    proxy.kill()


if __name__ == "__main__":
    asyncio.run(main())
