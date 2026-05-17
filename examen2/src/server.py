import socket
import sys


class UDPTextSearchServer:
    """Servidor UDP que procesa mensajes de busqueda sobre ficheros conocidos."""

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 16063
    DEFAULT_FILE_PATHS = ("/etc/passwd", "/etc/services")
    BUFFER_SIZE = 65535

    def __init__(self, host=None, port=None, file_paths=None):
        self.host = host if host is not None else self.DEFAULT_HOST
        self.port = port if port is not None else self.DEFAULT_PORT
        self.file_paths = list(file_paths or self.DEFAULT_FILE_PATHS)
        self.search_count = 0
        self.should_stop = False
        self.bound_port = None
        self._socket = None

    def handle_message(self, message):
        if message == "NUMERO":
            return f"OK {self.search_count}"

        if message == "SALIR":
            self.should_stop = True
            return "OK"

        if message.startswith("BUSCAR"):
            return self._handle_search(message)

        return "ERROR"

    def serve_forever(self):
        self.should_stop = False
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            self._socket = server_socket
            server_socket.bind((self.host, self.port))
            self.bound_port = server_socket.getsockname()[1]

            while not self.should_stop:
                data, client_address = server_socket.recvfrom(self.BUFFER_SIZE)
                message = data.decode("utf-8")
                self._log_request(client_address, message)
                response = self.handle_message(message)
                server_socket.sendto(response.encode("utf-8"), client_address)

        self._socket = None

    def close(self):
        if self._socket is not None:
            self._socket.close()
            self._socket = None

    def _handle_search(self, message):
        if not message.startswith("BUSCAR "):
            return "ERROR"

        search_text = message[len("BUSCAR ") :]
        if search_text.strip() == "":
            return "ERROR"

        self.search_count += 1
        matches = self._find_matches(search_text)

        if not matches:
            return "RESULTADO 0"

        return f"RESULTADO {len(matches)}\n" + "\n".join(matches)

    def _log_request(self, client_address, message):
        client_ip = client_address[0]
        print(f"{client_ip} {message}", file=sys.stderr)

    def _find_matches(self, search_text):
        matches = []
        for file_path in self.file_paths:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    clean_line = line.rstrip("\n")
                    if search_text in clean_line:
                        matches.append(clean_line)
        return matches
