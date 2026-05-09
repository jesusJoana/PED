import socket

from config import DEFAULT_HOST, DEFAULT_PORT


class FileServer:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def build_response(self, file_path):
        # El servidor responde con el contenido textual del fichero solicitado.
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except OSError as error:
            return f"ERROR: no se pudo leer {file_path}: {error}\n"
