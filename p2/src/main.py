"""Punto de entrada del sistema cliente-servidor con pipes UNIX."""

import sys


USAGE = "Uso: python3 src/main.py <fichero.txt>"


def validate_args(args: list[str]) -> str:
    """Valida los argumentos y devuelve la ruta solicitada por el cliente."""
    if len(args) != 1:
        raise ValueError(USAGE)

    return args[0]


def main(argv: list[str] | None = None) -> int:
    """Arranque principal del programa.

    Acepta una lista de argumentos para poder probarlo sin depender de sys.argv.
    Mas adelante, con argumentos validos, aqui arrancaremos pipes y fork.
    """
    args = sys.argv[1:] if argv is None else argv

    try:
        validate_args(args)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
