class FileServer:
    """Servidor encargado de construir respuestas para peticiones de ficheros."""

    def __init__(self, socket_path):
        self.socket_path = socket_path

    def build_response(self, file_path):
        """Devuelve el contenido del fichero o un mensaje de error."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except OSError as error:
            return f"ERROR: no se pudo leer el fichero '{file_path}': {error}"
