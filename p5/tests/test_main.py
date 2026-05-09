import contextlib
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


class MainTest(unittest.TestCase):

    # ============================================================
    # Iteracion 5 - Test 5 Unitario
    #
    # Objetivo:
    # Definir el punto de entrada main.py sin ejecutar integracion real.
    #
    # Requisitos:
    # R4: El cliente mostrara la respuesta recibida por terminal.
    # Contrato: la aplicacion se lanza desde main.py y no recibe host
    # ni puerto por linea de comandos.
    # ============================================================

    def test_iteracion_5_main_client_imprime_respuesta(self):
        """
        Requisito: R4.
        Comprueba que el modo cliente delega en FileClient e imprime
        por terminal la respuesta recibida.
        """
        from main import main

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file_path = file.name

        client_instance = Mock()
        client_instance.request_file.return_value = "respuesta desde main\n"

        try:
            with patch("main.FileClient", return_value=client_instance):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    result = main(["client", file_path])

            self.assertEqual(0, result)
            self.assertEqual("respuesta desde main\n", output.getvalue())
            client_instance.request_file.assert_called_once_with(file_path)
        finally:
            os.unlink(file_path)

    def test_iteracion_5_main_server_delega_en_file_server(self):
        """
        Requisito: contrato de trabajo.
        Comprueba que el modo servidor delega el arranque en FileServer.
        """
        from main import main

        server_instance = Mock()

        with patch("main.FileServer", return_value=server_instance):
            result = main(["server"])

        self.assertEqual(0, result)
        server_instance.start.assert_called_once_with()

    def test_iteracion_5_main_rechaza_host_y_puerto_por_argumentos(self):
        """
        Requisito: contrato de trabajo.
        Comprueba que host y puerto no se pasan por linea de comandos.
        """
        from main import build_parser

        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args(["client", "/tmp/fichero.txt", "--host", "127.0.0.1"])

        with self.assertRaises(SystemExit):
            parser.parse_args(["server", "--port", "16063"])


if __name__ == "__main__":
    unittest.main()
