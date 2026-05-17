import io
import socket
import threading
import unittest


from src.client import UDPTextSearchClient


class UDPServerLigero:
    """Servidor UDP auxiliar para probar solo responsabilidades del cliente."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.received_messages = []
        self.host = "127.0.0.1"
        self.port = None
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()
        self._ready.wait(timeout=2)

    def join(self):
        self._thread.join(timeout=2)

    def _run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((self.host, 0))
            self.port = server_socket.getsockname()[1]
            self._ready.set()

            for response in self.responses:
                data, client_address = server_socket.recvfrom(65535)
                self.received_messages.append(data.decode("utf-8"))
                server_socket.sendto(response.encode("utf-8"), client_address)


class TestClienteIteracion2(unittest.TestCase):
    """Tests de la Iteración 2 - Cliente."""

    def test_cliente_usa_host_y_puerto_por_defecto_del_contrato(self):
        """Iteración 2. Requisito: el cliente usa la dirección por defecto."""
        client = UDPTextSearchClient(messages=["NUMERO"])

        self.assertEqual("127.0.0.1", client.host)
        self.assertEqual(16063, client.port)

    def test_cliente_envia_al_menos_tres_mensajes_e_imprime_respuestas(self):
        """Iteración 2. Requisito: envía mínimo 3 mensajes e imprime respuestas."""
        server = UDPServerLigero(
            responses=[
                "OK 0",
                "RESULTADO 1\nroot:x:0:0:root:/root:/bin/bash",
                "OK",
            ]
        )
        server.start()
        output = io.StringIO()
        messages = ["NUMERO", "BUSCAR root", "SALIR"]

        client = UDPTextSearchClient(
            host=server.host,
            port=server.port,
            messages=messages,
            timeout=1,
        )
        client.run(output=output)
        server.join()

        self.assertEqual(messages, server.received_messages)
        self.assertIn("OK 0", output.getvalue())
        self.assertIn("RESULTADO 1\nroot:x:0:0:root:/root:/bin/bash", output.getvalue())
        self.assertIn("OK", output.getvalue())

    def test_cliente_termina_tras_el_ultimo_mensaje(self):
        """Iteración 2. Requisito: el cliente termina tras el último mensaje."""
        server = UDPServerLigero(responses=["OK 0", "RESULTADO 0", "OK"])
        server.start()
        output = io.StringIO()

        client = UDPTextSearchClient(
            host=server.host,
            port=server.port,
            messages=["NUMERO", "BUSCAR nada", "SALIR"],
            timeout=1,
        )
        client.run(output=output)
        server.join()

        self.assertFalse(server._thread.is_alive())

    def test_cliente_imprime_error_ante_timeout(self):
        """Iteración 2. Requisito: ante error de comunicación imprime error."""
        unused_port = self._get_unused_udp_port()
        output = io.StringIO()
        client = UDPTextSearchClient(
            host="127.0.0.1",
            port=unused_port,
            messages=["NUMERO"],
            timeout=0.1,
        )

        client.run(output=output)

        self.assertIn("ERROR", output.getvalue())

    def _get_unused_udp_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as test_socket:
            test_socket.bind(("127.0.0.1", 0))
            return test_socket.getsockname()[1]


class TestClienteIteracion5(unittest.TestCase):
    """Tests de la Iteración 5 - Cliente modificado."""

    def test_cliente_pide_direccion_completa_y_envia_al_destino_indicado(self):
        """Iteración 5. Requisito: pedir host:puerto y usar esa dirección."""
        server = UDPServerLigero(responses=["OK 0", "RESULTADO 0", "OK"])
        server.start()
        input_stream = io.StringIO(f"{server.host}:{server.port}\n")
        output = io.StringIO()

        client = UDPTextSearchClient(
            messages=["NUMERO", "BUSCAR nada", "SALIR"],
            timeout=1,
        )
        client.run_interactive(input_stream=input_stream, output=output)
        server.join()

        self.assertEqual(["NUMERO", "BUSCAR nada", "SALIR"], server.received_messages)
        self.assertIn("OK 0", output.getvalue())
        self.assertIn("RESULTADO 0", output.getvalue())
        self.assertIn("OK", output.getvalue())

    def test_cliente_imprime_error_si_la_direccion_no_tiene_formato_valido(self):
        """Iteración 5. Requisito: dirección completa inválida produce ERROR."""
        input_stream = io.StringIO("direccion-sin-puerto\n")
        output = io.StringIO()
        client = UDPTextSearchClient(messages=["NUMERO"], timeout=0.1)

        client.run_interactive(input_stream=input_stream, output=output)

        self.assertIn("ERROR", output.getvalue())

    def test_cliente_interactivo_imprime_error_si_no_consigue_comunicarse(self):
        """Iteración 5. Requisito: error si no consigue comunicarse."""
        unused_port = self._get_unused_udp_port()
        input_stream = io.StringIO(f"127.0.0.1:{unused_port}\n")
        output = io.StringIO()
        client = UDPTextSearchClient(messages=["NUMERO"], timeout=0.1)

        client.run_interactive(input_stream=input_stream, output=output)

        self.assertIn("ERROR", output.getvalue())

    def _get_unused_udp_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as test_socket:
            test_socket.bind(("127.0.0.1", 0))
            return test_socket.getsockname()[1]


if __name__ == "__main__":
    unittest.main()
