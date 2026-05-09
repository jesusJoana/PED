import os
import socket
import sys
import tempfile
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 16063


class ServidorTest(unittest.TestCase):

    # ============================================================
    # Iteracion 2 - Test 2 Unitario
    #
    # Objetivo:
    # Definir el comportamiento minimo de la clase FileServer.
    #
    # Requisitos:
    # R2: Uso de socket UDP de Internet.
    # R3: El servidor responde con el contenido del fichero.
    # ============================================================

    def test_iteracion_2_servidor_tiene_host_y_puerto_por_defecto(self):
        """
        Requisitos: R2, R3.
        Comprueba que el constructor configura el punto local UDP por defecto.
        """
        from server import FileServer

        server = FileServer()

        self.assertEqual(DEFAULT_HOST, server.host)
        self.assertEqual(DEFAULT_PORT, server.port)

    def test_iteracion_2_servidor_construye_respuesta_con_contenido_de_fichero(self):
        """
        Requisito: R3.
        Comprueba que el servidor devuelve el contenido de un fichero existente.
        """
        from server import FileServer

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido servido por udp\n")
            file_path = file.name

        try:
            response = FileServer().build_response(file_path)

            self.assertEqual("contenido servido por udp\n", response)
        finally:
            os.unlink(file_path)

    def test_iteracion_2_servidor_crea_socket_udp_inet(self):
        """
        Requisito: R2.
        Comprueba que el servidor crea un socket real AF_INET/SOCK_DGRAM.
        """
        from server import FileServer

        server_socket = FileServer().create_socket()

        try:
            self.assertEqual(socket.AF_INET, server_socket.family)
            self.assertEqual(socket.SOCK_DGRAM, server_socket.type)
        finally:
            server_socket.close()


if __name__ == "__main__":
    unittest.main()
