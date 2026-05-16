import sys

from src.client import TCPClient, parse_server_address
from src.server import TCPServer


def run_server():
    # El servidor real se ejecuta de forma continua.
    server = TCPServer()
    server.start()


def run_client():
    # El cliente modificado pregunta al usuario la direccion completa.
    address_text = input("Direccion completa del servidor (host:puerto): ")
    try:
        host, port = parse_server_address(address_text.strip())
    except ValueError:
        print("ERROR: direccion del servidor invalida")
        return 1

    client = TCPClient(host=host, port=port)
    for response in client.send_default_messages():
        print(response)
    return 0


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
        return run_client()

    print("ERROR: modo no reconocido", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
