import socket
import sys


class LetterCountClient:
    """Cliente TCP para enviar mensajes al servidor de conteo."""

    BUFFER_SIZE = 4096
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 16063
    DEFAULT_MESSAGE_COUNT = 3

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

    def _print_response(self, response):
        print(response, file=self.output)

    def _print_error(self, error):
        print(f"ERROR: {error}", file=self.output)
