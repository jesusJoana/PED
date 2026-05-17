import io
import os
import socket
import sys
import threading
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.client import UDPInfoClient


HOST = "127.0.0.1"
TIMEOUT = 1.0


class UDPTestServer:
    """Servidor UDP auxiliar para probar solo la responsabilidad del cliente."""

    def __init__(self, responses):
        self.responses = responses
        self.received_messages = []
        self.port = self._free_port()
        self.ready = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _free_port(self):
        """Obtiene un puerto local libre para el servidor auxiliar."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, 0))
            return sock.getsockname()[1]

    def start(self):
        """Arranca el servidor UDP auxiliar."""
        self.thread.start()
        self.ready.wait(TIMEOUT)

    def join(self):
        """Espera a que el servidor auxiliar termine."""
        self.thread.join(TIMEOUT)

    def _run(self):
        """Recibe tantos mensajes como respuestas tenga configuradas."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, self.port))
            sock.settimeout(TIMEOUT)
            self.ready.set()

            for response in self.responses:
                data, address = sock.recvfrom(65535)
                self.received_messages.append(data.decode("utf-8"))
                sock.sendto(response.encode("utf-8"), address)


class TestClienteIteracion2(unittest.TestCase):
    """Iteracion 2: pruebas unitarias del cliente UDP."""

    def _puerto_libre(self):
        """Obtiene un puerto sin servidor para provocar timeout controlado."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, 0))
            return sock.getsockname()[1]

    def test_cliente_envia_al_menos_tres_mensajes_automaticos(self):
        """
        Iteracion 2 - Cliente.
        Requisito: el cliente envia automaticamente un minimo de tres mensajes.
        """
        server = UDPTestServer(["R1", "R2", "R3"])
        server.start()
        output = io.StringIO()
        client = UDPInfoClient(host=HOST, port=server.port, timeout=TIMEOUT)

        client.run(output=output)
        server.join()

        self.assertGreaterEqual(len(server.received_messages), 3)
        self.assertFalse(server.thread.is_alive())

    def test_cliente_imprime_las_respuestas_recibidas(self):
        """
        Iteracion 2 - Cliente.
        Requisito: el cliente imprime por stdout las respuestas del servidor.
        """
        server = UDPTestServer(["respuesta uno", "respuesta dos", "respuesta tres"])
        server.start()
        output = io.StringIO()
        client = UDPInfoClient(host=HOST, port=server.port, timeout=TIMEOUT)

        client.run(output=output)

        printed = output.getvalue()
        self.assertIn("respuesta uno", printed)
        self.assertIn("respuesta dos", printed)
        self.assertIn("respuesta tres", printed)

    def test_cliente_termina_tras_el_ultimo_mensaje(self):
        """
        Iteracion 2 - Cliente.
        Requisito: el cliente termina tras recibir e imprimir la ultima respuesta.
        """
        server = UDPTestServer(["OK 0", "1\nroot:x:0:0:root:/root:/bin/bash", "OK"])
        server.start()
        output = io.StringIO()
        client = UDPInfoClient(host=HOST, port=server.port, timeout=TIMEOUT)

        client.run(output=output)
        server.join()

        self.assertEqual(3, len(server.received_messages))
        self.assertFalse(server.thread.is_alive())

    def test_cliente_imprime_error_si_no_recibe_respuesta(self):
        """
        Iteracion 2 - Cliente.
        Requisito: el cliente informa de ERROR ante un fallo de comunicacion.
        """
        output = io.StringIO()
        client = UDPInfoClient(
            host=HOST,
            port=self._puerto_libre(),
            messages=["NUMERO"],
            timeout=0.1,
        )

        client.run(output=output)

        self.assertIn("ERROR", output.getvalue())


class TestClienteIteracion5(unittest.TestCase):
    """Iteracion 5: pruebas del cliente interactivo mejorado."""

    def _puerto_libre(self):
        """Obtiene un puerto sin servidor para provocar timeout controlado."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, 0))
            return sock.getsockname()[1]

    def test_cliente_pregunta_direccion_y_envia_buscar_indicado(self):
        """
        Iteracion 5 - Cliente mejorado.
        Requisito: el cliente pregunta direccion completa y permite BUSCAR.
        """
        server = UDPTestServer(["respuesta buscar"])
        server.start()
        input_stream = io.StringIO(HOST + ":" + str(server.port) + "\nBUSCAR ssh\n")
        output = io.StringIO()
        client = UDPInfoClient(timeout=TIMEOUT)

        client.run_interactive(input_stream=input_stream, output=output)
        server.join()

        self.assertEqual(["BUSCAR ssh"], server.received_messages)
        self.assertIn("respuesta buscar", output.getvalue())

    def test_cliente_interactivo_permite_enviar_numero(self):
        """
        Iteracion 5 - Cliente mejorado.
        Requisito: el cliente permite enviar la peticion NUMERO elegida.
        """
        server = UDPTestServer(["OK 4"])
        server.start()
        input_stream = io.StringIO(HOST + ":" + str(server.port) + "\nNUMERO\n")
        output = io.StringIO()
        client = UDPInfoClient(timeout=TIMEOUT)

        client.run_interactive(input_stream=input_stream, output=output)
        server.join()

        self.assertEqual(["NUMERO"], server.received_messages)
        self.assertIn("OK 4", output.getvalue())

    def test_cliente_interactivo_permite_enviar_salir(self):
        """
        Iteracion 5 - Cliente mejorado.
        Requisito: el cliente permite enviar la peticion SALIR elegida.
        """
        server = UDPTestServer(["OK"])
        server.start()
        input_stream = io.StringIO(HOST + ":" + str(server.port) + "\nSALIR\n")
        output = io.StringIO()
        client = UDPInfoClient(timeout=TIMEOUT)

        client.run_interactive(input_stream=input_stream, output=output)
        server.join()

        self.assertEqual(["SALIR"], server.received_messages)
        self.assertIn("OK", output.getvalue())

    def test_cliente_interactivo_imprime_error_si_no_hay_respuesta(self):
        """
        Iteracion 5 - Cliente mejorado.
        Requisito: el cliente imprime ERROR si no consigue comunicarse.
        """
        input_stream = io.StringIO(HOST + ":" + str(self._puerto_libre()) + "\nNUMERO\n")
        output = io.StringIO()
        client = UDPInfoClient(timeout=0.1)

        client.run_interactive(input_stream=input_stream, output=output)

        self.assertIn("ERROR", output.getvalue())


if __name__ == "__main__":
    unittest.main()
