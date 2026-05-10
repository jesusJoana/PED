import sys

from client import Client
from server import Server


def main():
    """Punto de entrada: sin argumentos arranca servidor; con client arranca cliente."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "server"

    if mode == "client":
        client = Client()
        client.run_interactive()
        return

    server = Server()
    server.run()


if __name__ == "__main__":
    main()
