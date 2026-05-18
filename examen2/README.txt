README - EXAMEN2
================

Descripcion general
-------------------

Este proyecto implementa un sistema cliente-servidor UDP en Python.

El servidor escucha peticiones UDP y responde informacion sobre las lineas de
los ficheros:

- /etc/passwd
- /etc/services

El cliente permite introducir la direccion completa del servidor y enviar una
peticion del protocolo.

Valores por defecto:

- Host: 127.0.0.1
- Puerto: 16063


Protocolo de mensajes
---------------------

Todos los mensajes se codifican en UTF-8.

Mensajes aceptados por el servidor:

- BUSCAR <cadena>
- NUMERO
- SALIR

BUSCAR <cadena>
    Busca la cadena indicada en /etc/passwd y /etc/services.
    La respuesta contiene el numero de lineas encontradas, un salto de linea y
    las lineas completas encontradas.

NUMERO
    Devuelve OK y el numero de busquedas ejecutadas por el servidor.

SALIR
    Devuelve OK y termina la ejecucion del servidor.

Cualquier otro mensaje
    Devuelve ERROR.


Ejecucion del servidor
----------------------

Desde la carpeta examen2:

    make server

El servidor queda escuchando en UDP 127.0.0.1:16063 hasta recibir SALIR.


Ejecucion del cliente
---------------------

Desde otra terminal, en la carpeta examen2:

    make client

El cliente pregunta:

    Direccion del servidor (host:puerto):
    Peticion:

Ejemplo para buscar una cadena:

    127.0.0.1:16063
    BUSCAR ssh

Ejemplo para consultar el numero de busquedas:

    127.0.0.1:16063
    NUMERO

Ejemplo para cerrar el servidor:

    127.0.0.1:16063
    SALIR


Ejemplo completo de uso
-----------------------

Terminal 1:

    cd /home/jjoana/ejerciciosPED/PED/examen2
    make server

Terminal 2:

    cd /home/jjoana/ejerciciosPED/PED/examen2
    make client

Entrada de ejemplo:

    127.0.0.1:16063
    BUSCAR root


Comprobacion de stderr del servidor
-----------------------------------

En la iteracion 4 se implemento que el servidor escriba por la salida estandar
de error una linea cada vez que recibe un mensaje de un cliente. La linea
contiene la IP del cliente y el mensaje recibido.

Para comprobarlo separando stdout y stderr:

    cd /home/jjoana/ejerciciosPED/PED/examen2
    make server > /tmp/server_stdout.txt 2> /tmp/server_stderr.txt &
    make client

En el cliente se puede introducir, por ejemplo:

    127.0.0.1:16063
    NUMERO

Despues se comprueba el fichero de error estandar del servidor:

    cat /tmp/server_stderr.txt

Debe observarse una linea similar a:

    127.0.0.1 NUMERO

El fichero /tmp/server_stdout.txt no debe contener esas lineas, porque el
registro pedido por la iteracion 4 se escribe en stderr.


Ejecucion de pruebas
--------------------

Para ejecutar toda la bateria de pruebas:

    make test

Las pruebas estan separadas en:

- tests/test_server.py
- tests/test_client.py
- tests/test_integracion.py


Notas de funcionamiento
-----------------------

- El servidor usa sockets UDP reales.
- El cliente imprime por stdout las respuestas recibidas.
- Si el cliente no recibe respuesta, imprime ERROR.
- En UDP no existe una conexion persistente como en TCP; cada datagrama recibido
  se registra como mensaje recibido de un cliente.
