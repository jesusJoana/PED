import tempfile
import unittest
from pathlib import Path

from src.main import FileServer


class FileServerTest(unittest.TestCase):
    """Pruebas del servidor que lee ficheros de texto."""

    def test_read_existing_text_file(self):
        """Comprueba que el servidor lee el contenido de un fichero existente."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "datos.txt"
            file_path.write_text("contenido de prueba", encoding="utf-8")
            server = FileServer()

            self.assertEqual("contenido de prueba", server.read_file(file_path))

    def test_read_multiline_text_file(self):
        """Comprueba que el servidor conserva saltos de linea del fichero."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "lineas.txt"
            file_path.write_text("linea 1\nlinea 2\n", encoding="utf-8")
            server = FileServer()

            self.assertEqual("linea 1\nlinea 2\n", server.read_file(file_path))

    def test_build_error_response_when_file_does_not_exist(self):
        """Comprueba que el servidor responde con error si falta el fichero."""
        server = FileServer()

        response = server.build_response_for_file(Path("no_existe.txt"))

        self.assertEqual("ERROR: fichero no encontrado", response.to_message())


if __name__ == "__main__":
    unittest.main()
