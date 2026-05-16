import socket
import sys

from src.protocol import MessageProcessor


class TCPServer:
    """Servidor TCP que procesa un mensaje por conexion."""

    def __init__(self, host="127.0.0.1", port=16063):
        # Valores por defecto definidos por el contrato de la practica.
        self.host = host
        self.port = port
        self.processor = MessageProcessor()

    def handle_message(self, message):
        # La logica del protocolo queda delegada en MessageProcessor.
        return self.processor.process(message)

    def start(self, max_connections=None):
        # max_connections permite que los tests terminen aunque el servidor real
        # vaya a ejecutarse de forma continua.
        served_connections = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            while max_connections is None or served_connections < max_connections:
                connection, address = server_socket.accept()
                self.handle_client(connection, address)
                served_connections += 1

    def handle_client(self, connection, address):
        # Cada cliente envia un mensaje, recibe una respuesta y queda cerrado.
        with connection:
            data = connection.recv(4096)
            message = data.decode("utf-8")
            self.log_connection(address[0], message)
            response = self.handle_message(message)
            connection.sendall(response.encode("utf-8"))

    def log_connection(self, client_ip, message):
        # El enunciado exige registrar IP y mensaje recibido en error estandar.
        print(f"Cliente {client_ip} envio: {message}", file=sys.stderr)
