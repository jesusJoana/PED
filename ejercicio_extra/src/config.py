import os


class SocketConfig:
    """Lee y valida la ruta configurable del socket UDS."""

    def __init__(self, config_path):
        self.config_path = config_path

    def read_socket_path(self):
        """Devuelve la ruta del socket indicada en el fichero de configuracion."""
        with open(self.config_path, "r", encoding="utf-8") as config_file:
            socket_path = config_file.readline().strip()

        if not socket_path:
            raise ValueError("La ruta del socket no puede estar vacia")

        if os.path.dirname(socket_path) != "/tmp":
            raise ValueError("El socket UDS debe crearse dentro de /tmp")

        return socket_path
