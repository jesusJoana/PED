import os
import subprocess
import sys
import tempfile
import time
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MAIN_PATH = os.path.join(PROJECT_ROOT, "src", "main.py")
MAKEFILE_PATH = os.path.join(PROJECT_ROOT, "Makefile")


class IntegracionTest(unittest.TestCase):

    # ============================================================
    # Iteracion 6 - Test 6 Integracion
    #
    # Objetivo:
    # Comprobar el flujo extremo a extremo con procesos y sockets UDP reales.
    #
    # Requisitos:
    # R2: Cliente envia peticion mediante UDP.
    # R3: Servidor responde con contenido de fichero.
    # R4: Cliente muestra la respuesta por terminal.
    # Contrato: ejecucion desde main.py y mediante make.
    # ============================================================

    def test_iteracion_6_cliente_recibe_contenido_desde_servidor_udp_real(self):
        """
        Requisitos: R2, R3, R4.
        Comprueba que cliente y servidor reales colaboran mediante UDP
        y que el cliente imprime el contenido del fichero solicitado.
        """
        server_process = None

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido recibido desde servidor udp\n")
            file_path = file.name

        try:
            server_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "server"],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(0.3)

            client_process = subprocess.run(
                [sys.executable, MAIN_PATH, "client", file_path],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertEqual("contenido recibido desde servidor udp\n", client_process.stdout)
        finally:
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)
            os.unlink(file_path)

    def test_iteracion_6_makefile_lanza_cliente_y_servidor_desde_main_sin_host_ni_puerto(self):
        """
        Requisito: contrato de trabajo.
        Comprueba que make lanza cliente y servidor desde main.py sin
        pasar host ni puerto por linea de comandos.
        """
        self.assertTrue(os.path.exists(MAKEFILE_PATH), "Falta Makefile")

        with open(MAKEFILE_PATH, "r", encoding="utf-8") as makefile:
            content = makefile.read()

        self.assertIn("test:", content)
        self.assertIn("server:", content)
        self.assertIn("client:", content)
        self.assertIn("src/main.py server", content)
        self.assertIn("src/main.py client", content)
        self.assertNotIn("--host", content)
        self.assertNotIn("--port", content)

    # ============================================================
    # Iteracion 7 - Test 7 Integracion
    #
    # Objetivo:
    # Comprobar el flujo real cuando el fichero solicitado no existe.
    #
    # Requisitos:
    # R3: Servidor responde con mensaje de error si no puede devolver
    #     el fichero.
    # R4: Cliente muestra la respuesta por terminal.
    # ============================================================

    def test_iteracion_7_cliente_imprime_error_de_fichero_inexistente(self):
        """
        Requisitos: R3, R4.
        Comprueba que cliente y servidor reales colaboran mediante UDP
        y que el cliente imprime el error recibido del servidor.
        """
        server_process = None
        missing_path = os.path.join(
            tempfile.gettempdir(),
            "ped_p5_fichero_inexistente_integracion_7.txt",
        )
        if os.path.exists(missing_path):
            os.unlink(missing_path)

        try:
            server_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "server"],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(0.3)

            client_process = subprocess.run(
                [sys.executable, MAIN_PATH, "client", missing_path],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertTrue(client_process.stdout.startswith("ERROR:"))
            self.assertIn(missing_path, client_process.stdout)
        finally:
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)

    # ============================================================
    # Iteracion 8 - Test 8 Integracion
    #
    # Objetivo:
    # Comprobar que el servidor atiende mas de un cliente y permanece vivo.
    #
    # Requisitos:
    # R5: El servidor permite mas de un cliente simultaneamente.
    # R6: El servidor no se cierra al terminar una peticion.
    # ============================================================

    def test_iteracion_8_servidor_atiende_varios_clientes_reales(self):
        """
        Requisitos: R5, R6.
        Comprueba que varios clientes reales reciben respuesta del mismo
        servidor UDP.
        """
        server_process = None

        with tempfile.NamedTemporaryFile("w", delete=False) as first_file:
            first_file.write("respuesta primer cliente\n")
            first_file_path = first_file.name

        with tempfile.NamedTemporaryFile("w", delete=False) as second_file:
            second_file.write("respuesta segundo cliente\n")
            second_file_path = second_file.name

        try:
            server_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "server"],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(0.3)

            first_client = self._run_client(first_file_path)
            second_client = self._run_client(second_file_path)

            self.assertEqual(0, first_client.returncode, first_client.stderr)
            self.assertEqual("respuesta primer cliente\n", first_client.stdout)
            self.assertEqual(0, second_client.returncode, second_client.stderr)
            self.assertEqual("respuesta segundo cliente\n", second_client.stdout)
        finally:
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)
            os.unlink(first_file_path)
            os.unlink(second_file_path)

    def test_iteracion_8_servidor_sigue_vivo_tras_responder(self):
        """
        Requisito: R6.
        Comprueba que el proceso servidor no termina automaticamente tras
        responder a una peticion.
        """
        server_process = None

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("respuesta para mantener servidor vivo\n")
            file_path = file.name

        try:
            server_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "server"],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(0.3)

            client_process = self._run_client(file_path)

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertEqual("respuesta para mantener servidor vivo\n", client_process.stdout)
            time.sleep(0.2)
            self.assertIsNone(server_process.poll())
        finally:
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)
            os.unlink(file_path)

    def _run_client(self, file_path):
        return subprocess.run(
            [sys.executable, MAIN_PATH, "client", file_path],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    # ============================================================
    # Iteracion 9 - Test 9 Integracion
    #
    # Objetivo:
    # Comprobar con ps los nombres de proceso pedidos por el enunciado.
    #
    # Requisitos:
    # R1: Los procesos cliente y servidor deben contener cli5 y serv5.
    # ============================================================

    def test_iteracion_9_proceso_servidor_aparece_como_serv5_en_ps(self):
        """
        Requisito: R1.
        Comprueba que el proceso servidor aparece como serv5 en ps.
        """
        server_process = None

        try:
            server_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "server"],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            server_args = self._wait_for_process_args(server_process.pid, "serv5")

            self.assertIn("serv5", server_args)
        finally:
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)

    def test_iteracion_9_proceso_cliente_aparece_como_cli5_en_ps(self):
        """
        Requisito: R1.
        Comprueba que el proceso cliente aparece como cli5 en ps.
        """
        server_process = None
        client_process = None
        fifo_path = os.path.join(tempfile.gettempdir(), "ped_p5_fifo_cliente_test_9")

        if os.path.exists(fifo_path):
            os.unlink(fifo_path)
        os.mkfifo(fifo_path)

        try:
            server_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "server"],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(0.3)

            client_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "client", fifo_path],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            client_args = self._wait_for_process_args(client_process.pid, "cli5")

            self.assertIn("cli5", client_args)
        finally:
            if client_process is not None and client_process.poll() is None:
                client_process.terminate()
                client_process.wait(timeout=5)
            if server_process is not None and server_process.poll() is None:
                server_process.terminate()
                server_process.wait(timeout=5)
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


if __name__ == "__main__":
    unittest.main()
