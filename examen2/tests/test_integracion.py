import io
import os
import socket
import subprocess
import sys
import time
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.client import UDPInfoClient


HOST = "127.0.0.1"
TIMEOUT = 2.0


class TestIntegracionIteracion3(unittest.TestCase):
    """Iteracion 3: pruebas reales de integracion cliente-servidor."""

    def _puerto_libre(self):
        """Obtiene un puerto local libre para lanzar el servidor real."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, 0))
            return sock.getsockname()[1]

    def _arrancar_servidor_real(self, port):
        """Arranca el servidor real en otro proceso usando el punto de entrada."""
        env = os.environ.copy()
        env["PED_HOST"] = HOST
        env["PED_PORT"] = str(port)
        return subprocess.Popen(
            [sys.executable, "-m", "src.main"],
            cwd=PROJECT_ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def _esperar_servidor(self, process, port):
        """Espera brevemente a que el servidor acepte datagramas UDP."""
        deadline = time.time() + TIMEOUT
        while time.time() < deadline:
            if process.poll() is not None:
                self.fail("El servidor termino antes de aceptar mensajes")

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(0.1)
                try:
                    sock.sendto("NUMERO".encode("utf-8"), (HOST, port))
                    data, _address = sock.recvfrom(65535)
                    if data.decode("utf-8").startswith("OK"):
                        return
                except OSError:
                    time.sleep(0.05)

        self.fail("El servidor no quedo listo en el puerto de integracion")

    def _cerrar_servidor(self, process, port):
        """Cierra el servidor si la prueba falla antes de enviar SALIR."""
        if process.poll() is not None:
            return

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(0.2)
            try:
                sock.sendto("SALIR".encode("utf-8"), (HOST, port))
                sock.recvfrom(65535)
            except OSError:
                process.terminate()

        try:
            process.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=TIMEOUT)

    def test_cliente_y_servidor_reales_ejecutan_protocolo_completo(self):
        """
        Iteracion 3 - Integracion.
        Requisito: cliente y servidor reales se comunican por UDP.
        """
        port = self._puerto_libre()
        server_process = self._arrancar_servidor_real(port)
        self.addCleanup(self._cerrar_servidor, server_process, port)
        self._esperar_servidor(server_process, port)
        output = io.StringIO()
        client = UDPInfoClient(
            host=HOST,
            port=port,
            messages=["BUSCAR root", "NUMERO", "SALIR"],
            timeout=TIMEOUT,
        )

        client.run(output=output)
        server_process.wait(timeout=TIMEOUT)

        printed = output.getvalue()
        self.assertIn("root", printed)
        self.assertIn("OK 1", printed)
        self.assertIn("OK", printed)
        self.assertEqual(0, server_process.returncode)

    def test_cliente_y_servidor_reales_responden_error_a_mensaje_invalido(self):
        """
        Iteracion 3 - Integracion.
        Requisito: el protocolo real responde ERROR ante mensajes invalidos.
        """
        port = self._puerto_libre()
        server_process = self._arrancar_servidor_real(port)
        self.addCleanup(self._cerrar_servidor, server_process, port)
        self._esperar_servidor(server_process, port)
        output = io.StringIO()
        client = UDPInfoClient(
            host=HOST,
            port=port,
            messages=["MENSAJE INVALIDO", "SALIR"],
            timeout=TIMEOUT,
        )

        client.run(output=output)
        server_process.wait(timeout=TIMEOUT)

        self.assertIn("ERROR", output.getvalue())
        self.assertIn("OK", output.getvalue())
        self.assertEqual(0, server_process.returncode)


if __name__ == "__main__":
    unittest.main()
