import os
import socket
import tempfile
import threading
import time
import unittest

from src.client import FileClient


class TestFileClient(unittest.TestCase):
    # Test 2 Unitario
    # Requisito: el cliente debe conectarse al servidor mediante un socket UDS.
    # Requisito: el cliente debe enviar el path completo del fichero.
    # Comprueba que un path relativo se convierte en absoluto antes de enviarse.
    def test_cliente_envia_path_completo_al_servidor(self):
        socket_path = tempfile.mktemp(prefix="ped_g6_client_", dir="/tmp")
        received_paths = []
        thread = self._start_fake_server(socket_path, received_paths, "OK")

        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                client = FileClient(socket_path)
                response = client.request_file("fichero.txt")

                self.assertEqual(response, "OK")
                self.assertEqual(received_paths[0], os.path.join(temp_dir, "fichero.txt"))
            finally:
                os.chdir(old_cwd)
                thread.join(timeout=2)
                self._remove_socket(socket_path)

    # Test 2 Unitario
    # Requisito: el cliente debe mostrar la respuesta recibida por el servidor.
    # Comprueba que la clase cliente devuelve la respuesta completa recibida.
    def test_cliente_devuelve_respuesta_recibida_del_servidor(self):
        socket_path = tempfile.mktemp(prefix="ped_g6_client_", dir="/tmp")
        received_paths = []
        thread = self._start_fake_server(socket_path, received_paths, "respuesta del servidor")

        try:
            client = FileClient(socket_path)
            response = client.request_file("/tmp/fichero.txt")

            self.assertEqual(response, "respuesta del servidor")
        finally:
            thread.join(timeout=2)
            self._remove_socket(socket_path)

    def _start_fake_server(self, socket_path, received_paths, response):
        def fake_server():
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_socket:
                server_socket.bind(socket_path)
                server_socket.listen(1)
                connection, _ = server_socket.accept()
                with connection:
                    received_paths.append(connection.recv(4096).decode("utf-8"))
                    connection.sendall(response.encode("utf-8"))

        thread = threading.Thread(target=fake_server)
        thread.start()
        self._wait_for_socket(socket_path)
        return thread

    def _wait_for_socket(self, socket_path):
        for _ in range(50):
            if os.path.exists(socket_path):
                return
            time.sleep(0.02)
        self.fail(f"No se creo el socket de prueba: {socket_path}")

    def _remove_socket(self, socket_path):
        if os.path.exists(socket_path):
            os.unlink(socket_path)


if __name__ == "__main__":
    unittest.main()
