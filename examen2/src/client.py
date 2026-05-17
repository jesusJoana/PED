import socket
import sys


class UDPTextSearchClient:
    """Cliente UDP que envia mensajes al servidor y muestra sus respuestas."""

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 16063
    DEFAULT_MESSAGES = ("NUMERO", "BUSCAR root", "SALIR")
    BUFFER_SIZE = 65535

    def __init__(self, host=None, port=None, messages=None, timeout=2):
        self.host = host if host is not None else self.DEFAULT_HOST
        self.port = port if port is not None else self.DEFAULT_PORT
        self.messages = list(messages or self.DEFAULT_MESSAGES)
        self.timeout = timeout

    def run(self, output=None):
        output_stream = output if output is not None else sys.stdout

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.settimeout(self.timeout)

            for message in self.messages:
                try:
                    response = self._send_and_receive(client_socket, message)
                except OSError:
                    print("ERROR", file=output_stream)
                    return

                print(response, file=output_stream)

    def _send_and_receive(self, client_socket, message):
        client_socket.sendto(message.encode("utf-8"), (self.host, self.port))
        data, _ = client_socket.recvfrom(self.BUFFER_SIZE)
        return data.decode("utf-8")
