import socket
import threading
import time
import unittest

from src.client import TCPClient
from src.server import TCPServer


class TestClientServerIntegration(unittest.TestCase):
    """Pruebas de integracion entre cliente y servidor reales."""

    def _get_free_port(self):
        # Usamos un puerto libre para que el test no dependa del puerto del
        # contrato ni choque con un servidor manual en ejecucion.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            test_socket.bind(("127.0.0.1", 0))
            return test_socket.getsockname()[1]

    def _start_server(self, port, max_connections):
        # El servidor real se ejecuta en un hilo y se limita a las conexiones de
        # la prueba para que pueda terminar.
        server = TCPServer(host="127.0.0.1", port=port)
        thread = threading.Thread(
            target=server.start,
            kwargs={"max_connections": max_connections},
            daemon=True,
        )
        thread.start()
        time.sleep(0.1)
        return thread

    # Iteracion 4 - Test 4 Integracion
    # Requisito: cliente y servidor reales colaboran mediante sockets TCP,
    # usando el protocolo completo de mensajes y respuestas.
    def test_client_and_server_exchange_three_messages(self):
        port = self._get_free_port()
        server_thread = self._start_server(port, max_connections=3)
        client = TCPClient(host="127.0.0.1", port=port)

        responses = client.send_default_messages()

        server_thread.join(timeout=2)

        self.assertEqual(
            [
                "m:3",
                "m:3,e:4,z:0",
                "ERROR",
            ],
            responses,
        )
        self.assertFalse(server_thread.is_alive())

    # Iteracion 4 - Test 4 Integracion
    # Requisito: la aplicacion debe disponer de un punto de entrada main.py para
    # lanzar cliente y servidor mediante make.
    def test_main_module_exposes_entry_point(self):
        from src.main import main

        self.assertTrue(callable(main))


if __name__ == "__main__":
    # Permite ejecutar este archivo de test directamente con python.
    unittest.main()
