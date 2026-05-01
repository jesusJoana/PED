import ctypes
import os
import stat
import sys
from pathlib import Path


REQUEST_COMMAND = "GET"
OK_PREFIX = "OK"
FILE_NOT_FOUND_MESSAGE = "ERROR: fichero no encontrado"
DEFAULT_REQUEST_FIFO = "/tmp/p3_cliente_servidor.fifo"
DEFAULT_RESPONSE_FIFO = "/tmp/p3_servidor_cliente.fifo"
CLIENT_PROCESS_NAME = "cli3"
SERVER_PROCESS_NAME = "serv3"
PROCESS_WAIT_SECONDS_ENV = "PED_WAIT_SECONDS"


class FileRequest:
    """Representa una peticion de fichero realizada por el cliente."""

    def __init__(self, filename):
        """Guarda el nombre del fichero que se quiere solicitar."""
        self.filename = filename

    def to_message(self):
        """Construye el mensaje que el cliente enviara al servidor."""
        return f"{REQUEST_COMMAND} {self.filename}"

    @classmethod
    def from_message(cls, message):
        """Crea una peticion a partir del mensaje recibido por el servidor."""
        parts = message.split()
        if len(parts) != 2 or parts[0] != REQUEST_COMMAND:
            raise ValueError("Peticion no valida")
        return cls(parts[1])


class FileServer:
    """Representa el servidor encargado de leer ficheros de texto."""

    def read_file(self, file_path):
        """Lee y devuelve el contenido de un fichero de texto."""
        return Path(file_path).read_text(encoding="utf-8")

    def build_response_for_file(self, file_path):
        """Construye la respuesta para el fichero solicitado."""
        path = Path(file_path)
        if not path.exists():
            return FileResponse.file_not_found()
        return FileResponse.with_content(self.read_file(path))

    def serve_once(self, request_fifo, response_fifo):
        """Atiende una unica peticion recibida por FIFO."""
        with open(request_fifo, "r", encoding="utf-8") as fifo:
            request = FileRequest.from_message(fifo.read())

        response = self.build_response_for_file(request.filename)
        with open(response_fifo, "w", encoding="utf-8") as fifo:
            fifo.write(response.to_message())


class FileResponse:
    """Representa la respuesta que el servidor envia al cliente."""

    def __init__(self, message):
        """Guarda el mensaje que se enviara al cliente."""
        self.message = message

    @classmethod
    def with_content(cls, content):
        """Crea una respuesta correcta con el contenido del fichero."""
        return cls(f"{OK_PREFIX}\n{content}")

    @classmethod
    def file_not_found(cls):
        """Crea una respuesta de error para ficheros inexistentes."""
        return cls(FILE_NOT_FOUND_MESSAGE)

    def to_message(self):
        """Devuelve el texto completo de la respuesta."""
        return self.message


class FifoManager:
    """Gestiona las tuberias FIFO usadas por cliente y servidor."""

    def __init__(self, request_fifo, response_fifo):
        """Guarda las rutas de las tuberias de peticion y respuesta."""
        self.request_fifo = Path(request_fifo)
        self.response_fifo = Path(response_fifo)

    def setup(self):
        """Crea las tuberias FIFO si todavia no existen."""
        self._create_fifo(self.request_fifo)
        self._create_fifo(self.response_fifo)

    def cleanup(self):
        """Elimina las tuberias FIFO creadas por la aplicacion."""
        for fifo_path in (self.request_fifo, self.response_fifo):
            if fifo_path.exists() and stat.S_ISFIFO(fifo_path.stat().st_mode):
                fifo_path.unlink()

    def _create_fifo(self, fifo_path):
        """Crea una FIFO y acepta que ya exista previamente."""
        if fifo_path.exists():
            if not stat.S_ISFIFO(fifo_path.stat().st_mode):
                raise ValueError(f"La ruta existe y no es FIFO: {fifo_path}")
            return
        os.mkfifo(fifo_path)


class FileClient:
    """Representa el cliente que solicita un fichero al servidor."""

    def __init__(self, filename):
        """Guarda el fichero que se solicitara al servidor."""
        self.filename = filename

    def request_file(self, request_fifo, response_fifo):
        """Envia la peticion por FIFO y muestra la respuesta recibida."""
        request = FileRequest(self.filename)
        with open(request_fifo, "w", encoding="utf-8") as fifo:
            fifo.write(request.to_message())

        with open(response_fifo, "r", encoding="utf-8") as fifo:
            print(fifo.read())


def set_process_name(name):
    """Cambia el nombre visible del proceso en sistemas Linux."""
    libc = ctypes.CDLL(None)
    libc.prctl(15, name.encode("utf-8"), 0, 0, 0)


def wait_for_manual_check():
    """Pausa opcionalmente el proceso para comprobar su nombre con ps."""
    wait_seconds = float(os.environ.get(PROCESS_WAIT_SECONDS_ENV, "0"))
    if wait_seconds > 0:
        import time

        time.sleep(wait_seconds)


def main():
    """Crea cliente y servidor comunicados mediante FIFO."""
    filename = sys.argv[1] if len(sys.argv) > 1 else "prueba.txt"
    fifo_manager = FifoManager(DEFAULT_REQUEST_FIFO, DEFAULT_RESPONSE_FIFO)
    fifo_manager.setup()

    pid = os.fork()
    if pid == 0:
        set_process_name(CLIENT_PROCESS_NAME)
        wait_for_manual_check()
        FileClient(filename).request_file(
            fifo_manager.request_fifo, fifo_manager.response_fifo
        )
        sys.exit(0)

    try:
        set_process_name(SERVER_PROCESS_NAME)
        wait_for_manual_check()
        FileServer().serve_once(fifo_manager.request_fifo, fifo_manager.response_fifo)
        os.waitpid(pid, 0)
    finally:
        fifo_manager.cleanup()


if __name__ == "__main__":
    main()
