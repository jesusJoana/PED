import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MAIN_PATH = os.path.join(PROJECT_ROOT, "src", "main.py")
MAKEFILE_PATH = os.path.join(PROJECT_ROOT, "Makefile")
README_PATH = os.path.join(PROJECT_ROOT, "README.txt")
INSTALL_PATH = os.path.join(PROJECT_ROOT, "INSTALL.txt")
REQUIREMENTS_PATH = os.path.join(PROJECT_ROOT, "requirements.txt")
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 16063


class IntegracionTest(unittest.TestCase):

    # ============================================================
    # Iteracion 3 - Test 3 Integracion
    #
    # Objetivo:
    # Comprobar el flujo extremo a extremo con procesos y sockets TCP reales.
    #
    # Requisitos:
    # R2: Comunicacion mediante sockets TCP de Internet.
    # R3: Cliente envia peticion de fichero al servidor.
    # R4: Servidor responde con contenido de fichero.
    # R6: Cliente muestra la respuesta por salida estandar.
    # R7: Cliente termina despues de imprimir la respuesta.
    # R8: Servidor permanece vivo tras atender peticiones.
    # ============================================================

    def test_iteracion_3_cliente_recibe_contenido_desde_servidor_tcp_real(self):
        """
        Requisitos: R2, R3, R4, R6.
        Comprueba que cliente y servidor reales colaboran mediante TCP y que
        el cliente imprime el contenido del fichero solicitado.
        """
        server_process = None

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("contenido recibido desde servidor tcp\n")
            file_path = file.name

        try:
            server_process = self._start_server()

            client_process = self._run_client(file_path)

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertEqual("contenido recibido desde servidor tcp\n", client_process.stdout)
        finally:
            self._stop_process(server_process)
            os.unlink(file_path)

    def test_iteracion_3_cliente_termina_despues_de_imprimir_respuesta(self):
        """
        Requisito: R7.
        Comprueba que el proceso cliente finaliza tras recibir e imprimir la
        respuesta del servidor.
        """
        server_process = None

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("respuesta para cliente que termina\n")
            file_path = file.name

        try:
            server_process = self._start_server()

            client_process = self._run_client(file_path)

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertEqual("respuesta para cliente que termina\n", client_process.stdout)
        finally:
            self._stop_process(server_process)
            os.unlink(file_path)

    def test_iteracion_3_servidor_sigue_vivo_tras_responder(self):
        """
        Requisito: R8.
        Comprueba que el servidor no termina automaticamente tras atender una
        peticion TCP.
        """
        server_process = None

        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            file.write("respuesta para mantener servidor vivo\n")
            file_path = file.name

        try:
            server_process = self._start_server()

            client_process = self._run_client(file_path)

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertEqual("respuesta para mantener servidor vivo\n", client_process.stdout)
            time.sleep(0.2)
            self.assertIsNone(server_process.poll())
        finally:
            self._stop_process(server_process)
            os.unlink(file_path)

    def test_iteracion_3_servidor_atiende_varios_clientes_reales(self):
        """
        Requisitos: R4, R8.
        Comprueba que varios clientes reales consecutivos reciben respuesta del
        mismo servidor TCP.
        """
        server_process = None

        with tempfile.NamedTemporaryFile("w", delete=False) as first_file:
            first_file.write("respuesta primer cliente tcp\n")
            first_file_path = first_file.name

        with tempfile.NamedTemporaryFile("w", delete=False) as second_file:
            second_file.write("respuesta segundo cliente tcp\n")
            second_file_path = second_file.name

        try:
            server_process = self._start_server()

            first_client = self._run_client(first_file_path)
            second_client = self._run_client(second_file_path)

            self.assertEqual(0, first_client.returncode, first_client.stderr)
            self.assertEqual("respuesta primer cliente tcp\n", first_client.stdout)
            self.assertEqual(0, second_client.returncode, second_client.stderr)
            self.assertEqual("respuesta segundo cliente tcp\n", second_client.stdout)
        finally:
            self._stop_process(server_process)
            os.unlink(first_file_path)
            os.unlink(second_file_path)

    # ============================================================
    # Iteracion 4 - Test 4 Integracion
    #
    # Objetivo:
    # Comprobar los requisitos finales de error, nombres de proceso,
    # ejecucion mediante make y documentacion obligatoria.
    #
    # Requisitos:
    # R1: Los procesos deben contener cli6 y serv6.
    # R5: El servidor responde con error si no puede leer el fichero.
    # R6: El cliente muestra la respuesta por salida estandar.
    # Contrato PED: ejecucion desde main.py, make, requirements e INSTALL.
    # ============================================================

    def test_iteracion_4_cliente_imprime_error_de_fichero_inexistente(self):
        """
        Requisitos: R5, R6.
        Comprueba que cliente y servidor reales colaboran mediante TCP y que el
        cliente imprime el error recibido del servidor.
        """
        server_process = None
        missing_path = os.path.join(
            tempfile.gettempdir(),
            "ped_p6_fichero_inexistente_integracion_4.txt",
        )
        if os.path.exists(missing_path):
            os.unlink(missing_path)

        try:
            server_process = self._start_server()

            client_process = self._run_client(missing_path)

            self.assertEqual(0, client_process.returncode, client_process.stderr)
            self.assertTrue(client_process.stdout.startswith("ERROR:"))
            self.assertIn(missing_path, client_process.stdout)
        finally:
            self._stop_process(server_process)

    def test_iteracion_4_proceso_servidor_aparece_como_serv6_en_ps(self):
        """
        Requisito: R1.
        Comprueba que el proceso servidor aparece como serv6 en ps.
        """
        server_process = None

        try:
            server_process = self._start_server()

            server_args = self._wait_for_process_args(server_process.pid, "serv6")

            self.assertIn("serv6", server_args)
        finally:
            self._stop_process(server_process)

    def test_iteracion_4_proceso_cliente_aparece_como_cli6_en_ps(self):
        """
        Requisito: R1.
        Comprueba que el proceso cliente aparece como cli6 en ps.
        """
        server_process = None
        client_process = None
        fifo_path = os.path.join(tempfile.gettempdir(), "ped_p6_fifo_cliente_test_4")

        if os.path.exists(fifo_path):
            os.unlink(fifo_path)
        os.mkfifo(fifo_path)

        try:
            server_process = self._start_server()
            client_process = subprocess.Popen(
                [sys.executable, MAIN_PATH, "client", fifo_path],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            client_args = self._wait_for_process_args(client_process.pid, "cli6")

            self.assertIn("cli6", client_args)
        finally:
            self._stop_process(client_process)
            self._stop_process(server_process)
            if os.path.exists(fifo_path):
                os.unlink(fifo_path)

    def test_iteracion_4_makefile_lanza_cliente_y_servidor_desde_main_sin_host_ni_puerto(self):
        """
        Requisito: contrato PED.
        Comprueba que make lanza cliente y servidor desde main.py sin pasar host
        ni puerto por linea de comandos.
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

    def test_iteracion_4_documentacion_y_dependencias_obligatorias_existen(self):
        """
        Requisito: contrato PED.
        Comprueba que existen los documentos y dependencias obligatorias para
        entregar y ejecutar la practica.
        """
        self.assertTrue(os.path.exists(README_PATH), "Falta README.txt")
        self.assertTrue(os.path.exists(INSTALL_PATH), "Falta INSTALL.txt")
        self.assertTrue(os.path.exists(REQUIREMENTS_PATH), "Falta requirements.txt")

        with open(REQUIREMENTS_PATH, "r", encoding="utf-8") as requirements:
            self.assertIn("setproctitle", requirements.read())

    def _start_server(self):
        server_process = subprocess.Popen(
            [sys.executable, MAIN_PATH, "server"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._wait_for_server(server_process)
        return server_process

    def _run_client(self, file_path):
        return subprocess.run(
            [sys.executable, MAIN_PATH, "client", file_path],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def _wait_for_server(self, server_process):
        deadline = time.time() + 5
        while time.time() < deadline:
            if server_process.poll() is not None:
                self.fail("El servidor termino antes de aceptar conexiones")
            try:
                with socket.create_connection((DEFAULT_HOST, DEFAULT_PORT), timeout=0.1):
                    return
            except OSError:
                time.sleep(0.05)
        self.fail("El servidor TCP no arranco en el tiempo esperado")

    def _stop_process(self, process):
        if process is not None and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)

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
