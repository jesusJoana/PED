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

    def run_interactive(self, input_stream=None, output=None):
        input_data = input_stream if input_stream is not None else sys.stdin
        output_stream = output if output is not None else sys.stdout

        try:
            host, port = self._parse_server_address(input_data.readline().strip())
        except ValueError:
            print("ERROR", file=output_stream)
            return

        self.host = host
        self.port = port
        self.run(output=output_stream)

    def _parse_server_address(self, address):
        host, separator, port_text = address.rpartition(":")
        if separator == "" or host == "" or port_text == "":
            raise ValueError("Direccion de servidor invalida")

        try:
            port = int(port_text)
        except ValueError as exc:
            raise ValueError("Puerto invalido") from exc

        return host, port

    def _send_and_receive(self, client_socket, message):
        client_socket.sendto(message.encode("utf-8"), (self.host, self.port))
        data, _ = client_socket.recvfrom(self.BUFFER_SIZE)
        return data.decode("utf-8")
