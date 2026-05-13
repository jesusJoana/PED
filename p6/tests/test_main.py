import os
import sys
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


class MainTest(unittest.TestCase):

    # ============================================================
    # Iteracion 2 - Test 2 Unitario
    #
    # Objetivo:
    # Definir el punto de entrada unico exigido por el contrato.
    #
    # Requisitos:
    # Contrato PED: La aplicacion cliente-servidor debe lanzarse desde main.py.
    # R7: El cliente termina despues de imprimir la respuesta.
    # ============================================================

    def test_iteracion_2_parser_acepta_modos_cliente_y_servidor(self):
        """
        Requisito: contrato PED.
        Comprueba que el parser acepta los modos principales de ejecucion.
        """
        from main import build_parser

        parser = build_parser()

        server_args = parser.parse_args(["server"])
        client_args = parser.parse_args(["client", "/tmp/fichero.txt"])

        self.assertEqual("server", server_args.mode)
        self.assertEqual("client", client_args.mode)
        self.assertEqual("/tmp/fichero.txt", client_args.file)

    def test_iteracion_2_main_client_sin_fichero_finaliza_con_error(self):
        """
        Requisito: contrato PED.
        Comprueba que el modo cliente exige la ruta del fichero solicitado.
        """
        from main import main

        with self.assertRaises(SystemExit) as context:
            main(["client"])

        self.assertNotEqual(0, context.exception.code)


if __name__ == "__main__":
    unittest.main()
