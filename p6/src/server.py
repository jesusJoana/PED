import socket

from config import BUFFER_SIZE, DEFAULT_HOST, DEFAULT_PORT


class FileServer:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        # Direccion local donde el servidor TCP quedara escuchando.
        self.host = host
        self.port = port

    def create_socket(self):
        # Socket de Internet orientado a conexion: TCP.
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        with self.create_socket() as server_socket:
            # Permite reutilizar el puerto tras cerrar y relanzar el servidor.
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            # El servidor permanece vivo hasta que el usuario fuerce su cierre.
            while True:
                connection, _client_address = server_socket.accept()
                self.handle_client(connection)

    def handle_client(self, connection):
        # Cada conexion TCP representa ya el canal de vuelta hacia ese cliente.
        with connection:
            request = self._receive_request(connection)
            response = self.process_request(request)
            connection.sendall(response.encode("utf-8"))

    def build_response(self, file_path):
        # Devuelve el contenido del fichero o un error textual si no puede leerlo.
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except OSError as error:
            return f"ERROR: no se pudo leer {file_path}: {error}\n"

    def process_request(self, request):
        # La peticion recibida es la ruta absoluta del fichero solicitado.
        return self.build_response(request)

    def _receive_request(self, connection):
        # Lee la peticion completa hasta que el cliente cierre la escritura.
        chunks = []
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                break
            chunks.append(data)
        return b"".join(chunks).decode("utf-8")
