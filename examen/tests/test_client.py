import io
import os
import socket
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from client import Client


class FakeSocket:
    def __init__(self, responses=None, error_on_send=False):
        self.responses = list(responses or [])
        self.error_on_send = error_on_send
        self.sent_messages = []
        self.closed = False

    def sendto(self, data, address):
        if self.error_on_send:
            raise OSError("fallo de red")
        self.sent_messages.append((data, address))

    def recvfrom(self, buffer_size):
        if not self.responses:
            raise OSError("sin respuesta")
        return self.responses.pop(0).encode("utf-8"), ("127.0.0.1", 16063)

    def close(self):
        self.closed = True


class TestClientIteration2(unittest.TestCase):
    """Iteracion 2 - Test 2: pruebas unitarias del cliente UDP."""

    def test_cliente_tiene_host_y_puerto_por_defecto(self):
        """Iteracion 2 - Requisito cliente: usa la direccion del servidor por defecto."""
        client = Client()

        self.assertEqual(client.host, "127.0.0.1")
        self.assertEqual(client.port, 16063)

    def test_cliente_envia_minimo_tres_mensajes_al_servidor(self):
        """Iteracion 2 - Requisito cliente: envia un minimo de 3 mensajes al servidor."""
        fake_socket = FakeSocket(responses=["RESULTADO 0", "OK 1", "OK"])
        client = Client(socket_factory=Mock(return_value=fake_socket))

        client.run()

        self.assertGreaterEqual(len(fake_socket.sent_messages), 3)
        for data, address in fake_socket.sent_messages:
            self.assertIsInstance(data, bytes)
            self.assertEqual(address, ("127.0.0.1", 16063))

    def test_cliente_imprime_respuestas_recibidas(self):
        """Iteracion 2 - Requisito cliente: imprime por stdout las respuestas UDP recibidas."""
        fake_socket = FakeSocket(responses=["RESULTADO 0", "OK 1", "OK"])
        client = Client(socket_factory=Mock(return_value=fake_socket))
        output = io.StringIO()

        with redirect_stdout(output):
            client.run()

        self.assertEqual(output.getvalue(), "RESULTADO 0\nOK 1\nOK\n")

    def test_cliente_cierra_socket_al_terminar(self):
        """Iteracion 2 - Requisito cliente: se desconecta correctamente al finalizar."""
        fake_socket = FakeSocket(responses=["RESULTADO 0", "OK 1", "OK"])
        client = Client(socket_factory=Mock(return_value=fake_socket))

        client.run()

        self.assertTrue(fake_socket.closed)

    def test_cliente_imprime_error_si_falla_la_comunicacion(self):
        """Iteracion 2 - Requisito cliente: informa de cualquier condicion de error."""
        fake_socket = FakeSocket(error_on_send=True)
        client = Client(socket_factory=Mock(return_value=fake_socket))
        output = io.StringIO()

        with redirect_stdout(output):
            client.run()

        self.assertIn("ERROR", output.getvalue())
        self.assertTrue(fake_socket.closed)


if __name__ == "__main__":
    unittest.main()
