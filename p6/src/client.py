import os
import socket

from config import BUFFER_SIZE, DEFAULT_HOST, DEFAULT_PORT


class FileClient:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        # Direccion del servidor TCP al que se conectara el cliente.
        self.host = host
        self.port = port

    def request_file(self, file_path):
        # El protocolo de la practica trabaja con rutas absolutas.
        if not os.path.isabs(file_path):
            raise ValueError("El path del fichero debe ser absoluto")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # En TCP el cliente conecta con el puerto donde escucha el servidor.
            client_socket.connect((self.host, self.port))
            client_socket.sendall(file_path.encode("utf-8"))
            # Indica al servidor que ya se ha enviado toda la peticion.
            client_socket.shutdown(socket.SHUT_WR)
            response = self._receive_all(client_socket)

        return response.decode("utf-8")

    def _receive_all(self, client_socket):
        # Recibe la respuesta completa hasta que el servidor cierre la conexion.
        chunks = []
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            chunks.append(data)
        return b"".join(chunks)
