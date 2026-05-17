import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path


from src.server import UDPTextSearchServer


class TestServidorIteracion1(unittest.TestCase):
    """Tests de la Iteración 1 - Servidor."""

    def setUp(self):
        """Prepara ficheros temporales conocidos por el servidor bajo prueba."""
        self.temp_dir = tempfile.TemporaryDirectory()
        base_path = Path(self.temp_dir.name)

        self.passwd_path = base_path / "passwd"
        self.services_path = base_path / "services"

        self.passwd_path.write_text(
            "root:x:0:0:root:/root:/bin/bash\n"
            "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n"
            "usuario:x:1000:1000:Usuario:/home/usuario:/bin/bash\n",
            encoding="utf-8",
        )
        self.services_path.write_text(
            "http 80/tcp www\n"
            "xmlrpc-beep 602/tcp # XML-RPC over BEEP\n"
            "xmlrpc-beep 602/udp # XML-RPC over BEEP\n",
            encoding="utf-8",
        )

        self.server = UDPTextSearchServer(
            host="127.0.0.1",
            port=0,
            file_paths=[str(self.passwd_path), str(self.services_path)],
        )

    def tearDown(self):
        self.server.close()
        self.temp_dir.cleanup()

    def test_buscar_devuelve_numero_y_lineas_encontradas(self):
        """Iteración 1. Requisito: BUSCAR devuelve RESULTADO n y líneas completas."""
        response = self.server.handle_message("BUSCAR xmlrpc")

        self.assertEqual(
            "RESULTADO 2\n"
            "xmlrpc-beep 602/tcp # XML-RPC over BEEP\n"
            "xmlrpc-beep 602/udp # XML-RPC over BEEP",
            response,
        )

    def test_buscar_sin_resultados_devuelve_resultado_cero(self):
        """Iteración 1. Requisito: BUSCAR sin coincidencias devuelve RESULTADO 0."""
        response = self.server.handle_message("BUSCAR no encontrado")

        self.assertEqual("RESULTADO 0", response)

    def test_buscar_distingue_mayusculas_y_minusculas(self):
        """Iteración 1. Requisito: la búsqueda es sensible a mayúsculas."""
        response = self.server.handle_message("BUSCAR usuario")

        self.assertEqual(
            "RESULTADO 1\nusuario:x:1000:1000:Usuario:/home/usuario:/bin/bash",
            response,
        )

    def test_buscar_mal_formateado_devuelve_error(self):
        """Iteración 1. Requisito: BUSCAR sin cadena devuelve ERROR."""
        self.assertEqual("ERROR", self.server.handle_message("BUSCAR"))
        self.assertEqual("ERROR", self.server.handle_message("BUSCAR   "))

    def test_numero_devuelve_busquedas_ejecutadas_correctamente(self):
        """Iteración 1. Requisito: NUMERO devuelve el contador de búsquedas."""
        self.server.handle_message("BUSCAR root")
        self.server.handle_message("BUSCAR xmlrpc")

        self.assertEqual("OK 2", self.server.handle_message("NUMERO"))

    def test_salir_devuelve_ok_y_solicita_detener_servidor(self):
        """Iteración 1. Requisito: SALIR responde OK y detiene el servidor."""
        self.assertFalse(self.server.should_stop)

        response = self.server.handle_message("SALIR")

        self.assertEqual("OK", response)
        self.assertTrue(self.server.should_stop)

    def test_mensaje_desconocido_devuelve_error(self):
        """Iteración 1. Requisito: cualquier mensaje inválido devuelve ERROR."""
        self.assertEqual("ERROR", self.server.handle_message("HOLA"))
        self.assertEqual("ERROR", self.server.handle_message("numero"))
        self.assertEqual("ERROR", self.server.handle_message(""))

    def test_servidor_responde_por_udp_real(self):
        """Iteración 1. Requisito: el servidor acepta peticiones UDP reales."""
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self._wait_until_server_is_ready()

        response = self._send_udp_message("BUSCAR root")
        stop_response = self._send_udp_message("SALIR")
        thread.join(timeout=2)

        self.assertEqual(
            "RESULTADO 1\nroot:x:0:0:root:/root:/bin/bash",
            response,
        )
        self.assertEqual("OK", stop_response)
        self.assertFalse(thread.is_alive())

    def _wait_until_server_is_ready(self):
        deadline = time.time() + 2
        while self.server.bound_port is None and time.time() < deadline:
            time.sleep(0.01)
        self.assertIsNotNone(self.server.bound_port)

    def _send_udp_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.settimeout(2)
            client_socket.sendto(
                message.encode("utf-8"),
                (self.server.host, self.server.bound_port),
            )
            data, _ = client_socket.recvfrom(65535)
        return data.decode("utf-8")


if __name__ == "__main__":
    unittest.main()
