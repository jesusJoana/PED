README - ejercicio_extra
========================

Descripcion general
-------------------

Esta practica implementa un sistema cliente-servidor sencillo en Python usando
sockets Unix Domain Socket, de tipo STREAM.

El cliente envia al servidor el path completo de un fichero. El servidor intenta
leer ese fichero y responde con su contenido. Si no puede leerlo, responde con un
mensaje de error. El cliente muestra en su terminal la respuesta recibida.

El servidor no finaliza despues de atender a un cliente. Permanece en ejecucion
aceptando nuevas conexiones hasta que se detiene manualmente con Control + C.

Estructura principal
--------------------

- src/config.py: lee y valida la ruta configurable del socket UDS.
- src/server.py: contiene la clase FileServer.
- src/client.py: contiene la clase FileClient.
- src/main.py: punto de entrada para lanzar cliente o servidor.
- config.txt: fichero de configuracion con la ruta del socket.
- tests/: pruebas unitarias y de integracion con unittest.

Configuracion del socket UDS
----------------------------

La direccion del socket se configura en el fichero:

config.txt

Valor por defecto:

/tmp/ped_g6_serv4.sock

Para cambiar la direccion del socket no hay que modificar ni recompilar codigo.
Basta con editar config.txt y escribir otra ruta dentro de /tmp.

Ejemplo:

/tmp/otro_socket_grupo6.sock

Cliente y servidor deben usar la misma ruta, por eso ambos leen config.txt.

Ejecucion del servidor
----------------------

Desde la carpeta ejercicio_extra:

make server

El servidor crea el socket UDS configurado y queda esperando peticiones.

Para detener el servidor:

Control + C

Ejecucion del cliente
---------------------

Desde otra terminal, tambien en la carpeta ejercicio_extra:

make client FILE=/ruta/completa/fichero.txt

Ejemplo:

make client FILE=/tmp/prueba.txt

El cliente enviara el path completo al servidor y mostrara por pantalla la
respuesta recibida.

Nombres de proceso
------------------

La practica usa setproctitle para que los procesos contengan las cadenas pedidas
por el enunciado:

- Servidor: serv4_g6
- Cliente: cli4_g6

Se pueden comprobar con el comando ps mientras los procesos estan en ejecucion.

Pruebas
-------

Para ejecutar las pruebas:

make test

Las pruebas cubren:

- lectura de configuracion,
- validacion de socket en /tmp,
- respuesta del servidor ante ficheros existentes e inexistentes,
- envio del path completo desde el cliente,
- validacion de main.py,
- integracion real cliente-servidor con socket UDS STREAM,
- conexion de varios clientes consecutivos.
