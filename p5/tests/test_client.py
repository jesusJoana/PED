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
    # Definir el comportamiento minimo de la clase FileClient.
    #
    # Requisitos:
    # R2: El cliente enviara una peticion al servidor mediante
    #     un socket UDP de Internet.
    # ============================================================

    def test_iteracion_1_cliente_tiene_host_y_puerto_por_defecto(self):
        """
        Requisito: R2.
        Comprueba que el constructor configura el destino UDP por defecto.
        """
        from client import FileClient

        client = FileClient()

        self.assertEqual(DEFAULT_HOST, client.host)
        self.assertEqual(DEFAULT_PORT, client.port)

    def test_iteracion_1_cliente_rechaza_ruta_relativa(self):
        """
        Requisito: R2.
        Comprueba que el cliente exige rutas absolutas para enviar peticiones.
        """
        from client import FileClient

        client = FileClient()

        with self.assertRaises(ValueError):
            client.request_file("fichero_relativo.txt")

    def test_iteracion_1_cliente_envia_peticion_udp_y_recibe_respuesta(self):
        """
        Requisito: R2.
        Comprueba con sockets reales que el cliente envia la ruta solicitada
        por UDP y devuelve la respuesta recibida.
        """
        from client import FileClient

        received_requests = []
        server_ready = threading.Event()

        def udp_server():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                server_socket.settimeout(5)
                server_socket.bind((DEFAULT_HOST, DEFAULT_PORT))
                server_ready.set()
                data, client_address = server_socket.recvfrom(BUFFER_SIZE)
                received_requests.append(data.decode("utf-8"))
                server_socket.sendto(
                    "respuesta desde servidor de prueba\n".encode("utf-8"),
                    client_address,
                )

        server_thread = threading.Thread(target=udp_server)
        server_thread.start()
        self.assertTrue(server_ready.wait(timeout=5), "El servidor UDP de prueba no arranco")

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file_path = file.name

        try:
            response = FileClient().request_file(file_path)

            self.assertEqual(file_path, received_requests[0])
            self.assertEqual("respuesta desde servidor de prueba\n", response)
        finally:
            os.unlink(file_path)
            server_thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
