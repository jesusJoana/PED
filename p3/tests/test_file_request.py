import unittest

from src.main import FileRequest


class FileRequestTest(unittest.TestCase):
    """Pruebas de la clase que construye mensajes de peticion."""

    def test_build_message_for_requested_file(self):
        """Comprueba que una peticion genera el mensaje esperado."""
        request = FileRequest("datos.txt")

        self.assertEqual("GET datos.txt", request.to_message())


if __name__ == "__main__":
    unittest.main()
