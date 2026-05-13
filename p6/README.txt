Practica 6 - Cliente-servidor TCP
=================================

Descripcion
-----------

Esta practica implementa un sistema cliente-servidor sencillo mediante sockets
TCP de Internet. El cliente solicita al servidor el contenido de un fichero y el
servidor responde con el contenido o con un mensaje de error si no puede leerlo.

La comunicacion se realiza con sockets PF_INET/AF_INET de tipo SOCK_STREAM, es
decir, TCP orientado a conexion.

Configuracion de red
--------------------

La direccion y el puerto estan definidos en los constructores de las clases:

- host: 127.0.0.1
- puerto: 16063

No se pasan host ni puerto por linea de comandos.

Ejecucion
---------

Para arrancar el servidor:

make server

El servidor permanece en ejecucion hasta que el usuario lo cierre manualmente,
por ejemplo con Ctrl+C.

Para ejecutar el cliente usando el fichero de ejemplo:

make client

Tambien puede indicarse otro fichero absoluto:

make client FILE=/ruta/absoluta/al/fichero.txt

El cliente imprime por terminal la respuesta recibida del servidor y termina.

Ejemplo de uso
--------------

En una terminal:

make server

En otra terminal:

make client

Si el fichero existe, se mostrara su contenido. Si el fichero no puede leerse,
se mostrara un mensaje que empieza por ERROR:.

Nombres de proceso
------------------

El programa usa la libreria setproctitle para que los procesos puedan
identificarse con ps:

- el servidor aparece como serv6,
- el cliente aparece como cli6.

Estructura principal
--------------------

- src/main.py: punto de entrada de cliente y servidor.
- src/client.py: clase FileClient.
- src/server.py: clase FileServer.
- src/config.py: constantes compartidas.
- tests/: pruebas unitarias e integracion.
