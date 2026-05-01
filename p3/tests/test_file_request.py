import unittest

from src.main import FileRequest


class FileRequestTest(unittest.TestCase):
    """Pruebas de la clase que construye mensajes de peticion."""

    def test_build_message_for_requested_file(self):
        """Comprueba que una peticion genera el mensaje esperado."""
        request = FileRequest("datos.txt")

        self.assertEqual("GET datos.txt", request.to_message())

    def test_build_message_for_another_requested_file(self):
        """Comprueba que el mensaje usa el nombre recibido por la peticion."""
        request = FileRequest("informe.txt")

        self.assertEqual("GET informe.txt", request.to_message())

    def test_parse_requested_file_from_message(self):
        """Comprueba que se extrae el fichero de una peticion recibida."""
        request = FileRequest.from_message("GET datos.txt")

        self.assertEqual("datos.txt", request.filename)

    def test_parse_message_with_extra_spaces(self):
        """Comprueba que se aceptan espacios extra alrededor del mensaje."""
        request = FileRequest.from_message("  GET   datos.txt  ")

        self.assertEqual("datos.txt", request.filename)

    def test_reject_invalid_request_command(self):
        """Comprueba que se rechaza una peticion con un comando no valido."""
        with self.assertRaises(ValueError):
            FileRequest.from_message("POST datos.txt")


if __name__ == "__main__":
    unittest.main()
