class FileServer:
    """Servidor encargado de construir respuestas para peticiones de ficheros."""

    def __init__(self, socket_path):
        self.socket_path = socket_path

    def build_response(self, file_path):
        """Devuelve el contenido del fichero o un mensaje de error."""
        try:
            return self._read_file(file_path)
        except OSError as error:
            return self._build_error(file_path, error)

    def _read_file(self, file_path):
        """Lee el fichero solicitado por el cliente."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _build_error(self, file_path, error):
        """Construye una respuesta de error legible para el cliente."""
        return f"ERROR: no se pudo leer el fichero '{file_path}': {error}"
