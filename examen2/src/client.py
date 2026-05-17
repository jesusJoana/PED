import socket
import sys


BUFFER_SIZE = 65535
DEFAULT_MESSAGES = ("NUMERO", "BUSCAR root", "SALIR")
DEFAULT_ATTEMPTS = 3


class UDPInfoClient:
    """Cliente UDP que envia mensajes y muestra las respuestas del servidor."""

    def __init__(
        self,
        host="127.0.0.1",
        port=16063,
        messages=None,
        timeout=2.0,
        attempts=DEFAULT_ATTEMPTS,
    ):
        self.host = host
        self.port = port
        self.messages = list(messages) if messages is not None else list(DEFAULT_MESSAGES)
        self.timeout = timeout
        self.attempts = attempts

    def run(self, output=None):
        """Envia los mensajes configurados e imprime cada respuesta recibida."""
        if output is None:
            output = sys.stdout

        with self._create_socket() as sock:
            for message in self.messages:
                response = self._send_and_receive(sock, message)
                self._print_response(output, response)
                if response is None:
                    break

    def _create_socket(self):
        """Crea el socket UDP configurado con timeout."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        return sock

    def _send_and_receive(self, sock, message):
        """Envia un mensaje UDP y devuelve la respuesta recibida."""
        for _attempt in range(self.attempts):
            try:
                sock.sendto(message.encode("utf-8"), (self.host, self.port))
                data, _address = sock.recvfrom(BUFFER_SIZE)
                return data.decode("utf-8")
            except OSError:
                pass

        return None

    def _print_response(self, output, response):
        """Imprime la respuesta recibida o ERROR si no hubo respuesta."""
        if response is None:
            print("ERROR", file=output)
            return

        print(response, file=output)
