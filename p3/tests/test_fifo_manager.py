import stat
import tempfile
import unittest
from pathlib import Path

from src.main import FifoManager


class FifoManagerTest(unittest.TestCase):
    """Pruebas del gestor de tuberias FIFO."""

    def test_create_request_and_response_fifos(self):
        """Comprueba que se crean las dos tuberias necesarias."""
        with tempfile.TemporaryDirectory() as temp_dir:
            request_fifo = Path(temp_dir) / "cliente_servidor.fifo"
            response_fifo = Path(temp_dir) / "servidor_cliente.fifo"
            manager = FifoManager(request_fifo, response_fifo)

            manager.setup()

            self.assertTrue(request_fifo.exists())
            self.assertTrue(response_fifo.exists())

    def test_create_existing_fifos_without_error(self):
        """Comprueba que crear FIFO existentes no provoca errores."""
        with tempfile.TemporaryDirectory() as temp_dir:
            request_fifo = Path(temp_dir) / "cliente_servidor.fifo"
            response_fifo = Path(temp_dir) / "servidor_cliente.fifo"
            manager = FifoManager(request_fifo, response_fifo)

            manager.setup()
            manager.setup()

            self.assertTrue(request_fifo.exists())
            self.assertTrue(response_fifo.exists())

    def test_created_paths_are_unix_fifos(self):
        """Comprueba que las rutas creadas son tuberias FIFO de UNIX."""
        with tempfile.TemporaryDirectory() as temp_dir:
            request_fifo = Path(temp_dir) / "cliente_servidor.fifo"
            response_fifo = Path(temp_dir) / "servidor_cliente.fifo"
            manager = FifoManager(request_fifo, response_fifo)

            manager.setup()

            self.assertTrue(stat.S_ISFIFO(request_fifo.stat().st_mode))
            self.assertTrue(stat.S_ISFIFO(response_fifo.stat().st_mode))


if __name__ == "__main__":
    unittest.main()
