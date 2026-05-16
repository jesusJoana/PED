import socket


def parse_server_address(address_text):
    # La direccion completa se espera en formato host:puerto.
    if ":" not in address_text:
        raise ValueError("direccion invalida")

    host, port_text = address_text.rsplit(":", 1)
    if not host or not port_text.isdigit():
        raise ValueError("direccion invalida")

    return host, int(port_text)


class TCPClient:
    """Cliente TCP que envia un mensaje por conexion."""

    def __init__(self, host="127.0.0.1", port=16063, timeout=2):
        # Valores por defecto definidos por el contrato de la practica.
        self.host = host
        self.port = port
        self.timeout = timeout
        self.default_messages = [
            "m:combinaciones momentaneas de palabras",
            "m,e,z:Combinaciones momentaneas de palabras",
            "mensaje incorrecto",
        ]

    def send_message(self, message):
        # Cada mensaje abre una conexion TCP, espera respuesta y cierra.
        try:
            with socket.create_connection(
                (self.host, self.port), timeout=self.timeout
            ) as client_socket:
                client_socket.settimeout(self.timeout)
                client_socket.sendall(message.encode("utf-8"))
                response = client_socket.recv(4096)
                return response.decode("utf-8")
        except OSError as error:
            return f"ERROR: {error}"

    def send_default_messages(self):
        # Devuelve las respuestas para que main.py pueda imprimirlas.
        responses = []
        for message in self.default_messages:
            responses.append(self.send_message(message))
        return responses
