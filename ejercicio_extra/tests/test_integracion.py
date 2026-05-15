import multiprocessing
import os
import tempfile
import time
import unittest

from src.client import FileClient
from src.server import FileServer


class TestIntegracionClienteServidor(unittest.TestCase):
    def setUp(self):
        self.socket_path = tempfile.mktemp(prefix="ped_g6_integracion_", dir="/tmp")
        self.server_process = multiprocessing.Process(target=self._run_server)
        self.server_process.start()
        self._wait_for_socket(self.socket_path)

    def tearDown(self):
        if self.server_process.is_alive():
            self.server_process.terminate()
            self.server_process.join(timeout=2)

        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

    # Test 3 Integracion
    # Requisito: cliente y servidor deben comunicarse mediante socket UDS STREAM.
    # Comprueba que el cliente recibe el contenido de un fichero existente.
    def test_cliente_recibe_contenido_de_fichero_existente(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido desde integracion")
            file_path = file.name

        try:
            response = FileClient(self.socket_path).request_file(file_path)
            self.assertEqual(response, "contenido desde integracion")
        finally:
            os.unlink(file_path)

    # Test 3 Integracion
    # Requisito: el servidor debe responder con error si no puede proporcionar el fichero.
    # Comprueba la respuesta completa ante un fichero inexistente.
    def test_cliente_recibe_error_de_fichero_inexistente(self):
        response = FileClient(self.socket_path).request_file("/tmp/no_existe_ped_g6.txt")
        self.assertIn("ERROR", response)

    # Test 3 Integracion
    # Requisito: el servidor debe permitir la conexion de mas de un cliente.
    # Comprueba dos peticiones consecutivas y que el servidor sigue ejecutandose.
    def test_servidor_atiende_varios_clientes_y_sigue_vivo(self):
        first_response = FileClient(self.socket_path).request_file("/tmp/no_existe_1_ped_g6.txt")
        second_response = FileClient(self.socket_path).request_file("/tmp/no_existe_2_ped_g6.txt")

        self.assertIn("ERROR", first_response)
        self.assertIn("ERROR", second_response)
        self.assertTrue(self.server_process.is_alive())

    # Test 3 Integracion
    # Requisito: todos los sockets necesarios deben crearse dentro de /tmp.
    # Comprueba que el socket real usado por el servidor esta en /tmp.
    def test_socket_real_se_crea_en_tmp(self):
        self.assertTrue(self.socket_path.startswith("/tmp/"))
        self.assertTrue(os.path.exists(self.socket_path))

    def _run_server(self):
        FileServer(self.socket_path).serve_forever()

    def _wait_for_socket(self, socket_path):
        for _ in range(100):
            if os.path.exists(socket_path):
                return
            time.sleep(0.02)

        self.fail(f"No se creo el socket UDS de integracion: {socket_path}")


if __name__ == "__main__":
    unittest.main()
