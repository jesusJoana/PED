class FileRequest:
    """Representa una peticion de fichero realizada por el cliente."""

    def __init__(self, filename):
        """Guarda el nombre del fichero que se quiere solicitar."""
        self.filename = filename

    def to_message(self):
        """Construye el mensaje que el cliente enviara al servidor."""
        return f"GET {self.filename}"

    @classmethod
    def from_message(cls, message):
        """Crea una peticion a partir del mensaje recibido por el servidor."""
        parts = message.split()
        if len(parts) != 2 or parts[0] != "GET":
            raise ValueError("Peticion no valida")
        return cls(parts[1])


class FileServer:
    """Representa el servidor encargado de leer ficheros de texto."""

    def read_file(self, file_path):
        """Lee y devuelve el contenido de un fichero de texto."""
        return file_path.read_text(encoding="utf-8")

    def build_response_for_file(self, file_path):
        """Construye la respuesta para el fichero solicitado."""
        if not file_path.exists():
            return FileResponse.file_not_found()
        return FileResponse.with_content(self.read_file(file_path))


class FileResponse:
    """Representa la respuesta que el servidor envia al cliente."""

    def __init__(self, message):
        """Guarda el mensaje que se enviara al cliente."""
        self.message = message

    @classmethod
    def with_content(cls, content):
        """Crea una respuesta correcta con el contenido del fichero."""
        return cls(f"OK\n{content}")

    @classmethod
    def file_not_found(cls):
        """Crea una respuesta de error para ficheros inexistentes."""
        return cls("ERROR: fichero no encontrado")

    def to_message(self):
        """Devuelve el texto completo de la respuesta."""
        return self.message
