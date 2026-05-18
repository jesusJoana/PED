import socket
from datetime import datetime

from src.config import CODIFICACION, HOST_SERVIDOR, PUERTO_SERVIDOR, TAMANO_BUFFER


class ServidorTCP:
    """Servidor TCP que responde a los mensajes definidos en el protocolo."""

    def __init__(self, host=HOST_SERVIDOR, puerto=PUERTO_SERVIDOR):
        self.host = host
        self.puerto = puerto

    def procesar_mensaje(self, mensaje):
        """Genera la respuesta del servidor segun el mensaje recibido."""
        if mensaje == "FECHA":
            return datetime.now().strftime("%Y-%m-%d")
        if mensaje == "HORA":
            return datetime.now().strftime("%H:%M:%S")
        return "ERROR"

    def iniciar(self, max_conexiones=None):
        """Inicia el servidor; en ejecucion normal queda atendiendo siempre."""
        conexiones_atendidas = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((self.host, self.puerto))
            servidor.listen()

            while max_conexiones is None or conexiones_atendidas < max_conexiones:
                conexion, _ = servidor.accept()
                with conexion:
                    datos = conexion.recv(TAMANO_BUFFER)
                    mensaje = datos.decode(CODIFICACION)
                    respuesta = self.procesar_mensaje(mensaje)
                    conexion.sendall(respuesta.encode(CODIFICACION))
                conexiones_atendidas += 1
