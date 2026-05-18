import io
import re
import socket
import threading
import time
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src.client import ClienteTCP
from src.server import ServidorTCP


class TestIntegracionClienteServidor(unittest.TestCase):
    """Pruebas de la Iteracion 3: Integracion cliente-servidor."""

    def obtener_puerto_libre(self):
        """Reserva temporalmente un puerto libre para evitar choques en tests."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    def arrancar_servidor_real(self, max_conexiones=1):
        """Arranca el servidor real en un hilo controlado por la prueba."""
        puerto = self.obtener_puerto_libre()
        servidor = ServidorTCP(host="127.0.0.1", puerto=puerto)
        hilo = threading.Thread(
            target=servidor.iniciar,
            kwargs={"max_conexiones": max_conexiones},
            daemon=True,
        )
        hilo.start()
        time.sleep(0.1)
        return hilo, puerto

    # Iteracion 3 - Requisito: cliente y servidor reales intercambian FECHA.
    def test_cliente_real_recibe_fecha_de_servidor_real(self):
        hilo, puerto = self.arrancar_servidor_real(max_conexiones=1)
        cliente = ClienteTCP(host="127.0.0.1", puerto=puerto)

        cliente.conectar()
        respuesta = cliente.enviar_mensaje("FECHA")
        cliente.cerrar()

        hilo.join(timeout=2)
        self.assertRegex(respuesta, r"^\d{4}-\d{2}-\d{2}$")
        self.assertFalse(hilo.is_alive())

    # Iteracion 3 - Requisito: cliente y servidor reales intercambian HORA.
    def test_cliente_real_recibe_hora_de_servidor_real(self):
        hilo, puerto = self.arrancar_servidor_real(max_conexiones=1)
        cliente = ClienteTCP(host="127.0.0.1", puerto=puerto)

        cliente.conectar()
        respuesta = cliente.enviar_mensaje("HORA")
        cliente.cerrar()

        hilo.join(timeout=2)
        self.assertRegex(respuesta, r"^\d{2}:\d{2}:\d{2}$")
        self.assertFalse(hilo.is_alive())

    # Iteracion 3 - Requisito: mensajes no reconocidos devuelven ERROR extremo a extremo.
    def test_cliente_real_recibe_error_de_servidor_real(self):
        hilo, puerto = self.arrancar_servidor_real(max_conexiones=1)
        cliente = ClienteTCP(host="127.0.0.1", puerto=puerto)

        cliente.conectar()
        respuesta = cliente.enviar_mensaje("DESCONOCIDO")
        cliente.cerrar()

        hilo.join(timeout=2)
        self.assertEqual("ERROR", respuesta)
        self.assertFalse(hilo.is_alive())

    # Iteracion 3 - Requisito: el cliente envia tres mensajes antes de cerrar.
    def test_cliente_interactivo_real_envia_tres_mensajes_y_cierra(self):
        hilo, puerto = self.arrancar_servidor_real(max_conexiones=1)
        cliente = ClienteTCP(host="127.0.0.1", puerto=puerto, mensajes_minimos=3)
        entradas = iter(["FECHA", "HORA", "DESCONOCIDO", "SALIR"])
        salida = io.StringIO()

        with patch("builtins.input", side_effect=lambda _: next(entradas)):
            with redirect_stdout(salida):
                cliente.ejecutar_interactivo()

        hilo.join(timeout=2)
        texto_salida = salida.getvalue()
        self.assertRegex(texto_salida, r"\d{4}-\d{2}-\d{2}")
        self.assertRegex(texto_salida, r"\d{2}:\d{2}:\d{2}")
        self.assertIn("ERROR", texto_salida)
        self.assertIn("Cliente desconectado correctamente.", texto_salida)
        self.assertFalse(hilo.is_alive())


if __name__ == "__main__":
    unittest.main()
