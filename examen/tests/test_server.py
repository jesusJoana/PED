import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from server import Server


class TestServerProtocolIteration1(unittest.TestCase):
    """Iteracion 1 - Test 1: pruebas unitarias del protocolo del servidor UDP."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.passwd_path = os.path.join(self.temp_dir.name, "passwd")
        self.services_path = os.path.join(self.temp_dir.name, "services")

        with open(self.passwd_path, "w", encoding="utf-8") as passwd_file:
            passwd_file.write("root:x:0:0:root:/root:/bin/bash\n")
            passwd_file.write("daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n")
            passwd_file.write("usuario:x:1000:1000:Usuario:/home/usuario:/bin/bash\n")

        with open(self.services_path, "w", encoding="utf-8") as services_file:
            services_file.write("xmlrpc-beep 602/tcp # XML-RPC over BEEP\n")
            services_file.write("xmlrpc-beep 602/udp # XML-RPC over BEEP\n")
            services_file.write("http 80/tcp www\n")

        self.server = Server(
            host="127.0.0.1",
            port=16063,
            passwd_path=self.passwd_path,
            services_path=self.services_path,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_buscar_devuelve_numero_y_lineas_encontradas(self):
        """Iteracion 1 - Requisito BUSCAR: devuelve RESULTADO, contador y lineas completas."""
        response = self.server.process_message("BUSCAR xmlrpc")

        self.assertEqual(
            response,
            "RESULTADO 2\n"
            "xmlrpc-beep 602/tcp # XML-RPC over BEEP\n"
            "xmlrpc-beep 602/udp # XML-RPC over BEEP\n",
        )

    def test_buscar_distingue_mayusculas_y_minusculas(self):
        """Iteracion 1 - Requisito BUSCAR: la busqueda es sensible a mayusculas."""
        response = self.server.process_message("BUSCAR usuario")

        self.assertEqual(
            response,
            "RESULTADO 1\nusuario:x:1000:1000:Usuario:/home/usuario:/bin/bash\n",
        )

    def test_buscar_sin_resultados_devuelve_resultado_cero(self):
        """Iteracion 1 - Requisito BUSCAR: si no hay coincidencias devuelve RESULTADO 0."""
        response = self.server.process_message("BUSCAR no_encontrado")

        self.assertEqual(response, "RESULTADO 0")

    def test_numero_devuelve_busquedas_ejecutadas(self):
        """Iteracion 1 - Requisito NUMERO: devuelve el numero de busquedas realizadas."""
        self.server.process_message("BUSCAR root")
        self.server.process_message("BUSCAR xmlrpc")

        response = self.server.process_message("NUMERO")

        self.assertEqual(response, "OK 2")

    def test_salir_devuelve_ok_y_marca_parada(self):
        """Iteracion 1 - Requisito SALIR: devuelve OK y solicita parada del servidor."""
        response = self.server.process_message("SALIR")

        self.assertEqual(response, "OK")
        self.assertTrue(self.server.should_stop)

    def test_mensaje_desconocido_devuelve_error(self):
        """Iteracion 1 - Requisito de errores: cualquier mensaje desconocido devuelve ERROR."""
        response = self.server.process_message("HOLA")

        self.assertEqual(response, "ERROR")

    def test_mensajes_mal_formados_devuelven_error(self):
        """Iteracion 1 - Requisito de errores: formatos incorrectos devuelven ERROR."""
        invalid_messages = [
            "",
            "BUSCAR",
            "BUSCAR a ver que encuentro",
            "NUMERO algo",
            "SALIR algo",
        ]

        for message in invalid_messages:
            with self.subTest(message=message):
                self.assertEqual(self.server.process_message(message), "ERROR")


class TestServerTraceIteration3(unittest.TestCase):
    """Iteracion 3 - Test 3: pruebas unitarias de trazas del servidor en stderr."""

    def test_registra_en_stderr_ip_y_mensaje_recibido(self):
        """Iteracion 3 - Requisito servidor modificado: imprime IP y mensaje en stderr."""
        server = Server()
        stderr = StringIO()

        with redirect_stderr(stderr):
            server.log_request(("192.168.1.20", 34567), "BUSCAR root")

        output = stderr.getvalue()
        self.assertIn("192.168.1.20", output)
        self.assertIn("BUSCAR root", output)

    def test_la_traza_no_altera_la_respuesta_del_protocolo(self):
        """Iteracion 3 - Requisito servidor modificado: la traza no cambia la respuesta UDP."""
        server = Server()

        response = server.process_datagram("NUMERO", ("10.0.0.5", 50000))

        self.assertEqual(response, "OK 0")


if __name__ == "__main__":
    unittest.main()
