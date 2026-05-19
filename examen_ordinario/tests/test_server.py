import importlib
import io
import socket
import threading
import time
import unittest


class ServerTestHelpers:
    HOST = "127.0.0.1"

    def _crear_servidor(self, max_connections=1):
        modulo = importlib.import_module("src.server")
        servidor_cls = modulo.LetterCountServer
        return servidor_cls(
            host=self.HOST,
            port=0,
            max_connections=max_connections,
            timeout=1.0,
        )

    def _arrancar_servidor(self, max_connections=1):
        servidor = self._crear_servidor(max_connections=max_connections)
        hilo = threading.Thread(target=servidor.start, daemon=True)
        hilo.start()

        limite = time.time() + 2
        while getattr(servidor, "port", 0) == 0 and time.time() < limite:
            time.sleep(0.01)

        self.assertNotEqual(
            0,
            getattr(servidor, "port", 0),
            "El servidor debe publicar el puerto real cuando arranca con port=0",
        )

        self.addCleanup(self._cerrar_servidor, servidor, hilo)
        return servidor

    def _cerrar_servidor(self, servidor, hilo):
        if hasattr(servidor, "stop"):
            servidor.stop()
        hilo.join(timeout=2)

    def _enviar_mensaje(self, puerto, mensaje):
        with socket.create_connection((self.HOST, puerto), timeout=2) as sock:
            sock.sendall(mensaje.encode("utf-8"))
            sock.shutdown(socket.SHUT_WR)
            respuesta = sock.recv(4096)

        return respuesta.decode("utf-8")


class TestServidorIteracion1(ServerTestHelpers, unittest.TestCase):
    """
    Iteracion 1 - Servidor.

    Estas pruebas validan que el servidor TCP acepta conexiones reales, recibe
    mensajes UTF-8 y responde segun el protocolo de conteo de letras.
    """

    def test_responde_conteo_de_una_letra(self):
        """
        Iteracion 1.
        Requisito: el servidor cuenta una letra indicada antes de ':'.
        """
        servidor = self._arrancar_servidor()

        respuesta = self._enviar_mensaje(servidor.port, "c:casa con coco")

        self.assertEqual("c:4", respuesta)

    def test_responde_conteo_de_varias_letras_en_orden(self):
        """
        Iteracion 1.
        Requisito: el servidor cuenta varias letras separadas por comas.
        """
        servidor = self._arrancar_servidor()

        respuesta = self._enviar_mensaje(servidor.port, "c,t,p:ccttpp")

        self.assertEqual("c:2,t:2,p:2", respuesta)

    def test_distingue_mayusculas_y_minusculas(self):
        """
        Iteracion 1.
        Requisito: el conteo es sensible a mayusculas y minusculas.
        """
        servidor = self._arrancar_servidor()

        respuesta = self._enviar_mensaje(servidor.port, "a,A:aAaA")

        self.assertEqual("a:2,A:2", respuesta)

    def test_responde_error_ante_mensaje_invalido(self):
        """
        Iteracion 1.
        Requisito: cualquier mensaje no valido obtiene respuesta ERROR.
        """
        servidor = self._arrancar_servidor()

        respuesta = self._enviar_mensaje(servidor.port, "mensaje sin formato")

        self.assertEqual("ERROR", respuesta)

    def test_atiende_mas_de_una_conexion(self):
        """
        Iteracion 1.
        Requisito: el servidor no termina tras atender un unico cliente.
        """
        servidor = self._arrancar_servidor(max_connections=2)

        primera = self._enviar_mensaje(servidor.port, "p:ped")
        segunda = self._enviar_mensaje(servidor.port, "d:ped")

        self.assertEqual("p:1", primera)
        self.assertEqual("d:1", segunda)


class TestServidorIteracion4(ServerTestHelpers, unittest.TestCase):
    """
    Iteracion 4 - Servidor modificado.

    Estas pruebas validan que el servidor escribe en error estandar una linea
    por conexion con la IP del cliente y el mensaje recibido.
    """

    def _crear_servidor(self, max_connections=1):
        modulo = importlib.import_module("src.server")
        servidor_cls = modulo.LetterCountServer
        self.error_output = io.StringIO()
        return servidor_cls(
            host=self.HOST,
            port=0,
            max_connections=max_connections,
            timeout=1.0,
            error_output=self.error_output,
        )

    def test_escribe_ip_del_cliente_en_error_estandar(self):
        """
        Iteracion 4.
        Requisito: el servidor registra en stderr la IP de cada cliente.
        """
        servidor = self._arrancar_servidor()

        respuesta = self._enviar_mensaje(servidor.port, "p:ped")

        self.assertEqual("p:1", respuesta)
        self.assertIn("127.0.0.1", self.error_output.getvalue())

    def test_escribe_mensaje_recibido_en_error_estandar(self):
        """
        Iteracion 4.
        Requisito: el servidor registra en stderr el mensaje recibido.
        """
        servidor = self._arrancar_servidor()

        respuesta = self._enviar_mensaje(servidor.port, "a,A:aAaA")

        self.assertEqual("a:2,A:2", respuesta)
        self.assertIn("a,A:aAaA", self.error_output.getvalue())

    def test_escribe_una_linea_por_conexion_en_error_estandar(self):
        """
        Iteracion 4.
        Requisito: el servidor escribe una linea de log por cada conexion.
        """
        servidor = self._arrancar_servidor(max_connections=2)

        primera = self._enviar_mensaje(servidor.port, "p:ped")
        segunda = self._enviar_mensaje(servidor.port, "d:ped")

        lineas = self.error_output.getvalue().splitlines()
        self.assertEqual("p:1", primera)
        self.assertEqual("d:1", segunda)
        self.assertEqual(2, len(lineas))
        self.assertIn("p:ped", lineas[0])
        self.assertIn("d:ped", lineas[1])
