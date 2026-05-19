import io
import threading
import time
import unittest

from src.client import LetterCountClient
from src.server import LetterCountServer


class TestIntegracionIteracion3(unittest.TestCase):
    """
    Iteracion 3 - Integracion cliente-servidor.

    Estas pruebas validan el flujo completo usando el cliente real, el servidor
    real y comunicacion TCP real.
    """

    HOST = "127.0.0.1"

    def _arrancar_servidor(self, max_connections):
        servidor = LetterCountServer(
            host=self.HOST,
            port=0,
            max_connections=max_connections,
            timeout=1.0,
        )
        hilo = threading.Thread(target=servidor.start, daemon=True)
        hilo.start()

        limite = time.time() + 2
        while servidor.port == 0 and time.time() < limite:
            time.sleep(0.01)

        self.assertNotEqual(0, servidor.port)
        self.addCleanup(self._cerrar_servidor, servidor, hilo)
        return servidor

    def _cerrar_servidor(self, servidor, hilo):
        servidor.stop()
        hilo.join(timeout=2)

    def test_cliente_y_servidor_intercambian_un_mensaje_valido(self):
        """
        Iteracion 3.
        Requisito: cliente y servidor reales se comunican por TCP y obtienen la
        respuesta del protocolo.
        """
        output = io.StringIO()
        servidor = self._arrancar_servidor(max_connections=1)
        cliente = LetterCountClient(
            host=self.HOST,
            port=servidor.port,
            timeout=1.0,
            output=output,
        )

        respuesta = cliente.send_message("p,a:me gusta ped")

        self.assertEqual("p:1,a:1", respuesta)
        self.assertEqual("p:1,a:1\n", output.getvalue())

    def test_cliente_y_servidor_intercambian_tres_mensajes(self):
        """
        Iteracion 3.
        Requisito: el cliente real puede enviar 3 mensajes al servidor real y
        terminar tras imprimir sus respuestas.
        """
        output = io.StringIO()
        input_stream = io.StringIO("c:coco\nA:aAaA\nx:abc\n")
        servidor = self._arrancar_servidor(max_connections=3)
        cliente = LetterCountClient(
            host=self.HOST,
            port=servidor.port,
            timeout=1.0,
            output=output,
            input_stream=input_stream,
        )

        cliente.run_interactive(message_count=3)

        self.assertEqual("c:2\nA:2\nx:0\n", output.getvalue())

    def test_cliente_y_servidor_manejan_mensaje_invalido(self):
        """
        Iteracion 3.
        Requisito: ante un mensaje invalido, el servidor real responde ERROR y
        el cliente real lo imprime.
        """
        output = io.StringIO()
        servidor = self._arrancar_servidor(max_connections=1)
        cliente = LetterCountClient(
            host=self.HOST,
            port=servidor.port,
            timeout=1.0,
            output=output,
        )

        respuesta = cliente.send_message("mensaje sin formato")

        self.assertEqual("ERROR", respuesta)
        self.assertEqual("ERROR\n", output.getvalue())
