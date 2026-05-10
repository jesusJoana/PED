import socket


class Client:
    DEFAULT_MESSAGES = ("BUSCAR root", "NUMERO", "SALIR")

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
                udp_socket.sendto(message.encode("utf-8"), (self.host, self.port))
                data, _address = udp_socket.recvfrom(65535)
                print(data.decode("utf-8"))
        except OSError as error:
            print(f"ERROR {error}")
        finally:
            udp_socket.close()

    def _create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
