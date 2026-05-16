Practica 4 - Sistema cliente-servidor UDS

Descripcion general
-------------------

Este proyecto implementa un sistema cliente-servidor sencillo en Python usando
sockets UDS de tipo SOCK_STREAM.

El cliente envia al servidor el path absoluto de un fichero. El servidor intenta
leer ese fichero y responde con su contenido. Si no puede leerlo, responde con
un mensaje de ERROR. El cliente muestra en su terminal la respuesta recibida.

El socket UDS se crea dentro del directorio /tmp. El servidor permanece en
ejecucion para atender a mas de un cliente.

Manual de usuario
-----------------

1. Abrir una terminal en la carpeta p4.

2. Arrancar el servidor:

   make server

3. En otra terminal, pedir un fichero con el cliente:

   make client

   Por defecto se solicitara el fichero de ejemplo fichero.txt.
   Tambien se puede indicar otro path absoluto:

   make client FILE=/ruta/absoluta/del/fichero

4. El cliente imprimira en pantalla el contenido del fichero o un mensaje de
   error si el servidor no puede proporcionarlo.

Ejemplos de uso
---------------

Arrancar el servidor:

   make server

Ejecutar el cliente con el fichero de ejemplo:

   make client

Ejecutar el cliente con otro fichero:

   echo "hola desde UDS" > /tmp/prueba_p4.txt
   make client FILE=/tmp/prueba_p4.txt

Comprobar procesos con ps:

   ps -ef | grep serv4
   ps -ef | grep cli4

Explicacion funcional
---------------------

El ejecutable serv4 lanza el servidor definido en src/main.py. El servidor crea
un socket UDS en /tmp, queda escuchando conexiones y atiende cada cliente de
forma secuencial.

El ejecutable cli4 lanza el cliente definido en src/main.py. El cliente conecta
al socket del servidor, envia el path absoluto terminado en salto de linea y lee
la respuesta hasta que el servidor cierra la conexion.

Tambien puede personalizarse la ruta del socket con la variable SOCKET:

   make server SOCKET=/tmp/otro_serv4.sock
   make client SOCKET=/tmp/otro_serv4.sock
