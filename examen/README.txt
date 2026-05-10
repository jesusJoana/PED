README - Servidor y cliente UDP
================================

Descripcion general
-------------------

Este proyecto implementa una aplicacion cliente-servidor mediante UDP.

El servidor escucha mensajes de texto codificados en UTF-8, procesa el protocolo
pedido en el enunciado y devuelve una respuesta UDP al cliente.

El cliente pregunta al usuario la direccion completa del servidor, envia una
secuencia minima de tres mensajes, imprime las respuestas recibidas por salida
standard y termina.

Puerto elegido
--------------

El servidor escucha por defecto en:

Host: 127.0.0.1
Puerto: 16063

Protocolo
---------

Mensajes validos de cliente a servidor:

1. BUSCAR <cadena>

   Busca la cadena como subcadena en los ficheros:

   - /etc/passwd
   - /etc/services

   La busqueda distingue mayusculas y minusculas.

   Respuesta con resultados:

   RESULTADO <numero de lineas>
   <lineas completas encontradas>

   Respuesta sin resultados:

   RESULTADO 0

2. NUMERO

   Devuelve el numero de busquedas ejecutadas por el servidor.

   Ejemplo:

   OK 2

3. SALIR

   Solicita al servidor que termine.

   Respuesta:

   OK

Cualquier otro mensaje o formato incorrecto devuelve:

ERROR

Ejecucion
---------

Preparar el entorno:

make install

Ejecutar el servidor:

make run-server

En otra terminal, ejecutar el cliente:

make run-client

El cliente pedira una direccion con formato:

127.0.0.1:16063

Mensajes que envia el cliente
-----------------------------

El cliente envia por defecto:

BUSCAR root
NUMERO
SALIR

Tras recibir la respuesta de SALIR, el cliente termina y el servidor tambien
finaliza su ejecucion.

Pruebas automaticas
-------------------

Para ejecutar las pruebas unitarias:

make test

El proyecto incluye pruebas del servidor, del cliente, del cliente interactivo y
de las trazas del servidor por error standard.
