class FileRequest:
    """Representa una peticion de fichero realizada por el cliente."""

    def __init__(self, filename):
        """Guarda el nombre del fichero que se quiere solicitar."""
        self.filename = filename

    def to_message(self):
        """Construye el mensaje que el cliente enviara al servidor."""
        return f"GET {self.filename}"
