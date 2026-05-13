import os
import socket
import sys
import tempfile
import threading
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 16063
BUFFER_SIZE = 4096


class ClienteTest(unittest.TestCase):

    # ============================================================
    # Iteracion 1 - Test 1 Unitario
    #
    # Objetivo:
    # Definir el comportamiento basico del cliente TCP.
    #
    # Requisitos:
    # R2: Comunicacion mediante socket TCP de Internet.
    # R3: El cliente se conecta al servidor y envia la ruta del fichero.
    # ============================================================

    def test_iteracion_1_cliente_tiene_host_y_puerto_por_defecto(self):
        """
        Requisito: R2.
        Comprueba que el constructor configura el destino TCP por defecto.
        """
        from client import FileClient

        client = FileClient()

        self.assertEqual(DEFAULT_HOST, client.host)
        self.assertEqual(DEFAULT_PORT, client.port)

    def test_iteracion_1_cliente_rechaza_ruta_relativa(self):
        """
        Requisito: R3.
        Comprueba que el cliente exige rutas absolutas para enviar peticiones.
        """
        from client import FileClient

        client = FileClient()

        with self.assertRaises(ValueError):
            client.request_file("fichero_relativo.txt")

    def test_iteracion_1_cliente_envia_peticion_tcp_y_recibe_respuesta(self):
        """
        Requisitos: R2, R3.
        Comprueba con sockets reales que el cliente envia la ruta solicitada
        por TCP y devuelve la respuesta recibida.
        """
        from client import FileClient

        received_requests = []
        server_ready = threading.Event()
        server_port = self._free_tcp_port()

        def tcp_server():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((DEFAULT_HOST, server_port))
                server_socket.listen(1)
                server_ready.set()
                connection, _ = server_socket.accept()
                with connection:
                    request = self._receive_all(connection).decode("utf-8")
                    received_requests.append(request)
                    connection.sendall(
                        "respuesta desde servidor de prueba tcp\n".encode("utf-8")
                    )

        server_thread = threading.Thread(target=tcp_server)
        server_thread.start()
        self.assertTrue(server_ready.wait(timeout=5), "El servidor TCP de prueba no arranco")

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file_path = file.name

        try:
            response = FileClient(port=server_port).request_file(file_path)

            self.assertEqual(file_path, received_requests[0])
            self.assertEqual("respuesta desde servidor de prueba tcp\n", response)
        finally:
            os.unlink(file_path)
            server_thread.join(timeout=5)

    def _receive_all(self, connection):
        chunks = []
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                break
            chunks.append(data)
        return b"".join(chunks)

    def _free_tcp_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((DEFAULT_HOST, 0))
            return sock.getsockname()[1]


if __name__ == "__main__":
    unittest.main()
