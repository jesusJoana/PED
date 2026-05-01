# Pruebas iniciales para asegurar que la estructura del proyecto funciona.

import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src import main


class MainModuleTest(unittest.TestCase):
    def test_main_function_exists(self):
        # El proyecto debe exponer una funcion main como punto de entrada.
        self.assertTrue(callable(main.main))

    def test_validate_args_accepts_one_file_path(self):
        # La ejecucion correcta recibe exactamente una ruta de fichero.
        self.assertEqual(main.validate_args(["datos.txt"]), "datos.txt")

    def test_validate_args_rejects_missing_file_path(self):
        # Sin ruta de fichero no sabemos que debe pedir el cliente.
        with self.assertRaisesRegex(ValueError, "Uso"):
            main.validate_args([])

    def test_validate_args_rejects_too_many_arguments(self):
        # El programa solo acepta un fichero por ejecucion.
        with self.assertRaisesRegex(ValueError, "Uso"):
            main.validate_args(["uno.txt", "dos.txt"])

    def test_set_process_name_uses_setproctitle(self):
        # El nombre del proceso se cambia usando la libreria setproctitle.
        with mock.patch.object(main, "setproctitle") as fake_setproctitle:
            main.set_process_name("cli2")

        fake_setproctitle.assert_called_once_with("cli2")

    def test_process_names_are_cli2_and_serv2(self):
        # Dejamos los nombres en constantes para no escribirlos a mano varias veces.
        self.assertEqual(main.CLIENT_PROCESS_NAME, "cli2")
        self.assertEqual(main.SERVER_PROCESS_NAME, "serv2")

    def test_sleep_if_requested_uses_environment_value(self):
        # La pausa opcional permite comprobar los procesos con ps.
        with mock.patch.dict(os.environ, {main.PROCESS_SLEEP_ENV: "1.5"}):
            with mock.patch.object(main.time, "sleep") as fake_sleep:
                main.sleep_if_requested()

        fake_sleep.assert_called_once_with(1.5)

    def test_main_returns_error_when_arguments_are_invalid(self):
        # main convierte los errores de uso en codigo de salida fallido.
        error_output = io.StringIO()

        with contextlib.redirect_stderr(error_output):
            exit_code = main.main([])

        self.assertEqual(exit_code, 1)
        self.assertIn("Uso:", error_output.getvalue())

    def test_main_returns_success_when_arguments_are_valid(self):
        # Con argumentos validos, main debe terminar correctamente.
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = main.main(["datos.txt"])

        self.assertEqual(exit_code, 0)

    def test_read_requested_file_returns_file_content(self):
        # El servidor debe poder preparar como respuesta el contenido pedido.
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "datos.txt"
            file_path.write_text("linea 1\nlinea 2\n", encoding="utf-8")

            self.assertEqual(
                main.read_requested_file(str(file_path)),
                "linea 1\nlinea 2\n",
            )

    def test_read_requested_file_reports_missing_file(self):
        # Si la ruta no existe, el servidor responde con un error legible.
        response = main.read_requested_file("no_existe.txt")

        self.assertIn("ERROR:", response)
        self.assertIn("no existe", response)

    def test_read_requested_file_reports_directory_path(self):
        # Una carpeta no es una peticion valida de fichero de texto.
        with tempfile.TemporaryDirectory() as tmpdir:
            response = main.read_requested_file(tmpdir)

        self.assertIn("ERROR:", response)
        self.assertIn("no es un fichero", response)

    def test_pipe_message_can_be_written_and_read(self):
        # Un mensaje escrito en un pipe debe leerse igual desde el otro extremo.
        read_fd, write_fd = os.pipe()

        try:
            main.write_message(write_fd, "peticion.txt")
            os.close(write_fd)
            write_fd = None

            self.assertEqual(main.read_message(read_fd), "peticion.txt")
        finally:
            if write_fd is not None:
                os.close(write_fd)
            os.close(read_fd)

    def test_pipe_empty_message_can_be_written_and_read(self):
        # El mensaje vacio tambien debe cerrar bien el flujo sin bloquear.
        read_fd, write_fd = os.pipe()

        try:
            main.write_message(write_fd, "")
            os.close(write_fd)
            write_fd = None

            self.assertEqual(main.read_message(read_fd), "")
        finally:
            if write_fd is not None:
                os.close(write_fd)
            os.close(read_fd)

    def test_pipe_large_message_can_be_read_in_chunks(self):
        # Leemos por bloques para soportar respuestas mas grandes que un fragmento.
        read_fd, write_fd = os.pipe()
        message = "contenido\n" * 2000

        try:
            main.write_message(write_fd, message)
            os.close(write_fd)
            write_fd = None

            self.assertEqual(main.read_message(read_fd), message)
        finally:
            if write_fd is not None:
                os.close(write_fd)
            os.close(read_fd)

    def test_program_prints_requested_file_content(self):
        # Ejecutamos el script completo para comprobar lectura real con fork y pipes.
        program = Path(__file__).resolve().parents[1] / "src" / "main.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "peticion.txt"
            file_path.write_text("contenido real\nsegunda linea\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(program), str(file_path)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "contenido real\nsegunda linea\n")
        self.assertEqual(result.stderr, "")

    def test_program_prints_error_when_requested_file_does_not_exist(self):
        # Si el fichero no existe, el error tambien debe llegar al hijo.
        program = Path(__file__).resolve().parents[1] / "src" / "main.py"

        result = subprocess.run(
            [sys.executable, str(program), "no_existe.txt"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("ERROR:", result.stdout)
        self.assertIn("no existe", result.stdout)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
