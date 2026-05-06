import argparse
import sys

from client import FileClient
from server import DEFAULT_SOCKET_PATH, FileServer


def build_parser():
    parser = argparse.ArgumentParser(description="Sistema cliente-servidor UDS")
    parser.add_argument("mode", choices=["server", "client"])
    parser.add_argument("file", nargs="?")
    parser.add_argument("--socket", default=DEFAULT_SOCKET_PATH)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "server":
        FileServer(socket_path=args.socket).start()
        return 0

    if args.file is None:
        parser.error("el modo client requiere el path absoluto de un fichero")

    response = FileClient(socket_path=args.socket).request_file(args.file)
    print(response, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
