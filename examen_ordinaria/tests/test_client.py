import socket
import threading
import unittest


class TestTCPClient(unittest.TestCase):
    """Pruebas unitarias del cliente usando sockets TCP reales."""

    def setUp(self):
        # La importacion se hace aqui para que la fase RED falle test a test
        # mientras la clase TCPClient aun no exista.
        from src.client import TCPClient

        # Cada prueba crea su propio cliente con configuracion por defecto.
        self.client = TCPClient()

    def _get_free_port(self):
        # Pedimos al sistema un puerto libre para levantar servidores auxiliares
        # durante las pruebas.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            test_socket.bind(("127.0.0.1", 0))
            return test_socket.getsockname()[1]

    def _start_response_server(self, response_text, received_messages):
        # Servidor auxiliar minimo: acepta una conexion, guarda el mensaje
        # recibido y responde con el texto indicado.
        port = self._get_free_port()
        ready = threading.Event()

        def server_task():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind(("127.0.0.1", port))
                server_socket.listen(1)
                ready.set()

                connection, _ = server_socket.accept()
                with connection:
                    data = connection.recv(4096)
                    received_messages.append(data.decode("utf-8"))
                    connection.sendall(response_text.encode("utf-8"))

        thread = threading.Thread(target=server_task, daemon=True)
        thread.start()
        ready.wait(timeout=2)
        return port, thread

    # Iteracion 3 - Test 3 Unitario
    # Requisito del contrato: si no se indica otro valor, el host por defecto es
    # 127.0.0.1.
    def test_client_default_host_is_localhost(self):
        self.assertEqual("127.0.0.1", self.client.host)

    # Iteracion 3 - Test 3 Unitario
    # Requisito del contrato: si el enunciado no indica otro valor, el puerto
    # por defecto es 16063.
    def test_client_default_port_is_contract_port(self):
        self.assertEqual(16063, self.client.port)

    # Iteracion 3 - Test 3 Unitario
    # Requisito: el cliente debe tener un minimo de tres mensajes para enviar al
    # servidor.
    def test_client_has_at_least_three_default_messages(self):
        self.assertGreaterEqual(len(self.client.default_messages), 3)

    # Iteracion 3 - Test 3 Unitario
    # Requisito: el cliente debe abrir una conexion TCP real, enviar UTF-8,
    # recibir UTF-8 y cerrar correctamente.
    def test_client_sends_message_and_receives_response_using_tcp(self):
        from src.client import TCPClient

        received_messages = []
        port, thread = self._start_response_server("m:3", received_messages)
        client = TCPClient(host="127.0.0.1", port=port)

        response = client.send_message("m:combinaciones momentaneas de palabras")

        thread.join(timeout=2)

        self.assertEqual("m:3", response)
        self.assertEqual(["m:combinaciones momentaneas de palabras"], received_messages)
        self.assertFalse(thread.is_alive())

    # Iteracion 3 - Test 3 Unitario
    # Requisito: si no se puede conectar, el cliente debe devolver una condicion
    # de error controlada.
    def test_client_returns_error_when_connection_fails(self):
        from src.client import TCPClient

        port = self._get_free_port()
        client = TCPClient(host="127.0.0.1", port=port)

        response = client.send_message("m:mensaje")

        self.assertTrue(response.startswith("ERROR"))

    # Iteracion 8 - Test 8 Unitario
    # Requisito: el cliente modificado interpreta una direccion completa
    # indicada por el usuario en formato host:puerto.
    def test_parse_server_address_returns_host_and_port(self):
        from src.client import parse_server_address

        host, port = parse_server_address("127.0.0.1:16063")

        self.assertEqual("127.0.0.1", host)
        self.assertEqual(16063, port)

    # Iteracion 8 - Test 8 Unitario
    # Requisito: una direccion sin puerto no es valida.
    def test_parse_server_address_without_port_raises_error(self):
        from src.client import parse_server_address

        with self.assertRaises(ValueError):
            parse_server_address("127.0.0.1")

    # Iteracion 8 - Test 8 Unitario
    # Requisito: una direccion con puerto no numerico no es valida.
    def test_parse_server_address_with_non_numeric_port_raises_error(self):
        from src.client import parse_server_address

        with self.assertRaises(ValueError):
            parse_server_address("127.0.0.1:abc")


if __name__ == "__main__":
    # Permite ejecutar este archivo de test directamente con python.
    unittest.main()
