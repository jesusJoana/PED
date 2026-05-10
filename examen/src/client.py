import socket


class Client:
    BUFFER_SIZE = 65535
    DEFAULT_MESSAGES = ("BUSCAR root", "NUMERO", "SALIR")
    ERROR_PREFIX = "ERROR"

    def __init__(
        self,
        host="127.0.0.1",
        port=16063,
        messages=None,
        socket_factory=None,
    ):
        self.host = host
        self.port = port
        self.messages = tuple(messages or self.DEFAULT_MESSAGES)
        self.socket_factory = socket_factory or self._create_socket

    def run(self):
        udp_socket = self.socket_factory()

        try:
            for message in self.messages:
                response = self._send_message(udp_socket, message)
                print(response)
        except OSError as error:
            print(f"{self.ERROR_PREFIX} {error}")
        finally:
            udp_socket.close()

    def _send_message(self, udp_socket, message):
        udp_socket.sendto(message.encode("utf-8"), self._server_address())
        data, _address = udp_socket.recvfrom(self.BUFFER_SIZE)
        return data.decode("utf-8")

    def _server_address(self):
        return self.host, self.port

    def _create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
