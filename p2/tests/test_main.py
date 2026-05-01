"""Pruebas iniciales para asegurar que la estructura del proyecto funciona."""

import contextlib
import io
import unittest

from src import main


class MainModuleTest(unittest.TestCase):
    """Comprueba que el modulo principal ya esta disponible para iterar."""

    def test_main_function_exists(self):
        """El proyecto debe exponer una funcion main como punto de entrada."""
        self.assertTrue(callable(main.main))

    def test_validate_args_accepts_one_file_path(self):
        """La ejecucion correcta recibe exactamente una ruta de fichero."""
        self.assertEqual(main.validate_args(["datos.txt"]), "datos.txt")

    def test_validate_args_rejects_missing_file_path(self):
        """Sin ruta de fichero no sabemos que debe pedir el cliente."""
        with self.assertRaisesRegex(ValueError, "Uso"):
            main.validate_args([])

    def test_validate_args_rejects_too_many_arguments(self):
        """El programa solo acepta un fichero por ejecucion."""
        with self.assertRaisesRegex(ValueError, "Uso"):
            main.validate_args(["uno.txt", "dos.txt"])

    def test_main_returns_error_when_arguments_are_invalid(self):
        """main convierte los errores de uso en codigo de salida fallido."""
        error_output = io.StringIO()

        with contextlib.redirect_stderr(error_output):
            exit_code = main.main([])

        self.assertEqual(exit_code, 1)
        self.assertIn("Uso:", error_output.getvalue())

    def test_main_returns_success_when_arguments_are_valid(self):
        """Con argumentos validos, esta iteracion todavia termina sin fork."""
        self.assertEqual(main.main(["datos.txt"]), 0)


if __name__ == "__main__":
    unittest.main()
