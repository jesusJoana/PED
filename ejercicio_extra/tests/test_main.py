import unittest

from src.main import ApplicationLauncher


class TestApplicationLauncher(unittest.TestCase):
    # Test 2 Unitario
    # Requisito: la aplicacion cliente-servidor debe lanzarse desde main.py.
    # Comprueba que el modo servidor se acepta como argumento valido.
    def test_acepta_modo_server(self):
        launcher = ApplicationLauncher("config.txt")
        self.assertEqual(launcher.parse_args(["server"]), ("server", None))

    # Test 2 Unitario
    # Requisito: la aplicacion cliente-servidor debe lanzarse desde main.py.
    # Comprueba que el modo cliente acepta un path de fichero.
    def test_acepta_modo_client_con_path(self):
        launcher = ApplicationLauncher("config.txt")
        self.assertEqual(
            launcher.parse_args(["client", "/tmp/fichero.txt"]),
            ("client", "/tmp/fichero.txt"),
        )

    # Test 2 Unitario
    # Requisito: el cliente necesita el path completo de un fichero para pedirlo.
    # Comprueba que el modo cliente rechaza la llamada sin path.
    def test_rechaza_modo_client_sin_path(self):
        launcher = ApplicationLauncher("config.txt")
        with self.assertRaises(ValueError):
            launcher.parse_args(["client"])

    # Test 2 Unitario
    # Requisito: el proceso servidor debe contener la cadena serv4 en su nombre.
    # Comprueba que main.py prepara un nombre valido para el servidor.
    def test_nombre_proceso_servidor_contiene_serv4(self):
        launcher = ApplicationLauncher("config.txt")
        self.assertIn("serv4", launcher.process_name_for("server"))

    # Test 2 Unitario
    # Requisito: el proceso cliente debe contener la cadena cli4 en su nombre.
    # Comprueba que main.py prepara un nombre valido para el cliente.
    def test_nombre_proceso_cliente_contiene_cli4(self):
        launcher = ApplicationLauncher("config.txt")
        self.assertIn("cli4", launcher.process_name_for("client"))


if __name__ == "__main__":
    unittest.main()
