README
======

Descripcion general
-------------------

Este proyecto implementa un sistema cliente-servidor TCP en Python.

El servidor escucha conexiones TCP en la direccion 127.0.0.1 y en el puerto
16063. El cliente se conecta automaticamente a esa direccion y permite escribir
mensajes de forma interactiva desde teclado.

Todo el intercambio de mensajes se realiza usando codificacion UTF-8.


Protocolo de mensajes
---------------------

El servidor responde a los siguientes mensajes:

FECHA
    Devuelve la fecha actual del sistema en formato AAAA-MM-DD.

HORA
    Devuelve la hora actual del sistema en formato HH:MM:SS.

Cualquier otro mensaje
    Devuelve ERROR.


Cliente interactivo
-------------------

El cliente queda abierto esperando mensajes escritos por el usuario.

El comando local para cerrar el cliente es:

SALIR

Este comando no se envia al servidor y no cuenta como mensaje enviado.

El cliente no permite cerrarse hasta haber enviado al menos 3 mensajes reales al
servidor. Este minimo esta definido en src/config.py mediante la constante:

MIN_MENSAJES_CLIENTE = 3


Ejecucion del servidor
----------------------

Desde la carpeta del proyecto:

cd ~/ejerciciosPED/PED/simulacro

Lanzar el servidor:

make server

Tambien se puede usar:

make run-server

El servidor queda ejecutandose de forma continua. Para detenerlo manualmente se
puede usar Ctrl+C.


Ejecucion del cliente
---------------------

En otra terminal, desde la carpeta del proyecto:

cd ~/ejerciciosPED/PED/simulacro

Lanzar el cliente:

make client

Tambien se puede usar:

make run-client


Ejemplo de uso
--------------

Terminal 1:

make server

Terminal 2:

make client

Ejemplo de sesion del cliente:

> FECHA
2026-05-18
> HORA
17:45:00
> hola
ERROR
> SALIR
Cliente desconectado correctamente.

Si se intenta salir antes de enviar 3 mensajes:

> SALIR
No puedes salir hasta enviar al menos 3 mensajes. Has enviado 0.


Ejecucion de pruebas
--------------------

Para ejecutar todos los tests:

make test

Las pruebas estan organizadas en:

tests/test_server.py
    Pruebas unitarias del servidor.

tests/test_client.py
    Pruebas unitarias del cliente.

tests/test_integracion.py
    Pruebas de integracion cliente-servidor con sockets TCP reales.


Estructura principal
--------------------

main.py
    Punto de entrada de la aplicacion.

src/config.py
    Constantes de configuracion.

src/server.py
    Clase ServidorTCP.

src/client.py
    Clase ClienteTCP.

tests/
    Pruebas automatizadas con unittest.

docs/iteraciones.md
    Plan de iteraciones seguido durante el desarrollo.
