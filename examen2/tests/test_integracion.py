import io
import tempfile
import threading
import time
import unittest
from pathlib import Path


from src.client import UDPTextSearchClient
from src.server import UDPTextSearchServer


class TestIntegracionIteracion3(unittest.TestCase):
    """Tests de la Iteración 3 - Integración cliente-servidor."""

    def setUp(self):
        """Prepara ficheros temporales para un servidor real bajo prueba."""
        self.temp_dir = tempfile.TemporaryDirectory()
        base_path = Path(self.temp_dir.name)

        self.passwd_path = base_path / "passwd"
        self.services_path = base_path / "services"

        self.passwd_path.write_text(
            "root:x:0:0:root:/root:/bin/bash\n"
            "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n",
            encoding="utf-8",
        )
        self.services_path.write_text(
            "xmlrpc-beep 602/tcp # XML-RPC over BEEP\n",
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

    def test_cliente_real_y_servidor_real_completan_flujo_udp(self):
        """Iteración 3. Requisito: cliente y servidor reales colaboran por UDP."""
        server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        server_thread.start()
        self._wait_until_server_is_ready()
        output = io.StringIO()

        client = UDPTextSearchClient(
            host=self.server.host,
            port=self.server.bound_port,
            messages=["NUMERO", "BUSCAR root", "SALIR"],
            timeout=1,
        )
        client.run(output=output)
        server_thread.join(timeout=2)

        self.assertEqual(
            "OK 0\n"
            "RESULTADO 1\n"
            "root:x:0:0:root:/root:/bin/bash\n"
            "OK\n",
            output.getvalue(),
        )
        self.assertFalse(server_thread.is_alive())

    def _wait_until_server_is_ready(self):
        deadline = time.time() + 2
        while self.server.bound_port is None and time.time() < deadline:
            time.sleep(0.01)
        self.assertIsNotNone(self.server.bound_port)


if __name__ == "__main__":
    unittest.main()
