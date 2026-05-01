# Punto de entrada del sistema cliente-servidor con pipes UNIX.

import sys
from pathlib import Path


USAGE = "Uso: python3 src/main.py <fichero.txt>"


def validate_args(args: list[str]) -> str:
    # El programa solo acepta una ruta de fichero por ejecucion.
    if len(args) != 1:
        raise ValueError(USAGE)

    return args[0]


def read_requested_file(file_path: str) -> str:
    # Esta funcion representa la parte del servidor que prepara la respuesta.
    path = Path(file_path)

    # Si el fichero no existe, devolvemos un error que luego recibira el cliente.
    if not path.exists():
        return f"ERROR: el fichero '{file_path}' no existe"

    # Evitamos intentar leer carpetas como si fueran ficheros de texto.
    if not path.is_file():
        return f"ERROR: la ruta '{file_path}' no es un fichero"

    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        return f"ERROR: no se pudo leer '{file_path}': {error}"


def main(argv: list[str] | None = None) -> int:
    # Permitimos pasar argv desde los tests; en ejecucion real usamos sys.argv.
    args = sys.argv[1:] if argv is None else argv

    # Si el usuario llama mal al programa, mostramos el uso y salimos con error.
    try:
        validate_args(args)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    # En las siguientes iteraciones aqui arrancaremos pipes y fork.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
