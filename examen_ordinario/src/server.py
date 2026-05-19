import socket
import sys

from src.protocol import LetterCountProtocol


class LetterCountServer:
    """Servidor TCP que responde mensajes del protocolo de conteo."""

    BUFFER_SIZE = 4096

    def __init__(
        self,
        host="127.0.0.1",
        port=16063,
        max_connections=None,
        timeout=None,
        error_output=None,
    ):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.timeout = timeout
        self.error_output = error_output if error_output is not None else sys.stderr
        self.protocol = LetterCountProtocol()
        self._running = False
        self._server_socket = None

    def start(self):
        self._running = True
        handled_connections = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._server_socket = server_socket
            self._prepare_server_socket(server_socket)

            while self._should_continue(handled_connections):
                accepted_client = self._accept_client(server_socket)
                if accepted_client is None:
                    continue

                client_socket, client_address = accepted_client
                if client_socket is None:
                    continue

                self._handle_client(client_socket, client_address)
                handled_connections += 1

        self._server_socket = None
        self._running = False

    def _prepare_server_socket(self, server_socket):
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.timeout is not None:
            server_socket.settimeout(self.timeout)

        server_socket.bind((self.host, self.port))
        self.port = server_socket.getsockname()[1]
        server_socket.listen()

    def _accept_client(self, server_socket):
        try:
            return server_socket.accept()
        except socket.timeout:
            return None
        except OSError:
            self._running = False
            return None

    def stop(self):
        self._running = False
        if self._server_socket is not None:
            try:
                self._server_socket.close()
            except OSError:
                pass

    def _should_continue(self, attended_connections):
        if not self._running:
            return False

        if self.max_connections is None:
            return True

        return attended_connections < self.max_connections

    def _handle_client(self, client_socket, client_address):
        with client_socket:
            if self.timeout is not None:
                client_socket.settimeout(self.timeout)

            message = self._receive_message(client_socket)
            self._log_connection(client_address, message)
            response = self.protocol.process(message)
            client_socket.sendall(response.encode("utf-8"))

    def _log_connection(self, client_address, message):
        client_ip = client_address[0]
        print(f"{client_ip} {message}", file=self.error_output)

    def _receive_message(self, client_socket):
        chunks = []

        while True:
            try:
                data = client_socket.recv(self.BUFFER_SIZE)
            except socket.timeout:
                break

            if not data:
                break

            chunks.append(data)

        return b"".join(chunks).decode("utf-8")
