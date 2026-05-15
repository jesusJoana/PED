import os
import tempfile
import unittest

from src.config import SocketConfig


class TestSocketConfig(unittest.TestCase):
    # Test 1 Unitario
    # Requisito: la direccion del socket UDS debe ser configurable sin recompilar.
    # Comprueba que la configuracion lee la ruta del socket desde un fichero.
    def test_lee_ruta_socket_desde_fichero_configuracion(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as config_file:
            config_file.write("/tmp/ped_g6_serv4.sock\n")
            config_path = config_file.name

        try:
            config = SocketConfig(config_path)
            self.assertEqual(config.read_socket_path(), "/tmp/ped_g6_serv4.sock")
        finally:
            os.unlink(config_path)

    # Test 1 Unitario
    # Requisito: la direccion configurable debe ser valida para poder crear el socket.
    # Comprueba que una configuracion vacia se rechaza.
    def test_rechaza_configuracion_vacia(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as config_file:
            config_path = config_file.name

        try:
            config = SocketConfig(config_path)
            with self.assertRaises(ValueError):
                config.read_socket_path()
        finally:
            os.unlink(config_path)

    # Test 1 Unitario
    # Requisito: todos los sockets de la practica deben crearse dentro de /tmp.
    # Comprueba que se rechazan rutas fuera de /tmp.
    def test_rechaza_socket_fuera_de_tmp(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as config_file:
            config_file.write("/home/usuario/socket_no_valido.sock\n")
            config_path = config_file.name

        try:
            config = SocketConfig(config_path)
            with self.assertRaises(ValueError):
                config.read_socket_path()
        finally:
            os.unlink(config_path)


if __name__ == "__main__":
    unittest.main()
