"""Pruebas iniciales para asegurar que la estructura del proyecto funciona."""

import unittest

from src import main


class MainModuleTest(unittest.TestCase):
    """Comprueba que el modulo principal ya esta disponible para iterar."""

    def test_main_function_exists(self):
        """El proyecto debe exponer una funcion main como punto de entrada."""
        self.assertTrue(callable(main.main))

    def test_main_returns_success_code(self):
        """Por ahora main termina correctamente sin ejecutar logica real."""
        self.assertEqual(main.main(), 0)


if __name__ == "__main__":
    unittest.main()
