import socket
import sys


class LetterCountClient:
    """Cliente TCP para enviar mensajes al servidor de conteo."""

    BUFFER_SIZE = 4096
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 16063
    DEFAULT_MESSAGE_COUNT = 3
    EXIT_COMMAND = "SALIR"

    def __init__(
        self,
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        timeout=None,
        output=None,
        input_stream=None,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.output = output if output is not None else sys.stdout
        self.input_stream = input_stream if input_stream is not None else sys.stdin

    def send_message(self, message):
        try:
            response = self._send_and_receive(message)
        except OSError as error:
            self._print_error(error)
            return None

        self._print_response(response)
        return response

    def run_interactive(self, message_count=DEFAULT_MESSAGE_COUNT):
        for message in self._read_messages(message_count):
            self.send_message(message)

    def run_configured_interactive(self):
        if not self._configure_server_from_input():
            return

        for message in self._read_messages_until_exit():
            self.send_message(message)

    def _send_and_receive(self, message):
        with socket.create_connection(
            (self.host, self.port),
            timeout=self.timeout,
        ) as client_socket:
            client_socket.sendall(message.encode("utf-8"))
            client_socket.shutdown(socket.SHUT_WR)
            response = client_socket.recv(self.BUFFER_SIZE)

        return response.decode("utf-8")

    def _read_messages(self, message_count):
        for _ in range(message_count):
            message = self.input_stream.readline()
            if message == "":
                return

            yield message.rstrip("\n")

    def _configure_server_from_input(self):
        print("Direccion del servidor (host:puerto):", file=self.output)
        address = self.input_stream.readline().strip()

        try:
            host, port = self._parse_address(address)
        except ValueError as error:
            self._print_error(error)
            return False

        self.host = host
        self.port = port
        return True

    def _parse_address(self, address):
        if ":" not in address:
            raise ValueError("direccion invalida")

        host, port_text = address.rsplit(":", 1)
        if host == "" or port_text == "":
            raise ValueError("direccion invalida")

        try:
            port = int(port_text)
        except ValueError as error:
            raise ValueError("puerto invalido") from error

        return host, port

    def _read_messages_until_exit(self):
        while True:
            message = self.input_stream.readline()
            if message == "":
                return

            clean_message = message.rstrip("\n")
            if clean_message == self.EXIT_COMMAND:
                return

            yield clean_message

    def _print_response(self, response):
        print(response, file=self.output)

    def _print_error(self, error):
        print(f"ERROR: {error}", file=self.output)
