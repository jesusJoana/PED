README - examen2
================

Descripcion general
-------------------

Este proyecto implementa un sistema cliente-servidor UDP en Python.

El servidor escucha peticiones UDP y permite consultar informacion sobre las
lineas contenidas en los ficheros:

- /etc/passwd
- /etc/services

El cliente envia mensajes al servidor, espera las respuestas por UDP, imprime
las respuestas en salida estandar y termina tras completar sus mensajes.

Direccion por defecto
---------------------

El servidor usa por defecto:

- Host: 127.0.0.1
- Puerto: 16063

El cliente pregunta al usuario la direccion completa del servidor en formato:

host:puerto

Por ejemplo:

127.0.0.1:16063

Protocolo de mensajes
---------------------

Todos los mensajes se codifican en UTF-8.

Mensajes validos de cliente a servidor:

BUSCAR <cadena>

Busca la cadena indicada en /etc/passwd y /etc/services. La busqueda distingue
mayusculas y minusculas. La cadena puede contener espacios.

Respuesta con resultados:

RESULTADO n
linea_1
linea_2

Respuesta sin resultados:

RESULTADO 0

NUMERO

Devuelve el numero de busquedas BUSCAR ejecutadas correctamente.

Ejemplo:

OK 2

SALIR

Indica al servidor que debe terminar su ejecucion.

Respuesta:

OK

Mensajes invalidos
------------------

Cualquier mensaje desconocido, mal escrito o mal formateado produce:

ERROR

Ejemplos de mensajes validos
----------------------------

BUSCAR root
BUSCAR a ver que encuentro
NUMERO
SALIR

Uso del servidor
----------------

Para arrancar el servidor:

make server

El servidor queda escuchando por UDP hasta recibir el mensaje SALIR.

Cada vez que recibe una peticion, escribe en error estandar una linea con la IP
del cliente y el mensaje recibido.

Ejemplo:

127.0.0.1 BUSCAR root

Uso del cliente
---------------

Para ejecutar el cliente:

make client

El cliente pedira la direccion completa del servidor. Introducir, por ejemplo:

127.0.0.1:16063

Despues enviara automaticamente los mensajes definidos por defecto:

NUMERO
BUSCAR root
SALIR

Imprimira en salida estandar las respuestas recibidas del servidor.

Ejemplo de salida:

OK 0
RESULTADO 1
root:x:0:0:root:/root:/bin/bash
OK

Pruebas automatizadas
---------------------

Para ejecutar todos los tests:

make test

Las pruebas estan separadas en:

- tests/test_server.py: pruebas del servidor.
- tests/test_client.py: pruebas del cliente.
- tests/test_integracion.py: pruebas de integracion cliente-servidor.

Notas funcionales
-----------------

- El servidor usa sockets UDP.
- El servidor puede aceptar peticiones UDP de cualquier cliente.
- El servidor se ejecuta de forma continua hasta recibir SALIR.
- El cliente termina tras imprimir las respuestas recibidas.
- Si el cliente no consigue comunicarse con el servidor, imprime ERROR.
- Si el usuario introduce una direccion de servidor con formato incorrecto, el
  cliente imprime ERROR.

