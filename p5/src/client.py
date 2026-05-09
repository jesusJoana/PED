import os
import socket

from config import BUFFER_SIZE, DEFAULT_HOST, DEFAULT_PORT


class FileClient:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def request_file(self, file_path):
        # El protocolo de la practica trabaja con rutas absolutas.
        if not os.path.isabs(file_path):
            raise ValueError("El path del fichero debe ser absoluto")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.send(file_path.encode("utf-8"))
            response = client_socket.recv(BUFFER_SIZE)

        return response.decode("utf-8")
