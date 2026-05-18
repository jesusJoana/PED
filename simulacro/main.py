import sys

from src.server import ServidorTCP


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py servidor")
        return 1

    if sys.argv[1] == "servidor":
        ServidorTCP().iniciar()
        return 0

    print("Modo no reconocido")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
