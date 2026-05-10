import socket


class Client:
    """Cliente UDP que envia mensajes al servidor y muestra sus respuestas."""

    BUFFER_SIZE = 65535
    DEFAULT_MESSAGES = ("BUSCAR root", "NUMERO", "SALIR")
    ERROR_PREFIX = "ERROR"
    MIN_PORT = 1
    MAX_PORT = 65535
    SERVER_ADDRESS_PROMPT = "Direccion del servidor (host:puerto): "

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
        """Envia todos los mensajes configurados al servidor actual."""
        udp_socket = self.socket_factory()

        try:
            for message in self.messages:
                response = self._send_message(udp_socket, message)
                print(response)
        except OSError as error:
            print(f"{self.ERROR_PREFIX} {error}")
        finally:
            udp_socket.close()

    def run_interactive(self):
        """Pide al usuario la direccion del servidor antes de enviar mensajes."""
        address_text = self.ask_server_address()

        if not self.configure_server_address(address_text):
            return

        self.run()

    def ask_server_address(self):
        """Solicita al usuario la direccion completa con formato host:puerto."""
        return input(self.SERVER_ADDRESS_PROMPT)

    def configure_server_address(self, address_text):
        """Actualiza host y puerto si la direccion escrita por el usuario es valida."""
        try:
            self.host, self.port = self.parse_server_address(address_text)
            return True
        except ValueError as error:
            print(f"{self.ERROR_PREFIX} {error}")
            return False

    def parse_server_address(self, address_text):
        """Convierte una direccion host:puerto en una tupla (host, puerto)."""
        host, separator, port_text = address_text.strip().rpartition(":")

        if not separator or not host or not port_text:
            raise ValueError("formato de direccion invalido")

        try:
            port = int(port_text)
        except ValueError as error:
            raise ValueError("puerto invalido") from error

        if port < self.MIN_PORT or port > self.MAX_PORT:
            raise ValueError("puerto fuera de rango")

        return host, port

    def _send_message(self, udp_socket, message):
        """Envia un unico mensaje UDP y espera su respuesta."""
        udp_socket.sendto(message.encode("utf-8"), self._server_address())
        data, _address = udp_socket.recvfrom(self.BUFFER_SIZE)
        return data.decode("utf-8")

    def _server_address(self):
        """Devuelve la direccion UDP configurada para el servidor."""
        return self.host, self.port

    def _create_socket(self):
        """Crea el socket UDP real usado fuera de las pruebas."""
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
