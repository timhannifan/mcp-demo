"""Wait for a server to be ready."""

import os
import socket
import sys
import time

from dotenv import load_dotenv

load_dotenv()

host = sys.argv[1]
port = int(sys.argv[2])
timeout = int(os.getenv("WAIT_TIMEOUT", "30"))

deadline = time.time() + timeout
while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=1):
            print(f"Ready: {host}:{port}")
            sys.exit(0)
    except OSError:
        time.sleep(0.3)
print(f"Timeout waiting for {host}:{port}", file=sys.stderr)
sys.exit(1)
