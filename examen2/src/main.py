import sys

from src.server import UDPTextSearchServer


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "server":
        print("ERROR")
        return 1

    server = UDPTextSearchServer()
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
