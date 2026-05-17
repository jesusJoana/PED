import os
import sys

from src.client import UDPInfoClient
from src.server import UDPInfoServer


def main():
    """Arranca el servidor o el cliente segun el modo indicado."""
    host = os.environ.get("PED_HOST", "127.0.0.1")
    port = int(os.environ.get("PED_PORT", "16063"))

    if len(sys.argv) > 1 and sys.argv[1] == "client":
        client = UDPInfoClient(host=host, port=port)
        client.run_interactive()
        return

    server = UDPInfoServer(host=host, port=port)
    server.run()


if __name__ == "__main__":
    main()
