import contextlib
import io
import socket
import threading
import time
import unittest


class TestMessageProcessor(unittest.TestCase):
    """Pruebas unitarias del protocolo usado por el servidor."""

    def setUp(self):
        # La importacion se hace aqui para que en la fase RED cada test falle
        # individualmente si aun no existe la implementacion.
        from src.protocol import MessageProcessor

        # Cada prueba usa un procesador nuevo e independiente.
        self.processor = MessageProcessor()

    # Iteracion 1 - Test 1 Unitario
    # Requisito: el servidor responde al formato c:Frase con c:numero.
    def test_single_character_message_counts_occurrences(self):
        # Se cuenta cuantas veces aparece "m" en la frase.
        response = self.processor.process("m:combinaciones momentaneas de palabras")

        self.assertEqual("m:3", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: el servidor responde al formato c1,c2,...,cm:Frase con el
    # conteo de cada caracter, manteniendo el orden recibido.
    def test_multiple_character_message_counts_each_character(self):
        # Se cuentan varios caracteres en una sola peticion.
        response = self.processor.process(
            "m,e,z:Combinaciones momentaneas de palabras"
        )

        self.assertEqual("m:3,e:4,z:0", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: cualquier mensaje que no respete el formato esperado devuelve
    # ERROR.
    def test_message_without_separator_returns_error(self):
        # Sin ":" no se puede separar comando y frase.
        response = self.processor.process("mensaje incorrecto")

        self.assertEqual("ERROR", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: una lista vacia de caracteres no es un comando valido.
    def test_empty_character_list_returns_error(self):
        # Hay frase, pero falta el caracter o lista de caracteres a contar.
        response = self.processor.process(":frase sin caracter")

        self.assertEqual("ERROR", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: cada elemento de la lista debe ser un unico caracter.
    def test_character_token_with_more_than_one_character_returns_error(self):
        # "mm" no es un caracter individual, por tanto el comando no es valido.
        response = self.processor.process("mm:frase con formato invalido")

        self.assertEqual("ERROR", response)


class TestTCPServer(unittest.TestCase):
    """Pruebas unitarias de la clase servidor usando sockets TCP reales."""

    def setUp(self):
        # La importacion se hace aqui para que la fase RED falle test a test
        # mientras la clase TCPServer aun no exista.
        from src.server import TCPServer

        # Cada prueba crea su propio servidor con configuracion por defecto.
        self.server = TCPServer()

    def _get_free_port(self):
        # Pedimos al sistema un puerto libre para no depender del puerto real
        # del contrato durante las pruebas.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            test_socket.bind(("127.0.0.1", 0))
            return test_socket.getsockname()[1]

    # Iteracion 2 - Test 2 Unitario
    # Requisito del contrato: si no se indica otro valor, el host por defecto es
    # 127.0.0.1.
    def test_server_default_host_is_localhost(self):
        self.assertEqual("127.0.0.1", self.server.host)

    # Iteracion 2 - Test 2 Unitario
    # Requisito del contrato: si el enunciado no indica otro valor, el puerto
    # por defecto es 16063.
    def test_server_default_port_is_contract_port(self):
        self.assertEqual(16063, self.server.port)

    # Iteracion 2 - Test 2 Unitario
    # Requisito: el servidor calcula la respuesta correcta para mensajes
    # validos usando la logica del protocolo.
    def test_server_handles_valid_message(self):
        response = self.server.handle_message(
            "m:combinaciones momentaneas de palabras"
        )

        self.assertEqual("m:3", response)

    # Iteracion 2 - Test 2 Unitario
    # Requisito: cualquier mensaje no reconocido debe producir ERROR.
    def test_server_handles_invalid_message(self):
        response = self.server.handle_message("mensaje incorrecto")

        self.assertEqual("ERROR", response)

    # Iteracion 2 - Test 2 Unitario
    # Requisito: el servidor debe escuchar mediante TCP, aceptar una conexion
    # real, recibir UTF-8, responder por la misma conexion y cerrar el cliente.
    def test_server_accepts_tcp_connection_responds_and_closes_client(self):
        from src.server import TCPServer

        port = self._get_free_port()
        server = TCPServer(host="127.0.0.1", port=port)

        # En pruebas limitamos el servidor a una conexion para que el hilo
        # termine y el test no quede bloqueado.
        server_thread = threading.Thread(
            target=server.start,
            kwargs={"max_connections": 1},
            daemon=True,
        )
        server_thread.start()
        time.sleep(0.1)

        with socket.create_connection(("127.0.0.1", port), timeout=2) as client:
            client.settimeout(2)
            client.sendall("m:combinaciones momentaneas de palabras".encode("utf-8"))

            response = client.recv(1024).decode("utf-8")
            closed_data = client.recv(1024)

        server_thread.join(timeout=2)

        self.assertEqual("m:3", response)
        self.assertEqual(b"", closed_data)
        self.assertFalse(server_thread.is_alive())

    # Iteracion 7 - Test 7 Unitario
    # Requisito: cada vez que recibe una conexion, el servidor debe escribir en
    # error estandar la IP del cliente y el mensaje recibido.
    def test_server_logs_client_ip_and_received_message_to_stderr(self):
        from src.server import TCPServer

        port = self._get_free_port()
        server = TCPServer(host="127.0.0.1", port=port)
        stderr_buffer = io.StringIO()

        def run_server():
            with contextlib.redirect_stderr(stderr_buffer):
                server.start(max_connections=1)

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        time.sleep(0.1)

        message = "m:combinaciones momentaneas de palabras"
        with socket.create_connection(("127.0.0.1", port), timeout=2) as client:
            client.settimeout(2)
            client.sendall(message.encode("utf-8"))
            client.recv(1024)

        server_thread.join(timeout=2)
        stderr_output = stderr_buffer.getvalue()

        self.assertIn("127.0.0.1", stderr_output)
        self.assertIn(message, stderr_output)
        self.assertFalse(server_thread.is_alive())


if __name__ == "__main__":
    # Permite ejecutar este archivo de test directamente con python.
    unittest.main()
