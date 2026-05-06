import os
import subprocess
import sys
import tempfile
import time
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MAIN_PATH = os.path.join(PROJECT_ROOT, "src", "main.py")


class IntegracionTest(unittest.TestCase):

    # ============================================================
    # Iteracion 1
    # ============================================================

    def test_iteracion_1_cliente_recibe_contenido_desde_servidor_real(self):
        socket_path = os.path.join(tempfile.gettempdir(), "serv4_integracion_1.sock")
        server_process = None

        if os.path.exists(socket_path):
            os.unlink(socket_path)

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido servido por uds\n")
            file_path = file.name

        try:
            server_process = subprocess.Popen(
                [
                    sys.executable,
                    MAIN_PATH,
                    "server",
                    "--socket",
                    socket_path,
                ],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self._wait_for_socket(socket_path)

            client_process = subprocess.run(
                [
                    sys.executable,
                    MAIN_PATH,
                    "client",
                    file_path,
                    "--socket",
                    socket_path,
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertEqual("contenido servido por uds\n", client_process.stdout)
        finally:
            if server_process is not None:
                server_process.terminate()
                server_process.wait(timeout=5)
            if os.path.exists(socket_path):
                os.unlink(socket_path)
            os.unlink(file_path)

    def _wait_for_socket(self, socket_path):
        deadline = time.time() + 5
        while time.time() < deadline:
            if os.path.exists(socket_path):
                return
            time.sleep(0.05)
        self.fail("El servidor no creo el socket UDS a tiempo")

    # ============================================================
    # Iteracion 2
    # ============================================================

    def test_iteracion_2_servidor_atiende_mas_de_un_cliente(self):
        socket_path = os.path.join(tempfile.gettempdir(), "serv4_integracion_2.sock")
        server_process = None

        if os.path.exists(socket_path):
            os.unlink(socket_path)

        with tempfile.NamedTemporaryFile("w", delete=False) as first_file:
            first_file.write("respuesta primer cliente\n")
            first_file_path = first_file.name

        with tempfile.NamedTemporaryFile("w", delete=False) as second_file:
            second_file.write("respuesta segundo cliente\n")
            second_file_path = second_file.name

        try:
            server_process = subprocess.Popen(
                [
                    sys.executable,
                    MAIN_PATH,
                    "server",
                    "--socket",
                    socket_path,
                ],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self._wait_for_socket(socket_path)

            first_client = self._run_client(first_file_path, socket_path)
            second_client = self._run_client(second_file_path, socket_path)

            self.assertEqual(0, first_client.returncode, first_client.stderr)
            self.assertEqual("respuesta primer cliente\n", first_client.stdout)
            self.assertEqual(0, second_client.returncode, second_client.stderr)
            self.assertEqual("respuesta segundo cliente\n", second_client.stdout)
            self.assertIsNone(server_process.poll())
        finally:
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)
            if os.path.exists(socket_path):
                os.unlink(socket_path)
            os.unlink(first_file_path)
            os.unlink(second_file_path)

    def _run_client(self, file_path, socket_path):
        return subprocess.run(
            [
                sys.executable,
                MAIN_PATH,
                "client",
                file_path,
                "--socket",
                socket_path,
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
