import importlib
import io
import socket
import threading
import unittest


class SimpleTcpTestServer:
    """Servidor TCP minimo para probar la clase cliente."""

    def __init__(self, responses):
        self.host = "127.0.0.1"
        self.port = 0
        self.responses = list(responses)
        self.received_messages = []
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()
        self._ready.wait(timeout=2)

    def join(self):
        self._thread.join(timeout=2)

    def _run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, 0))
            self.port = server_socket.getsockname()[1]
            server_socket.listen()
            server_socket.settimeout(2)
            self._ready.set()

            for response in self.responses:
                client_socket, _client_address = server_socket.accept()
                with client_socket:
                    message = self._receive_message(client_socket)
                    self.received_messages.append(message)
                    client_socket.sendall(response.encode("utf-8"))

    def _receive_message(self, client_socket):
        chunks = []

        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            chunks.append(data)

        return b"".join(chunks).decode("utf-8")


class TestClienteIteracion2(unittest.TestCase):
    """
    Iteracion 2 - Cliente.

    Estas pruebas validan que el cliente conecta por TCP, envia mensajes UTF-8,
    imprime respuestas y gestiona errores de conexion.
    """

    def _crear_cliente(self, host, port, output=None, input_stream=None):
        modulo = importlib.import_module("src.client")
        client_cls = modulo.LetterCountClient
        return client_cls(
            host=host,
            port=port,
            timeout=1.0,
            output=output,
            input_stream=input_stream,
        )

    def test_envia_un_mensaje_e_imprime_respuesta(self):
        """
        Iteracion 2.
        Requisito: el cliente envia un mensaje y muestra la respuesta recibida.
        """
        output = io.StringIO()
        server = SimpleTcpTestServer(["p:1"])
        server.start()
        client = self._crear_cliente(server.host, server.port, output=output)

        response = client.send_message("p:ped")
        server.join()

        self.assertEqual("p:1", response)
        self.assertEqual(["p:ped"], server.received_messages)
        self.assertEqual("p:1\n", output.getvalue())

    def test_envia_tres_mensajes_interactivos_y_termina(self):
        """
        Iteracion 2.
        Requisito: el cliente permite escribir 3 mensajes, los envia e imprime
        sus respuestas antes de terminar.
        """
        output = io.StringIO()
        input_stream = io.StringIO("p:ped\na:Ana\nx:xxx\n")
        server = SimpleTcpTestServer(["p:1", "a:1", "x:3"])
        server.start()
        client = self._crear_cliente(
            server.host,
            server.port,
            output=output,
            input_stream=input_stream,
        )

        client.run_interactive(message_count=3)
        server.join()

        self.assertEqual(["p:ped", "a:Ana", "x:xxx"], server.received_messages)
        self.assertEqual("p:1\na:1\nx:3\n", output.getvalue())

    def test_informa_error_si_falla_la_conexion(self):
        """
        Iteracion 2.
        Requisito: el cliente imprime una condicion de error si no puede
        conectarse al servidor.
        """
        output = io.StringIO()
        client = self._crear_cliente("127.0.0.1", 1, output=output)

        response = client.send_message("p:ped")

        self.assertIsNone(response)
        self.assertIn("ERROR", output.getvalue())
