from pathlib import Path
import unittest


class TestDocumentacionIteracion6(unittest.TestCase):
    """
    Iteracion 6 - Documentacion.

    Estas pruebas validan que existen los documentos finales obligatorios y que
    contienen instrucciones basicas de uso, instalacion y stderr.
    """

    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    def _leer_documento(self, nombre):
        ruta = self.PROJECT_ROOT / nombre
        self.assertTrue(ruta.exists(), f"Debe existir {nombre}")
        return ruta.read_text(encoding="utf-8")

    def test_readme_contiene_manual_y_ejemplos_de_uso(self):
        """
        Iteracion 6.
        Requisito: README.txt describe el proyecto, su uso y ejemplos.
        """
        contenido = self._leer_documento("README.txt")

        self.assertIn("cliente-servidor TCP", contenido)
        self.assertIn("make server", contenido)
        self.assertIn("make client", contenido)
        self.assertIn("p,a:me gusta ped", contenido)
        self.assertIn("SALIR", contenido)

    def test_install_contiene_instalacion_y_stderr(self):
        """
        Iteracion 6.
        Requisito: INSTALL.txt explica instalacion, ejecucion y redireccion de
        stderr.
        """
        contenido = self._leer_documento("INSTALL.txt")

        self.assertIn("make install", contenido)
        self.assertIn("make test", contenido)
        self.assertIn("stderr", contenido)
        self.assertIn("2>", contenido)
        self.assertIn("make server 2> servidor.log", contenido)
