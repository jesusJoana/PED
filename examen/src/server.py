import socket
import sys


class Server:
    COMMAND_SEARCH = "BUSCAR"
    COMMAND_NUMBER = "NUMERO"
    COMMAND_EXIT = "SALIR"

    RESPONSE_ERROR = "ERROR"
    RESPONSE_OK = "OK"
    RESPONSE_RESULT = "RESULTADO"

    def __init__(
        self,
        host="127.0.0.1",
        port=16063,
        passwd_path="/etc/passwd",
        services_path="/etc/services",
    ):
        self.host = host
        self.port = port
        self.passwd_path = passwd_path
        self.services_path = services_path
        self.search_count = 0
        self.should_stop = False

    def process_message(self, message):
        parts = message.split()

        if len(parts) == 2 and parts[0] == self.COMMAND_SEARCH:
            return self._handle_search(parts[1])

        if len(parts) == 1 and parts[0] == self.COMMAND_NUMBER:
            return f"{self.RESPONSE_OK} {self.search_count}"

        if len(parts) == 1 and parts[0] == self.COMMAND_EXIT:
            self.should_stop = True
            return self.RESPONSE_OK

        return self.RESPONSE_ERROR

    def process_datagram(self, message, address):
        self.log_request(address, message)
        return self.process_message(message)

    def log_request(self, address, message):
        client_ip = address[0]
        print(f"{client_ip} {message}", file=sys.stderr)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.bind((self.host, self.port))

            while not self.should_stop:
                data, address = udp_socket.recvfrom(65535)
                message = data.decode("utf-8")
                response = self.process_datagram(message, address)
                udp_socket.sendto(response.encode("utf-8"), address)

    def _handle_search(self, search_text):
        self.search_count += 1
        lines = self._find_lines(search_text)
        return self._build_search_response(lines)

    def _build_search_response(self, lines):
        if not lines:
            return f"{self.RESPONSE_RESULT} 0"

        return f"{self.RESPONSE_RESULT} {len(lines)}\n" + "".join(lines)

    def _find_lines(self, search_text):
        found_lines = []

        for file_path in (self.passwd_path, self.services_path):
            with open(file_path, "r", encoding="utf-8") as source_file:
                for line in source_file:
                    if search_text in line:
                        found_lines.append(line)

        return found_lines
