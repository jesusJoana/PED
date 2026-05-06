import os
import sys
import tempfile
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)


class FileServerTest(unittest.TestCase):

    # ============================================================
    # Iteracion 1
    # ============================================================

    def test_iteracion_1_socket_por_defecto_esta_en_tmp(self):
        from server import FileServer

        server = FileServer()

        self.assertTrue(server.socket_path.startswith("/tmp/"))

    def test_iteracion_1_devuelve_contenido_de_fichero_existente(self):
        from server import FileServer

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido de prueba\nsegunda linea\n")
            file_path = file.name

        try:
            server = FileServer()
            response = server.build_response(file_path)

            self.assertEqual("contenido de prueba\nsegunda linea\n", response)
        finally:
            os.unlink(file_path)

    def test_iteracion_1_devuelve_error_si_el_fichero_no_existe(self):
        from server import FileServer

        missing_path = "/tmp/fichero_inexistente_p4.txt"
        server = FileServer()

        response = server.build_response(missing_path)

        self.assertIn("ERROR", response)
        self.assertIn(missing_path, response)


if __name__ == "__main__":
    unittest.main()
