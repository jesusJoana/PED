import argparse
import sys

from client import FileClient
from server import FileServer
from setproctitle import setproctitle


def build_parser():
    # main.py es el punto de entrada unico exigido por el contrato.
    parser = argparse.ArgumentParser(description="Sistema cliente-servidor TCP")
    parser.add_argument("mode", choices=["server", "client"])
    parser.add_argument("file", nargs="?")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.mode == "server":
        setproctitle("serv6")
        # El servidor queda bloqueado atendiendo clientes hasta cierre manual.
        FileServer().start()
        return 0

    if args.file is None:
        parser.error("el modo client requiere el path absoluto de un fichero")

    setproctitle("cli6")
    # El cliente imprime la respuesta recibida y termina.
    response = FileClient().request_file(args.file)
    print(response, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
