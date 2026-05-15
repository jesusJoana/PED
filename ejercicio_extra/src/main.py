import sys

from src.client import FileClient
from src.config import SocketConfig
from src.server import FileServer


class ApplicationLauncher:
    """Prepara el lanzamiento de cliente y servidor desde main.py."""

    def __init__(self, config_path):
        self.config_path = config_path

    def parse_args(self, args):
        """Valida los argumentos recibidos por linea de comandos."""
        if len(args) == 1 and args[0] == "server":
            return "server", None

        if len(args) == 2 and args[0] == "client":
            return "client", args[1]

        if args and args[0] == "client":
            raise ValueError("Uso: python src/main.py client <ruta_fichero>")

        raise ValueError("Uso: python src/main.py server | client <ruta_fichero>")

    def process_name_for(self, mode):
        """Devuelve el nombre de proceso exigido por el enunciado."""
        if mode == "server":
            return "serv4_g6"
        if mode == "client":
            return "cli4_g6"
        raise ValueError("Modo no reconocido")

    def set_process_name(self, mode):
        """Asigna el nombre del proceso si la dependencia esta instalada."""
        try:
            from setproctitle import setproctitle

            setproctitle(self.process_name_for(mode))
        except ImportError:
            pass

    def run(self, args):
        """Ejecuta el modo solicitado usando la ruta del socket configurada."""
        mode, file_path = self.parse_args(args)
        self.set_process_name(mode)
        socket_path = SocketConfig(self.config_path).read_socket_path()

        if mode == "server":
            server = FileServer(socket_path)
            server.serve_forever()
        else:
            client = FileClient(socket_path)
            print(client.request_file(file_path), end="")


def main():
    launcher = ApplicationLauncher("config.txt")
    try:
        launcher.run(sys.argv[1:])
    except ValueError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
