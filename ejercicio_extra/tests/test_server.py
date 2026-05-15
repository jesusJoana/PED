import os
import tempfile
import unittest

from src.server import FileServer


class TestFileServer(unittest.TestCase):
    # Test 1 Unitario
    # Requisito: el servidor debe usar una direccion UDS configurable.
    # Comprueba que el servidor conserva la ruta de socket recibida.
    def test_servidor_guarda_ruta_socket_configurada(self):
        server = FileServer("/tmp/ped_g6_serv4.sock")
        self.assertEqual(server.socket_path, "/tmp/ped_g6_serv4.sock")

    # Test 1 Unitario
    # Requisito: el servidor debe responder con el contenido del fichero solicitado.
    # Comprueba la respuesta ante un fichero existente y legible.
    def test_devuelve_contenido_de_fichero_existente(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido de prueba\nsegunda linea")
            file_path = file.name

        try:
            server = FileServer("/tmp/ped_g6_serv4.sock")
            response = server.build_response(file_path)
            self.assertEqual(response, "contenido de prueba\nsegunda linea")
        finally:
            os.unlink(file_path)

    # Test 1 Unitario
    # Requisito: el servidor debe responder con error si no puede proporcionar el fichero.
    # Comprueba la respuesta ante un fichero inexistente.
    def test_devuelve_error_si_fichero_no_existe(self):
        server = FileServer("/tmp/ped_g6_serv4.sock")
        response = server.build_response("/tmp/fichero_inexistente_ped_g6.txt")
        self.assertIn("ERROR", response)


if __name__ == "__main__":
    unittest.main()
