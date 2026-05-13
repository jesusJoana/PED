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
    # Iteracion 1 - Test 1 Unitario
    #
    # Objetivo:
    # Definir el comportamiento basico del servidor TCP.
    #
    # Requisitos:
    # R2: Comunicacion mediante socket TCP de Internet.
    # R4: El servidor responde con el contenido del fichero.
    # R5: El servidor responde con error si no puede leer el fichero.
    # ============================================================

    def test_iteracion_1_servidor_tiene_host_y_puerto_por_defecto(self):
        """
        Requisito: R2.
        Comprueba que el constructor configura el punto local TCP por defecto.
        """
        from server import FileServer

        server = FileServer()

        self.assertEqual(DEFAULT_HOST, server.host)
        self.assertEqual(DEFAULT_PORT, server.port)

    def test_iteracion_1_servidor_crea_socket_tcp_inet(self):
        """
        Requisito: R2.
        Comprueba que el servidor crea un socket real AF_INET/SOCK_STREAM.
        """
        from server import FileServer

        server_socket = FileServer().create_socket()

        try:
            self.assertEqual(socket.AF_INET, server_socket.family)
            self.assertEqual(socket.SOCK_STREAM, server_socket.type)
        finally:
            server_socket.close()

    def test_iteracion_1_servidor_construye_respuesta_con_contenido_de_fichero(self):
        """
        Requisito: R4.
        Comprueba que el servidor devuelve el contenido de un fichero existente.
        """
        from server import FileServer

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido servido por tcp\n")
            file_path = file.name

        try:
            response = FileServer().build_response(file_path)

            self.assertEqual("contenido servido por tcp\n", response)
        finally:
            os.unlink(file_path)

    def test_iteracion_1_servidor_devuelve_error_para_fichero_inexistente(self):
        """
        Requisito: R5.
        Comprueba que el servidor devuelve un mensaje textual de error
        cuando el fichero solicitado no existe.
        """
        from server import FileServer

        missing_path = os.path.join(
            tempfile.gettempdir(),
            "ped_p6_fichero_inexistente_test_1.txt",
        )
        if os.path.exists(missing_path):
            os.unlink(missing_path)

        response = FileServer().build_response(missing_path)

        self.assertTrue(response.startswith("ERROR:"))
        self.assertIn(missing_path, response)

    # ============================================================
    # Iteracion 2 - Test 2 Unitario
    #
    # Objetivo:
    # Definir el procesamiento de una peticion TCP individual.
    #
    # Requisitos:
    # R3: El cliente envia una peticion de fichero.
    # R4: El servidor responde con el contenido del fichero.
    # R5: El servidor responde con error si no puede leer el fichero.
    # R8: Atender una peticion individual no implica finalizar el servidor.
    # ============================================================

    def test_iteracion_2_servidor_procesa_peticion_de_fichero_existente(self):
        """
        Requisitos: R3, R4, R8.
        Comprueba que el servidor procesa una ruta recibida como peticion
        individual y devuelve la respuesta correspondiente.
        """
        from server import FileServer

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("respuesta desde process_request tcp\n")
            file_path = file.name

        try:
            response = FileServer().process_request(file_path)

            self.assertEqual("respuesta desde process_request tcp\n", response)
        finally:
            os.unlink(file_path)

    def test_iteracion_2_servidor_atiende_conexion_individual(self):
        """
        Requisitos: R3, R4, R8.
        Comprueba que el servidor lee una peticion desde una conexion,
        envia la respuesta por esa misma conexion y cierra solo el cliente.
        """
        from server import FileServer

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("respuesta desde handle_client tcp\n")
            file_path = file.name

        connection = FakeConnection([file_path.encode("utf-8"), b""])

        try:
            FileServer().handle_client(connection)

            self.assertEqual(
                "respuesta desde handle_client tcp\n",
                b"".join(connection.sent_data).decode("utf-8"),
            )
            self.assertTrue(connection.closed)
        finally:
            os.unlink(file_path)


class FakeConnection:
    def __init__(self, received_data):
        self.received_data = list(received_data)
        self.sent_data = []
        self.closed = False

    def recv(self, _buffer_size):
        if self.received_data:
            return self.received_data.pop(0)
        return b""

    def sendall(self, data):
        self.sent_data.append(data)

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.close()


if __name__ == "__main__":
    unittest.main()
