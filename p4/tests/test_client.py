import os
import socket
import sys
import tempfile
import threading
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)


class FileClientTest(unittest.TestCase):

    # ============================================================
    # Iteracion 1
    # ============================================================

    def test_iteracion_1_rechaza_paths_relativos(self):
        from client import FileClient

        client = FileClient(socket_path="/tmp/test_cli4.sock")

        with self.assertRaises(ValueError):
            client.request_file("relativo.txt")

    def test_iteracion_1_envia_path_absoluto_y_recibe_respuesta(self):
        from client import FileClient

        socket_path = os.path.join(tempfile.gettempdir(), "test_cli4_unit.sock")
        requested_path = "/tmp/fichero_cliente_unitario.txt"
        expected_response = "respuesta desde socket real\n"
        received_paths = []
        server_ready = threading.Event()

        if os.path.exists(socket_path):
            os.unlink(socket_path)

        def fake_server():
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_socket:
                server_socket.bind(socket_path)
                server_socket.listen(1)
                server_ready.set()
                connection, _ = server_socket.accept()
                with connection:
                    data = connection.recv(4096).decode("utf-8").strip()
                    received_paths.append(data)
                    connection.sendall(expected_response.encode("utf-8"))

        thread = threading.Thread(target=fake_server, daemon=True)
        thread.start()
        self.assertTrue(server_ready.wait(timeout=2))

        try:
            client = FileClient(socket_path=socket_path)
            response = client.request_file(requested_path)

            self.assertEqual(expected_response, response)
            self.assertEqual([requested_path], received_paths)
        finally:
            thread.join(timeout=2)
            if os.path.exists(socket_path):
                os.unlink(socket_path)


if __name__ == "__main__":
    unittest.main()
