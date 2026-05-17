import socket
import sys


BUFFER_SIZE = 65535
BUSCAR_PREFIX = "BUSCAR "
SEARCH_FILES = ("/etc/passwd", "/etc/services")


class UDPInfoServer:
    """Servidor UDP que responde al protocolo de consulta de frases."""

    def __init__(self, host="127.0.0.1", port=16063):
        self.host = host
        self.port = port
        self.search_count = 0
        self.running = False

    def run(self, max_messages=None):
        """Atiende mensajes UDP hasta SALIR o hasta max_messages en pruebas."""
        self.running = True
        processed = 0

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.host, self.port))

            while self.running:
                data, address = sock.recvfrom(BUFFER_SIZE)
                message = data.decode("utf-8")
                self._log_client_message(address, message)
                response = self.process_message(message)
                sock.sendto(response.encode("utf-8"), address)

                processed += 1
                if max_messages is not None and processed >= max_messages:
                    self.running = False

    def process_message(self, message):
        """Procesa un mensaje del protocolo y devuelve la respuesta."""
        if message == "NUMERO":
            return self._process_numero()

        if message == "SALIR":
            return self._process_salir()

        if message.startswith(BUSCAR_PREFIX) and len(message) > len(BUSCAR_PREFIX):
            return self._process_buscar(message[len(BUSCAR_PREFIX) :])

        return "ERROR"

    def _log_client_message(self, address, message):
        """Escribe en stderr la IP del cliente y el mensaje recibido."""
        print(address[0] + " " + message, file=sys.stderr, flush=True)

    def _process_numero(self):
        """Devuelve el numero de busquedas ejecutadas."""
        return "OK " + str(self.search_count)

    def _process_salir(self):
        """Marca el servidor para finalizar tras responder."""
        self.running = False
        return "OK"

    def _process_buscar(self, text):
        """Ejecuta una busqueda y construye la respuesta del protocolo."""
        self.search_count += 1
        found_lines = self.search_lines(text)
        return str(len(found_lines)) + "\n" + "\n".join(found_lines)

    def search_lines(self, text):
        """Busca el texto indicado en los ficheros conocidos por el servidor."""
        found = []
        for path in SEARCH_FILES:
            with open(path, "r", encoding="utf-8", errors="replace") as file:
                for line in file:
                    clean_line = line.rstrip("\n")
                    if text in clean_line:
                        found.append(clean_line)
        return found
