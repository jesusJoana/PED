import socket
import threading

from config import BUFFER_SIZE, DEFAULT_HOST, DEFAULT_PORT


class FileServer:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        with self.create_socket() as server_socket:
            server_socket.bind((self.host, self.port))
            while True:
                data, client_address = server_socket.recvfrom(BUFFER_SIZE)
                thread = threading.Thread(
                    target=self.handle_request,
                    args=(server_socket, data, client_address),
                    daemon=True,
                )
                thread.start()

    def handle_request(self, server_socket, data, client_address):
        request = data.decode("utf-8")
        response = self.process_request(request)
        server_socket.sendto(response.encode("utf-8"), client_address)

    def build_response(self, file_path):
        # El servidor responde con el contenido textual del fichero solicitado.
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except OSError as error:
            return f"ERROR: no se pudo leer {file_path}: {error}\n"

    def process_request(self, request):
        return self.build_response(request)
