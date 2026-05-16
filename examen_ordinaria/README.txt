SISTEMA CLIENTE-SERVIDOR TCP
============================

Descripcion general
-------------------

Este proyecto implementa un sistema cliente-servidor mediante sockets TCP en
Python.

El servidor escucha conexiones TCP, recibe un mensaje de texto codificado en
UTF-8, calcula la respuesta segun el protocolo indicado y responde por la misma
conexion. Tras responder, cierra la conexion con ese cliente y continua
aceptando nuevas conexiones.

El cliente pregunta al usuario la direccion completa del servidor, se conecta,
envia tres mensajes de prueba, imprime las respuestas recibidas por salida
estandar y termina.

Direccion por defecto
---------------------

Si no se indica otra configuracion en el codigo:

- host: 127.0.0.1
- puerto: 16063

Protocolo de mensajes
---------------------

Todos los mensajes se codifican en UTF-8.

Formato 1:

  c:Frase

El servidor responde con el numero de veces que aparece el caracter c en la
frase:

  c:numero

Ejemplo:

  m:combinaciones momentaneas de palabras

Respuesta:

  m:3

Formato 2:

  c1,c2,...,cm:Frase

El servidor responde con el numero de apariciones de cada caracter:

  c1:n1,c2:n2,...,cm:nm

Ejemplo:

  m,e,z:Combinaciones momentaneas de palabras

Respuesta:

  m:3,e:4,z:0

Cualquier otro mensaje produce:

  ERROR

Ejecucion
---------

Desde la carpeta examen_ordinaria:

  make server

En otra terminal:

  make client

El cliente preguntara:

  Direccion completa del servidor (host:puerto):

Para usar el servidor local por defecto, introducir:

  127.0.0.1:16063

Salida esperada del cliente:

  m:3
  m:3,e:4,z:0
  ERROR

Registro del servidor
---------------------

Cada vez que el servidor recibe una conexion, imprime en error estandar la IP
del cliente y el mensaje recibido.

Ejemplo:

  Cliente 127.0.0.1 envio: m:combinaciones momentaneas de palabras

Pruebas
-------

Las pruebas se ejecutan con:

  make test

Incluyen pruebas del protocolo, del servidor TCP, del cliente TCP y de la
integracion cliente-servidor.
