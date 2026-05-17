import sys

from src.client import UDPTextSearchClient
from src.server import UDPTextSearchServer


def main():
    if len(sys.argv) < 2:
        print("ERROR")
        return 1

    if sys.argv[1] == "server":
        server = UDPTextSearchServer()
        server.serve_forever()
        return 0

    if sys.argv[1] == "client":
        client = UDPTextSearchClient()
        client.run_interactive()
        return 0

    print("ERROR")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
