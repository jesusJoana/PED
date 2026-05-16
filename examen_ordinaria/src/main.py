import sys

from src.client import TCPClient
from src.server import TCPServer


def run_server():
    # El servidor real se ejecuta de forma continua.
    server = TCPServer()
    server.start()


def run_client():
    # El cliente automatico envia los mensajes por defecto e imprime respuestas.
    client = TCPClient()
    for response in client.send_default_messages():
        print(response)


def main(arguments=None):
    # arguments permite probar main sin depender directamente de sys.argv.
    if arguments is None:
        arguments = sys.argv[1:]

    if not arguments:
        print("Uso: python src/main.py server|client", file=sys.stderr)
        return 1

    mode = arguments[0]
    if mode == "server":
        run_server()
        return 0
    if mode == "client":
        run_client()
        return 0

    print("ERROR: modo no reconocido", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
