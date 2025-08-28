import socket, sys, time

host = sys.argv[1]
port = int(sys.argv[2])
timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 30

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
