import contextlib
import io
import os
import socket
import sys
import threading
import time
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.server import UDPInfoServer


HOST = "127.0.0.1"
TIMEOUT = 2.0


class TestServidorIteracion1(unittest.TestCase):
    """Iteracion 1: pruebas unitarias del servidor UDP."""

    def _puerto_libre(self):
        """Obtiene un puerto local libre para evitar conflictos entre pruebas."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, 0))
            return sock.getsockname()[1]

    def _arrancar_servidor(self, max_messages=1):
        """Arranca el servidor en un hilo para probar UDP real sin bloquear."""
        port = self._puerto_libre()
        server = UDPInfoServer(host=HOST, port=port)
        thread = threading.Thread(
            target=server.run,
            kwargs={"max_messages": max_messages},
            daemon=True,
        )
        thread.start()
        time.sleep(0.1)
        return server, thread, port

    def _enviar_mensaje(self, port, message):
        """Envia un datagrama UDP y devuelve la respuesta decodificada."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(TIMEOUT)
            sock.sendto(message.encode("utf-8"), (HOST, port))
            data, _ = sock.recvfrom(65535)
            return data.decode("utf-8")

    def _lineas_esperadas(self, text):
        """Calcula las lineas esperadas siguiendo el orden del enunciado."""
        found = []
        for path in ("/etc/passwd", "/etc/services"):
            with open(path, "r", encoding="utf-8", errors="replace") as file:
                for line in file:
                    clean_line = line.rstrip("\n")
                    if text in clean_line:
                        found.append(clean_line)
        return found

    def test_mensaje_desconocido_devuelve_error(self):
        """
        Iteracion 1 - Servidor.
        Requisito: cualquier mensaje desconocido debe responder ERROR.
        """
        _server, thread, port = self._arrancar_servidor(max_messages=1)

        response = self._enviar_mensaje(port, "HOLA")

        self.assertEqual("ERROR", response)
        thread.join(TIMEOUT)
        self.assertFalse(thread.is_alive())

    def test_numero_inicial_devuelve_ok_cero(self):
        """
        Iteracion 1 - Servidor.
        Requisito: NUMERO devuelve OK y el numero de busquedas ejecutadas.
        """
        _server, thread, port = self._arrancar_servidor(max_messages=1)

        response = self._enviar_mensaje(port, "NUMERO")

        self.assertEqual("OK 0", response)
        thread.join(TIMEOUT)
        self.assertFalse(thread.is_alive())

    def test_buscar_devuelve_numero_y_lineas_encontradas(self):
        """
        Iteracion 1 - Servidor.
        Requisito: BUSCAR busca en /etc/passwd y /etc/services.
        """
        expected_lines = self._lineas_esperadas("root")
        expected_response = str(len(expected_lines)) + "\n" + "\n".join(expected_lines)
        _server, thread, port = self._arrancar_servidor(max_messages=1)

        response = self._enviar_mensaje(port, "BUSCAR root")

        self.assertEqual(expected_response, response)
        thread.join(TIMEOUT)
        self.assertFalse(thread.is_alive())

    def test_buscar_incrementa_contador_de_busquedas(self):
        """
        Iteracion 1 - Servidor.
        Requisito: NUMERO refleja las busquedas ejecutadas con BUSCAR.
        """
        _server, thread, port = self._arrancar_servidor(max_messages=2)

        self._enviar_mensaje(port, "BUSCAR root")
        response = self._enviar_mensaje(port, "NUMERO")

        self.assertEqual("OK 1", response)
        thread.join(TIMEOUT)
        self.assertFalse(thread.is_alive())

    def test_salir_devuelve_ok_y_termina_servidor(self):
        """
        Iteracion 1 - Servidor.
        Requisito: SALIR responde OK y termina la ejecucion del servidor.
        """
        _server, thread, port = self._arrancar_servidor(max_messages=None)

        response = self._enviar_mensaje(port, "SALIR")

        self.assertEqual("OK", response)
        thread.join(TIMEOUT)
        self.assertFalse(thread.is_alive())


class TestServidorIteracion4(unittest.TestCase):
    """Iteracion 4: pruebas del registro de mensajes recibidos en stderr."""

    def _puerto_libre(self):
        """Obtiene un puerto local libre para evitar conflictos entre pruebas."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, 0))
            return sock.getsockname()[1]

    def _arrancar_servidor(self, max_messages=1):
        """Arranca el servidor en un hilo para probar UDP real sin bloquear."""
        port = self._puerto_libre()
        server = UDPInfoServer(host=HOST, port=port)
        thread = threading.Thread(
            target=server.run,
            kwargs={"max_messages": max_messages},
            daemon=True,
        )
        thread.start()
        time.sleep(0.1)
        return server, thread, port

    def _enviar_mensaje(self, port, message):
        """Envia un datagrama UDP y devuelve la respuesta decodificada."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(TIMEOUT)
            sock.sendto(message.encode("utf-8"), (HOST, port))
            data, _ = sock.recvfrom(65535)
            return data.decode("utf-8")

    def test_servidor_escribe_ip_del_cliente_en_stderr(self):
        """
        Iteracion 4 - Servidor modificado.
        Requisito: al recibir un mensaje, imprime la IP del cliente en stderr.
        """
        log = io.StringIO()

        with contextlib.redirect_stderr(log):
            _server, thread, port = self._arrancar_servidor(max_messages=1)
            response = self._enviar_mensaje(port, "NUMERO")
            thread.join(TIMEOUT)

        self.assertEqual("OK 0", response)
        self.assertIn(HOST, log.getvalue())
        self.assertFalse(thread.is_alive())

    def test_servidor_escribe_mensaje_recibido_en_stderr(self):
        """
        Iteracion 4 - Servidor modificado.
        Requisito: al recibir un mensaje, imprime el mensaje en stderr.
        """
        log = io.StringIO()

        with contextlib.redirect_stderr(log):
            _server, thread, port = self._arrancar_servidor(max_messages=1)
            response = self._enviar_mensaje(port, "BUSCAR root")
            thread.join(TIMEOUT)

        self.assertIn("root", response)
        self.assertIn("BUSCAR root", log.getvalue())
        self.assertFalse(thread.is_alive())


if __name__ == "__main__":
    unittest.main()
