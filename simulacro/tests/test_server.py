import re
import socket
import threading
import time
import unittest

from src.server import ServidorTCP


class TestServidorTCP(unittest.TestCase):
    """Pruebas unitarias de la Iteracion 1: Servidor."""

    def obtener_puerto_libre(self):
        """Reserva temporalmente un puerto libre para evitar choques en tests."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    def enviar_mensaje_tcp(self, puerto, mensaje):
        """Envia un mensaje real por TCP y devuelve la respuesta decodificada."""
        with socket.create_connection(("127.0.0.1", puerto), timeout=2) as sock:
            sock.sendall(mensaje.encode("utf-8"))
            respuesta = sock.recv(1024)
        return respuesta.decode("utf-8")

    def arrancar_servidor_para_una_conexion(self, servidor):
        """Arranca el servidor en un hilo limitado a una conexion de prueba."""
        hilo = threading.Thread(
            target=servidor.iniciar,
            kwargs={"max_conexiones": 1},
            daemon=True,
        )
        hilo.start()
        time.sleep(0.1)
        return hilo

    # Iteracion 1 - Requisito: FECHA debe devolver la fecha actual del sistema.
    def test_procesar_fecha_devuelve_fecha_con_formato_esperado(self):
        servidor = ServidorTCP()

        respuesta = servidor.procesar_mensaje("FECHA")

        self.assertRegex(respuesta, r"^\d{4}-\d{2}-\d{2}$")

    # Iteracion 1 - Requisito: HORA debe devolver la hora actual del sistema.
    def test_procesar_hora_devuelve_hora_con_formato_esperado(self):
        servidor = ServidorTCP()

        respuesta = servidor.procesar_mensaje("HORA")

        self.assertRegex(respuesta, r"^\d{2}:\d{2}:\d{2}$")

    # Iteracion 1 - Requisito: cualquier mensaje no reconocido devuelve ERROR.
    def test_procesar_mensaje_no_reconocido_devuelve_error(self):
        servidor = ServidorTCP()

        respuesta = servidor.procesar_mensaje("MENSAJE_DESCONOCIDO")

        self.assertEqual("ERROR", respuesta)

    # Iteracion 1 - Requisito: la comunicacion debe usar texto UTF-8.
    def test_servidor_responde_error_a_texto_utf8_no_reconocido(self):
        puerto = self.obtener_puerto_libre()
        servidor = ServidorTCP(host="127.0.0.1", puerto=puerto)
        hilo = self.arrancar_servidor_para_una_conexion(servidor)

        respuesta = self.enviar_mensaje_tcp(puerto, "mensaje con acento: á")

        hilo.join(timeout=2)
        self.assertEqual("ERROR", respuesta)
        self.assertFalse(hilo.is_alive())

    # Iteracion 1 - Requisito: el servidor acepta conexiones TCP reales.
    def test_servidor_tcp_responde_fecha_en_una_conexion_real(self):
        puerto = self.obtener_puerto_libre()
        servidor = ServidorTCP(host="127.0.0.1", puerto=puerto)
        hilo = self.arrancar_servidor_para_una_conexion(servidor)

        respuesta = self.enviar_mensaje_tcp(puerto, "FECHA")

        hilo.join(timeout=2)
        self.assertRegex(respuesta, r"^\d{4}-\d{2}-\d{2}$")
        self.assertFalse(hilo.is_alive())


if __name__ == "__main__":
    unittest.main()
