import socket

from src.config import (
    CODIFICACION,
    COMANDO_SALIDA,
    HOST_SERVIDOR,
    MIN_MENSAJES_CLIENTE,
    PUERTO_SERVIDOR,
    TAMANO_BUFFER,
)


class ClienteTCP:
    """Cliente TCP interactivo para comunicarse con el servidor."""

    def __init__(
        self,
        host=HOST_SERVIDOR,
        puerto=PUERTO_SERVIDOR,
        mensajes_minimos=MIN_MENSAJES_CLIENTE,
    ):
        self.host = host
        self.puerto = puerto
        self.mensajes_minimos = mensajes_minimos
        self.mensajes_enviados = 0
        self.socket_cliente = None

    def conectar(self):
        """Abre la conexion TCP con el servidor configurado."""
        self.socket_cliente = socket.create_connection((self.host, self.puerto), timeout=5)

    def cerrar(self):
        """Cierra la conexion del cliente si esta abierta."""
        if self.socket_cliente is not None:
            self.socket_cliente.close()
            self.socket_cliente = None

    def enviar_mensaje(self, mensaje):
        """Envia un mensaje al servidor y devuelve la respuesta recibida."""
        self.socket_cliente.sendall(mensaje.encode(CODIFICACION))
        respuesta = self.socket_cliente.recv(TAMANO_BUFFER).decode(CODIFICACION)
        self.mensajes_enviados += 1
        return respuesta

    def enviar_e_imprimir(self, mensaje):
        """Envia un mensaje e imprime la respuesta del servidor."""
        respuesta = self.enviar_mensaje(mensaje)
        print(respuesta)
        return respuesta

    def puede_salir(self):
        """Indica si el cliente ya puede finalizar segun el minimo configurado."""
        return self.mensajes_enviados >= self.mensajes_minimos

    def ejecutar_interactivo(self):
        """Ejecuta el cliente leyendo mensajes desde teclado."""
        self.conectar()
        try:
            while True:
                mensaje = input("> ")
                if mensaje == COMANDO_SALIDA:
                    if self.puede_salir():
                        print("Cliente desconectado correctamente.")
                        break
                    print(
                        "No puedes salir hasta enviar al menos "
                        f"{self.mensajes_minimos} mensajes. "
                        f"Has enviado {self.mensajes_enviados}."
                    )
                    continue

                self.enviar_e_imprimir(mensaje)
        except OSError as error:
            print(f"ERROR: {error}")
        finally:
            self.cerrar()
