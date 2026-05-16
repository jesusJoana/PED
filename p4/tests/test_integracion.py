import os
import subprocess
import sys
import tempfile
import time
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MAIN_PATH = os.path.join(PROJECT_ROOT, "src", "main.py")
SERV4_PATH = os.path.join(PROJECT_ROOT, "serv4")
CLI4_PATH = os.path.join(PROJECT_ROOT, "cli4")
README_PATH = os.path.join(PROJECT_ROOT, "README.txt")
INSTALL_PATH = os.path.join(PROJECT_ROOT, "INSTALL.txt")


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

    # ============================================================
    # Iteracion 3
    # ============================================================

    def test_iteracion_3_procesos_muestran_serv4_y_cli4_en_ps(self):
        socket_path = os.path.join(tempfile.gettempdir(), "serv4_integracion_3.sock")
        fifo_path = os.path.join(tempfile.gettempdir(), "fifo_cli4_integracion_3")
        server_process = None
        client_process = None

        self.assertTrue(os.path.exists(SERV4_PATH), "No existe el ejecutable serv4")
        self.assertTrue(os.access(SERV4_PATH, os.X_OK), "serv4 no es ejecutable")
        self.assertTrue(os.path.exists(CLI4_PATH), "No existe el ejecutable cli4")
        self.assertTrue(os.access(CLI4_PATH, os.X_OK), "cli4 no es ejecutable")

        if os.path.exists(socket_path):
            os.unlink(socket_path)
        if os.path.exists(fifo_path):
            os.unlink(fifo_path)

        os.mkfifo(fifo_path)

        try:
            server_process = subprocess.Popen(
                [SERV4_PATH, "--socket", socket_path],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self._wait_for_socket(socket_path)

            self.assertIn("serv4", self._ps_args(server_process.pid))

            # El FIFO mantiene al cliente bloqueado esperando respuesta,
            # lo que permite comprobar su nombre mediante ps.
            client_process = subprocess.Popen(
                [CLI4_PATH, fifo_path, "--socket", socket_path],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            client_args = self._wait_for_process_args(client_process.pid, "cli4")
            self.assertIn("cli4", client_args)
        finally:
            if client_process is not None and client_process.poll() is None:
                client_process.terminate()
                client_process.wait(timeout=5)
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)
            if os.path.exists(socket_path):
                os.unlink(socket_path)
            if os.path.exists(fifo_path):
                os.unlink(fifo_path)

    def _ps_args(self, pid):
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "args="],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return result.stdout.strip()

    def _wait_for_process_args(self, pid, expected_text):
        deadline = time.time() + 5
        while time.time() < deadline:
            args = self._ps_args(pid)
            if expected_text in args:
                return args
            time.sleep(0.05)
        self.fail(f"No aparece {expected_text} en ps para el proceso {pid}")

    # ============================================================
    # Iteracion 4
    # ============================================================

    def test_iteracion_4_readme_e_install_existen_y_documentan_uso(self):
        self.assertTrue(os.path.exists(README_PATH), "Falta README.txt")
        self.assertTrue(os.path.exists(INSTALL_PATH), "Falta INSTALL.txt")

        with open(README_PATH, "r", encoding="utf-8") as readme:
            readme_content = readme.read()

        with open(INSTALL_PATH, "r", encoding="utf-8") as install:
            install_content = install.read()

        for expected_text in ["cliente-servidor", "UDS", "make server", "make client"]:
            self.assertIn(expected_text, readme_content)

        for expected_text in ["make install", "make test", "make server", "make client"]:
            self.assertIn(expected_text, install_content)


if __name__ == "__main__":
    unittest.main()
