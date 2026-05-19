Sistema cliente-servidor TCP para conteo de letras
==================================================

Descripcion general
-------------------

Este proyecto implementa un sistema cliente-servidor TCP en Python.

El cliente se conecta al servidor, envia mensajes de texto en UTF-8 y muestra
por pantalla la respuesta recibida. El servidor atiende conexiones TCP en el
puerto 16063 y responde contando cuantas veces aparecen las letras indicadas en
la frase recibida.

El sistema usa programacion orientada a objetos y esta preparado para ejecutarse
mediante make.


Protocolo de mensajes
---------------------

Formato de mensaje valido:

letra1,letra2,...:frase

Ejemplo:

p,a:me gusta ped

Respuesta:

p:1,a:1

Las letras se cuentan de forma exacta. Por tanto, a y A son caracteres
distintos.

Ejemplo:

a,A:aAaA

Respuesta:

a:2,A:2

Si el mensaje no cumple el formato esperado, el servidor responde:

ERROR


Manual de usuario
-----------------

1. Abrir una terminal en la carpeta del proyecto:

cd examen_ordinario

2. Arrancar el servidor:

make server

Tambien se puede usar:

make run-server

3. Abrir otra terminal en la misma carpeta y arrancar el cliente:

make client

Tambien se puede usar:

make run-client

4. El cliente pedira la direccion completa del servidor:

Direccion del servidor (host:puerto):

Para ejecutar en la misma maquina, escribir:

127.0.0.1:16063

5. Escribir mensajes para enviarlos al servidor:

p,a:me gusta ped
c:casa con coco
mensaje sin formato

El cliente mostrara respuestas similares a:

p:1,a:1
c:4
ERROR

6. Para cerrar el cliente, escribir:

SALIR

SALIR es una orden local del cliente. No se envia al servidor.


Ejemplos de uso
---------------

Mensaje:

p,a:me gusta ped

Respuesta:

p:1,a:1

Mensaje:

c,t,p:ccttpp

Respuesta:

c:2,t:2,p:2

Mensaje:

p,M:Me gusta ped

Respuesta:

p:1,M:1

Mensaje invalido:

hola mundo

Respuesta:

ERROR


Salida del servidor
-------------------

El servidor escribe en la salida de error estandar una linea por cada conexion
recibida. Esa linea contiene la IP del cliente y el mensaje recibido.

Ejemplo:

127.0.0.1 p,a:me gusta ped

Esta salida sirve como traza de diagnostico del servidor. La respuesta funcional
del protocolo se envia siempre al cliente por la conexion TCP.


Pruebas
-------

Para ejecutar las pruebas automatizadas:

make test

Las pruebas estan escritas con unittest y cubren servidor, cliente, integracion
cliente-servidor y documentacion.
