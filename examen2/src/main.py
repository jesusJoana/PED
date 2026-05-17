import sys

from src.client import UDPInfoClient
from src.server import UDPInfoServer


def main():
    """Arranca el servidor o el cliente segun el modo indicado."""
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        client = UDPInfoClient()
        client.run()
        return

    server = UDPInfoServer()
    server.run()


if __name__ == "__main__":
    main()
