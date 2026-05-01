import unittest

from src.main import FileRequest


class FileRequestTest(unittest.TestCase):
    """Pruebas de la clase que construye mensajes de peticion."""

    def test_build_message_for_requested_file(self):
        """Comprueba que una peticion genera el mensaje esperado."""
        request = FileRequest("datos.txt")

        self.assertEqual("GET datos.txt", request.to_message())

    def test_parse_requested_file_from_message(self):
        """Comprueba que se extrae el fichero de una peticion recibida."""
        request = FileRequest.from_message("GET datos.txt")

        self.assertEqual("datos.txt", request.filename)


if __name__ == "__main__":
    unittest.main()
