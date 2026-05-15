import os
import socket


class FileClient:
    """Cliente que solicita ficheros a un servidor mediante socket UDS."""

    def __init__(self, socket_path):
        self.socket_path = socket_path

    def request_file(self, file_path):
        """Envia el path absoluto del fichero y devuelve la respuesta recibida."""
        full_path = os.path.abspath(file_path)

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.socket_path)
            client_socket.sendall(full_path.encode("utf-8"))
            return self._receive_response(client_socket)

    def _receive_response(self, client_socket):
        """Lee todos los fragmentos enviados por el servidor."""
        chunks = []
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)

        return b"".join(chunks).decode("utf-8")
