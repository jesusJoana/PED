import argparse
import sys

from client import FileClient
from server import FileServer


def build_parser():
    parser = argparse.ArgumentParser(description="Sistema cliente-servidor UDP")
    parser.add_argument("mode", choices=["server", "client"])
    parser.add_argument("file", nargs="?")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # main.py es el punto de entrada unico exigido por el contrato.
    if args.mode == "server":
        FileServer().start()
        return 0

    if args.file is None:
        parser.error("el modo client requiere el path absoluto de un fichero")

    response = FileClient().request_file(args.file)
    print(response, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
