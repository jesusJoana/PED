import socket


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
                data, address = sock.recvfrom(65535)
                message = data.decode("utf-8")
                response = self.process_message(message)
                sock.sendto(response.encode("utf-8"), address)

                processed += 1
                if max_messages is not None and processed >= max_messages:
                    self.running = False

    def process_message(self, message):
        """Procesa un mensaje del protocolo y devuelve la respuesta."""
        if message == "NUMERO":
            return "OK " + str(self.search_count)

        if message == "SALIR":
            self.running = False
            return "OK"

        if message.startswith("BUSCAR ") and len(message) > len("BUSCAR "):
            text = message[len("BUSCAR ") :]
            self.search_count += 1
            found_lines = self.search_lines(text)
            return str(len(found_lines)) + "\n" + "\n".join(found_lines)

        return "ERROR"

    def search_lines(self, text):
        """Busca el texto indicado en los ficheros conocidos por el servidor."""
        found = []
        for path in ("/etc/passwd", "/etc/services"):
            with open(path, "r", encoding="utf-8", errors="replace") as file:
                for line in file:
                    clean_line = line.rstrip("\n")
                    if text in clean_line:
                        found.append(clean_line)
        return found
