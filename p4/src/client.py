import os
import socket

from config import BUFFER_SIZE, DEFAULT_SOCKET_PATH


class FileClient:
    def __init__(self, socket_path=DEFAULT_SOCKET_PATH):
        self.socket_path = socket_path

    def request_file(self, file_path):
        # El protocolo de la practica trabaja con paths absolutos.
        if not os.path.isabs(file_path):
            raise ValueError("El path del fichero debe ser absoluto")

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.socket_path)
            # Se envia un salto de linea para marcar el final del path.
            client_socket.sendall(f"{file_path}\n".encode("utf-8"))
            return self._receive_response(client_socket)

    def _receive_response(self, client_socket):
        # Se lee hasta que el servidor cierre la conexion.
        data = b""
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                break
            data += chunk
        return data.decode("utf-8")
