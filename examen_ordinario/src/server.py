import socket

from src.protocol import LetterCountProtocol


class LetterCountServer:
    """Servidor TCP que responde mensajes del protocolo de conteo."""

    BUFFER_SIZE = 4096

    def __init__(self, host="127.0.0.1", port=16063, max_connections=None, timeout=None):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.timeout = timeout
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
                try:
                    client_socket, _client_address = server_socket.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break

                self._handle_client(client_socket)
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

    def _handle_client(self, client_socket):
        with client_socket:
            if self.timeout is not None:
                client_socket.settimeout(self.timeout)

            message = self._receive_message(client_socket)
            response = self.protocol.process(message)
            client_socket.sendall(response.encode("utf-8"))

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
