# Punto de entrada del sistema cliente-servidor con pipes UNIX.

import os
import sys
from pathlib import Path


USAGE = "Uso: python3 src/main.py <fichero.txt>"
BUFFER_SIZE = 4096


def validate_args(args):
    # El programa solo acepta una ruta de fichero por ejecucion.
    if len(args) != 1:
        raise ValueError(USAGE)

    return args[0]


def read_requested_file(file_path):
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


def write_message(fd, message):
    # Convertimos el texto a bytes porque los pipes trabajan con bytes.
    data = message.encode("utf-8")

    # os.write puede escribir solo una parte, asi que repetimos hasta terminar.
    while data:
        written = os.write(fd, data)
        data = data[written:]


def read_message(fd):
    # Leemos hasta EOF; EOF llega cuando el proceso emisor cierra su extremo.
    chunks = []

    while True:
        chunk = os.read(fd, BUFFER_SIZE)
        if not chunk:
            break

        chunks.append(chunk)

    return b"".join(chunks).decode("utf-8")


def run_client(file_path, request_write_fd, response_read_fd):
    # El cliente envia al servidor la ruta que quiere consultar.
    write_message(request_write_fd, file_path)
    os.close(request_write_fd)

    # Despues espera la respuesta del servidor y la muestra en su terminal.
    response = read_message(response_read_fd)
    os.close(response_read_fd)
    print(response, end="", flush=True)


def run_server(request_read_fd, response_write_fd):
    # El servidor lee la peticion que llega desde el cliente.
    requested_file = read_message(request_read_fd)
    os.close(request_read_fd)

    # Con la ruta recibida, el servidor prepara el contenido o un error controlado.
    response = read_requested_file(requested_file)
    write_message(response_write_fd, response)
    os.close(response_write_fd)


def run_client_server(file_path):
    # Usamos dos pipes: uno para la peticion y otro para la respuesta.
    request_read_fd, request_write_fd = os.pipe()
    response_read_fd, response_write_fd = os.pipe()

    pid = os.fork()

    if pid == 0:
        # Proceso hijo: actua como cliente y no debe continuar el unittest/main.
        os.close(request_read_fd)
        os.close(response_write_fd)

        try:
            run_client(file_path, request_write_fd, response_read_fd)
        except OSError:
            os._exit(1)

        os._exit(0)

    # Proceso padre: actua como servidor.
    os.close(request_write_fd)
    os.close(response_read_fd)

    try:
        run_server(request_read_fd, response_write_fd)
    finally:
        _child_pid, child_status = os.waitpid(pid, 0)

    return os.waitstatus_to_exitcode(child_status)


def main(argv=None):
    # Permitimos pasar argv desde los tests; en ejecucion real usamos sys.argv.
    args = sys.argv[1:] if argv is None else argv

    # Si el usuario llama mal al programa, mostramos el uso y salimos con error.
    try:
        file_path = validate_args(args)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    # Arrancamos el cliente-servidor para pedir el fichero al proceso padre.
    return run_client_server(file_path)


if __name__ == "__main__":
    raise SystemExit(main())
