import sys

from src.client import ClienteTCP
from src.server import ServidorTCP


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py servidor|cliente")
        return 1

    if sys.argv[1] == "servidor":
        ServidorTCP().iniciar()
        return 0

    if sys.argv[1] == "cliente":
        ClienteTCP().ejecutar_interactivo()
        return 0

    print("Modo no reconocido")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
