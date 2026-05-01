import unittest

from src.main import FileResponse


class FileResponseTest(unittest.TestCase):
    """Pruebas de las respuestas enviadas por el servidor."""

    def test_build_response_with_file_content(self):
        """Comprueba que una respuesta correcta incluye el contenido."""
        response = FileResponse.with_content("contenido de prueba")

        self.assertEqual("OK\ncontenido de prueba", response.to_message())

    def test_build_file_not_found_error_response(self):
        """Comprueba que una respuesta de error informa del fichero ausente."""
        response = FileResponse.file_not_found()

        self.assertEqual("ERROR: fichero no encontrado", response.to_message())


if __name__ == "__main__":
    unittest.main()
