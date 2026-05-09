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


if __name__ == "__main__":
    unittest.main()
