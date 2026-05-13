import os
import socket

from config import BUFFER_SIZE, DEFAULT_HOST, DEFAULT_PORT


class FileClient:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def request_file(self, file_path):
        if not os.path.isabs(file_path):
            raise ValueError("El path del fichero debe ser absoluto")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(file_path.encode("utf-8"))
            client_socket.shutdown(socket.SHUT_WR)
            response = self._receive_all(client_socket)

        return response.decode("utf-8")

    def _receive_all(self, client_socket):
        chunks = []
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            chunks.append(data)
        return b"".join(chunks)
