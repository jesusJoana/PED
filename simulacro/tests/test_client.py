import io
import socket
import threading
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src.client import ClienteTCP
from src.config import HOST_SERVIDOR, PUERTO_SERVIDOR


class ServidorPruebaTCP(threading.Thread):
    """Servidor TCP auxiliar para probar el cliente con sockets reales."""

    def __init__(self, host, puerto, respuestas):
        super().__init__(daemon=True)
        self.host = host
        self.puerto = puerto
        self.respuestas = respuestas
        self.mensajes_recibidos = []
        self.preparado = threading.Event()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((self.host, self.puerto))
            servidor.listen(1)
            self.preparado.set()

            conexion, _ = servidor.accept()
            with conexion:
                for respuesta in self.respuestas:
                    datos = conexion.recv(1024)
                    if not datos:
                        break
                    self.mensajes_recibidos.append(datos.decode("utf-8"))
                    conexion.sendall(respuesta.encode("utf-8"))


class TestClienteTCP(unittest.TestCase):
    """Pruebas unitarias de la Iteracion 2: Cliente."""

    def obtener_puerto_libre(self):
        """Reserva temporalmente un puerto libre para evitar choques en tests."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    def arrancar_servidor_prueba(self, respuestas):
        """Arranca un servidor auxiliar que devuelve respuestas prefijadas."""
        puerto = self.obtener_puerto_libre()
        servidor = ServidorPruebaTCP("127.0.0.1", puerto, respuestas)
        servidor.start()
        self.assertTrue(servidor.preparado.wait(timeout=2))
        return servidor, puerto

    # Iteracion 2 - Requisito: el cliente usa la direccion configurada.
    def test_cliente_usa_host_puerto_y_minimo_por_defecto(self):
        cliente = ClienteTCP()

        self.assertEqual(HOST_SERVIDOR, cliente.host)
        self.assertEqual(PUERTO_SERVIDOR, cliente.puerto)
        self.assertEqual(3, cliente.mensajes_minimos)

    # Iteracion 2 - Requisito: el cliente envia mensajes por TCP real.
    def test_cliente_envia_mensaje_y_recibe_respuesta(self):
        servidor, puerto = self.arrancar_servidor_prueba(["RESPUESTA_FECHA"])
        cliente = ClienteTCP(host="127.0.0.1", puerto=puerto)

        cliente.conectar()
        respuesta = cliente.enviar_mensaje("FECHA")
        cliente.cerrar()

        servidor.join(timeout=2)
        self.assertEqual("RESPUESTA_FECHA", respuesta)
        self.assertEqual(["FECHA"], servidor.mensajes_recibidos)
        self.assertFalse(servidor.is_alive())

    # Iteracion 2 - Requisito: el cliente imprime las respuestas recibidas.
    def test_cliente_imprime_respuesta_en_salida_estandar(self):
        servidor, puerto = self.arrancar_servidor_prueba(["RESPUESTA_HORA"])
        cliente = ClienteTCP(host="127.0.0.1", puerto=puerto)
        salida = io.StringIO()

        cliente.conectar()
        with redirect_stdout(salida):
            cliente.enviar_e_imprimir("HORA")
        cliente.cerrar()

        servidor.join(timeout=2)
        self.assertIn("RESPUESTA_HORA", salida.getvalue())

    # Iteracion 2 - Requisito: no puede salir antes del minimo de mensajes.
    def test_cliente_no_permite_salir_antes_del_minimo_configurado(self):
        cliente = ClienteTCP(mensajes_minimos=3)
        cliente.mensajes_enviados = 2

        self.assertFalse(cliente.puede_salir())

    # Iteracion 2 - Requisito: puede salir al alcanzar el minimo configurable.
    def test_cliente_permite_salir_al_alcanzar_el_minimo_configurado(self):
        cliente = ClienteTCP(mensajes_minimos=2)
        cliente.mensajes_enviados = 2

        self.assertTrue(cliente.puede_salir())

    # Iteracion 2 - Requisito: SALIR es local y no cuenta como mensaje enviado.
    def test_cliente_interactivo_no_cierra_antes_del_minimo_y_luego_sale(self):
        servidor, puerto = self.arrancar_servidor_prueba(["R1", "R2", "R3"])
        cliente = ClienteTCP(host="127.0.0.1", puerto=puerto, mensajes_minimos=3)
        entradas = iter(["SALIR", "FECHA", "HORA", "OTRO", "SALIR"])
        salida = io.StringIO()

        with patch("builtins.input", side_effect=lambda _: next(entradas)):
            with redirect_stdout(salida):
                cliente.ejecutar_interactivo()

        servidor.join(timeout=2)
        texto_salida = salida.getvalue()
        self.assertIn("No puedes salir", texto_salida)
        self.assertIn("R1", texto_salida)
        self.assertIn("R2", texto_salida)
        self.assertIn("R3", texto_salida)
        self.assertEqual(["FECHA", "HORA", "OTRO"], servidor.mensajes_recibidos)
        self.assertFalse(servidor.is_alive())


if __name__ == "__main__":
    unittest.main()
