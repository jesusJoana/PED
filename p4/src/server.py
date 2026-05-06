import os
import socket

from config import BUFFER_SIZE, DEFAULT_SOCKET_PATH


class FileServer:
    def __init__(self, socket_path=DEFAULT_SOCKET_PATH):
        # El enunciado exige que todos los sockets se creen dentro de /tmp.
        if not socket_path.startswith("/tmp/"):
            raise ValueError("El socket debe crearse dentro de /tmp")
        self.socket_path = socket_path

    def build_response(self, file_path):
        # El servidor responde siempre con texto: contenido del fichero o error.
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except OSError as error:
            return f"ERROR: no se pudo leer {file_path}: {error}\n"

    def start(self):
        # Si queda un socket antiguo, se elimina para poder hacer bind de nuevo.
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(self.socket_path)
            server_socket.listen(5)

            # El servidor no termina tras atender un cliente.
            while True:
                connection, _ = server_socket.accept()
                with connection:
                    self.handle_connection(connection)

    def handle_connection(self, connection):
        file_path = self._receive_path(connection)
        response = self.build_response(file_path)
        connection.sendall(response.encode("utf-8"))

    def _receive_path(self, connection):
        # El cliente termina la peticion con salto de linea.
        data = b""
        while b"\n" not in data:
            chunk = connection.recv(BUFFER_SIZE)
            if not chunk:
                break
            data += chunk
        return data.decode("utf-8").strip()
