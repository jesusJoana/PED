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
        return cls(parts[1])
