import os
import socket


class FileServer:
    """Servidor encargado de construir respuestas para peticiones de ficheros."""

    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.server_socket = None

    def build_response(self, file_path):
        """Devuelve el contenido del fichero o un mensaje de error."""
        try:
            return self._read_file(file_path)
        except OSError as error:
            return self._build_error(file_path, error)

    def serve_forever(self):
        """Crea el socket UDS y atiende clientes hasta recibir una interrupcion."""
        self._remove_old_socket()

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_socket:
            self.server_socket = server_socket
            server_socket.bind(self.socket_path)
            server_socket.listen()

            while True:
                connection, _ = server_socket.accept()
                with connection:
                    file_path = connection.recv(4096).decode("utf-8")
                    response = self.build_response(file_path)
                    connection.sendall(response.encode("utf-8"))

    def close(self):
        """Cierra el socket del servidor y elimina la entrada UDS si existe."""
        if self.server_socket is not None:
            self.server_socket.close()
        self._remove_old_socket()

    def _read_file(self, file_path):
        """Lee el fichero solicitado por el cliente."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _build_error(self, file_path, error):
        """Construye una respuesta de error legible para el cliente."""
        return f"ERROR: no se pudo leer el fichero '{file_path}': {error}"

    def _remove_old_socket(self):
        """Evita errores de bind si quedo un socket UDS anterior en la misma ruta."""
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
