from pathlib import Path


REQUEST_COMMAND = "GET"
OK_PREFIX = "OK"
FILE_NOT_FOUND_MESSAGE = "ERROR: fichero no encontrado"


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
