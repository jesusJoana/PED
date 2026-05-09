# Plan de iteraciones - Practica 5

## Objetivo general

Construir un sistema cliente-servidor sencillo mediante sockets UDP de Internet
(`PF_INET`/`AF_INET`, `SOCK_DGRAM`).

El cliente pedira al servidor el contenido de un fichero. El servidor respondera
con el contenido del fichero o con un mensaje de error si no puede devolverlo.

## Decisiones tecnicas iniciales

- Se usara Python con programacion orientada a objetos.
- La ejecucion se hara mediante `make`.
- Las pruebas se haran con `unittest`.
- El cliente usara un socket UDP con `connect((host, port))`, aunque UDP siga
  siendo no orientado a conexion.
- El cliente enviara la ruta absoluta del fichero como peticion.
- El servidor respondera al cliente mediante UDP.
- Se asumiran ficheros pequenos, adecuados para una respuesta en un datagrama
  UDP. Esta limitacion se documentara en `README.txt`.
- El servidor permanecera activo hasta que se cierre manualmente.
- Para justificar mejor la atencion de mas de un cliente, el servidor delegara
  cada peticion recibida en un hilo.

## Estructura prevista

```text
p5/
  Makefile
  README.txt
  INSTALL.txt
  cli5
  serv5
  fichero.txt
  docs/
    plan_iteraciones.md
  src/
    __init__.py
    main.py
    config.py
    client.py
    server.py
  tests/
    __init__.py
    test_client.py
    test_server.py
    test_integracion.py
```

## Iteracion 1 - Test 1

Objetivo: comprobar el flujo basico extremo a extremo con sockets UDP reales.

Pruebas:

- Arrancar servidor real en un proceso.
- Crear un fichero temporal con contenido conocido.
- Ejecutar cliente real contra el servidor.
- Verificar que el cliente imprime por terminal el contenido del fichero.

Estado esperado de la entrega: RED.

Archivos previstos:

- `tests/test_integracion.py`

## Iteracion 2 - Test 1 OK

Objetivo: implementar el minimo codigo para que el cliente reciba el contenido
de un fichero existente.

Implementacion:

- `src/config.py`
- `src/client.py`
- `src/server.py`
- `src/main.py`

Estado esperado de la entrega: GREEN.

## Iteracion 3 - Test 2

Objetivo: comprobar la respuesta de error cuando el fichero no puede leerse.

Pruebas:

- Cliente solicita un fichero inexistente.
- Servidor responde con un mensaje que empieza por `ERROR:`.
- Cliente imprime ese error por terminal.

Estado esperado de la entrega: RED.

Archivos previstos:

- `tests/test_integracion.py`
- posible prueba unitaria en `tests/test_server.py`

## Iteracion 4 - Test 2 OK

Objetivo: implementar el manejo de errores de lectura.

Implementacion:

- Capturar `OSError` al leer el fichero.
- Devolver una respuesta textual de error.

Estado esperado de la entrega: GREEN.

## Iteracion 5 - Test 3

Objetivo: comprobar que el servidor atiende mas de un cliente y no se cierra
tras responder.

Pruebas:

- Arrancar servidor real en un proceso.
- Ejecutar varios clientes contra el mismo servidor.
- Verificar que todos reciben respuesta.
- Verificar que el proceso servidor sigue vivo.

Estado esperado de la entrega: RED.

Archivos previstos:

- `tests/test_integracion.py`

## Iteracion 6 - Test 3 OK

Objetivo: hacer persistente el servidor y permitir atencion concurrente.

Implementacion:

- Bucle permanente con `recvfrom`.
- Hilo por peticion recibida.
- Respuesta enviada al origen de cada datagrama.

Estado esperado de la entrega: GREEN.

## Iteracion 7 - Test 4

Objetivo: comprobar que los procesos aparecen como `cli5` y `serv5` en `ps`.

Pruebas:

- Verificar que existen `cli5` y `serv5`.
- Lanzar servidor mediante `serv5`.
- Lanzar cliente mediante `cli5`.
- Comprobar con `ps` que los argumentos del proceso contienen las cadenas
  `serv5` y `cli5`.

Estado esperado de la entrega: RED.

Archivos previstos:

- `tests/test_integracion.py`

## Iteracion 8 - Test 4 OK

Objetivo: crear los wrappers ejecutables.

Implementacion:

- `serv5` ejecutara `src/main.py server`.
- `cli5` ejecutara `src/main.py client`.
- Ambos deberan tener permisos de ejecucion.

Estado esperado de la entrega: GREEN.

## Iteracion 9 - Test 5

Objetivo: comprobar que existe la documentacion final obligatoria.

Pruebas:

- Verificar existencia de `README.txt`.
- Verificar existencia de `INSTALL.txt`.
- Comprobar que documentan uso basico, instalacion, ejecucion, pruebas y
  limitacion de tamano por UDP.

Estado esperado de la entrega: RED.

Archivos previstos:

- `tests/test_integracion.py`

## Iteracion 10 - Test 5 OK

Objetivo: generar la documentacion final de la practica.

Implementacion:

- `README.txt`
- `INSTALL.txt`

Estado esperado de la entrega: GREEN.

## Refactorizaciones previstas

Se realizaran solo cuando todos los tests esten en verde.

Posibles mejoras:

- Extraer constantes compartidas.
- Mejorar nombres de clases y metodos.
- Eliminar duplicidades en tests.
- Simplificar la gestion de procesos de prueba.

En una entrega de refactor no se modificaran tests ni se anadira funcionalidad.
