import sys

from src.client import LetterCountClient
from src.server import LetterCountServer


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py servidor")
        return 1

    mode = sys.argv[1]

    if mode == "servidor":
        server = LetterCountServer()
        server.start()
        return 0

    if mode == "cliente":
        client = LetterCountClient()
        client.run_configured_interactive()
        return 0

    print("Modo no reconocido")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
