# Plan de iteraciones - examen2

## Contexto de trabajo

Este proyecto se desarrollará en la carpeta `examen2` siguiendo el contrato de
trabajo definido en `CONTRATOS/contrato_PED.md`.

El usuario ha indicado expresamente en este chat una modificación del esquema
general de iteraciones del contrato. Para este proyecto, el flujo será:

1. Iteración 1 - Servidor.
2. Iteración 2 - Cliente.
3. Iteración 3 - Integración cliente-servidor.
4. Iteración 4 - Servidor modificado.
5. Iteración 5 - Cliente modificado.
6. Iteración 6 - README.

Cada iteración con desarrollo de código tendrá entregas separadas:

- `Test n <ámbito>`: pruebas en rojo.
- `Test n <ámbito> OK`: implementación mínima en verde.
- `Refactor n <ámbito>`: refactorización posterior y separada, solo si aporta valor.

La refactorización no formará parte de la entrega `Test n <ámbito> OK`.

## Requisitos específicos del sistema

Se debe implementar un sistema cliente-servidor UDP para pedir información sobre
frases o cadenas contenidas en ficheros conocidos por el servidor.

El servidor:

- Atenderá por UDP en el puerto definido por el contrato.
- Usará por defecto:
  - host: `127.0.0.1`
  - puerto: `16063`
- Se ejecutará de forma continua.
- Aceptará peticiones UDP de cualquier cliente.
- Consultará los ficheros `/etc/passwd` y `/etc/services`.
- Codificará y decodificará todos los mensajes en UTF-8.

El cliente:

- Enviará peticiones UDP al servidor.
- Esperará respuestas UDP del servidor.
- Imprimirá las respuestas en salida estándar.
- Podrá terminar tras recibir e imprimir la respuesta o respuestas previstas.

## Protocolo de mensajes

### `BUSCAR <cadena>`

El servidor buscará las líneas de `/etc/passwd` y `/etc/services` en las que
aparezca `<cadena>` como subcadena, de forma equivalente a `grep`.

La búsqueda será sensible a mayúsculas y minúsculas.

La respuesta tendrá este formato:

```text
RESULTADO n
linea_encontrada_1
linea_encontrada_2
...
```

Si no hay resultados:

```text
RESULTADO 0
```

La cadena buscada podrá contener espacios. Por ejemplo:

```text
BUSCAR a ver que encuentro
```

### `NUMERO`

El servidor devolverá el número de búsquedas `BUSCAR` ejecutadas correctamente.

Ejemplo:

```text
OK 2
```

### `SALIR`

El servidor responderá:

```text
OK
```

Después deberá terminar su ejecución.

### Mensajes inválidos

Cualquier otro mensaje, o cualquier mensaje válido mal escrito o mal formateado,
generará la respuesta:

```text
ERROR
```

## Criterios de separación de pruebas

Las pruebas de servidor irán en `tests/test_server.py` cuando validen
responsabilidades propias del servidor, aunque usen UDP real.

Las pruebas de cliente irán en `tests/test_client.py` cuando validen
responsabilidades propias del cliente usando un servidor UDP ligero de prueba.

Las pruebas de integración irán en `tests/test_integracion.py` cuando validen la
colaboración extremo a extremo entre cliente real y servidor real.

## Estructura prevista

```text
examen2/
  src/
    main.py
    protocol.py
    server.py
    client.py
  tests/
    test_server.py
    test_client.py
    test_integracion.py
  docs/
    plan_iteraciones.md
  README.txt
  INSTALL.txt
  Makefile
```

## Iteración 1 - Servidor

### Objetivo

Implementar el servidor UDP continuo capaz de recibir mensajes del protocolo y
generar las respuestas adecuadas.

### Entregas

- `Test 1 Servidor`: pruebas del servidor en rojo.
- `Test 1 Servidor OK`: implementación mínima para dejar en verde las pruebas.
- `Refactor 1 Servidor`: refactorización posterior y separada, si aporta valor.

### Pruebas previstas

- `BUSCAR <cadena>` devuelve `RESULTADO n` y las líneas completas encontradas.
- La búsqueda distingue mayúsculas y minúsculas.
- `BUSCAR` sin cadena devuelve `ERROR`.
- `NUMERO` devuelve `OK n`.
- `SALIR` devuelve `OK` y permite detener el servidor.
- Un mensaje desconocido devuelve `ERROR`.
- El servidor responde por UDP real a peticiones enviadas desde el test.

### Archivos afectados

- `src/protocol.py`
- `src/server.py`
- `src/main.py`
- `tests/test_server.py`

## Iteración 2 - Cliente

### Objetivo

Implementar el cliente UDP para que se conecte automáticamente a la dirección
del servidor definida en el contrato, envíe al menos tres mensajes, imprima las
respuestas en salida estándar y termine tras el último mensaje.

### Entregas

- `Test 2 Cliente`: pruebas del cliente en rojo.
- `Test 2 Cliente OK`: implementación mínima para dejar en verde las pruebas.
- `Refactor 2 Cliente`: refactorización posterior y separada, si aporta valor.

### Pruebas previstas

- El cliente usa automáticamente host y puerto por defecto.
- El cliente envía al menos tres mensajes UDP.
- El cliente imprime en salida estándar cada respuesta recibida.
- El cliente termina tras el último mensaje.
- Ante timeout o error de comunicación, el cliente imprime una condición de error
  y termina sin bloquear.

### Archivos afectados

- `src/client.py`
- `src/main.py`
- `tests/test_client.py`

## Iteración 3 - Integración cliente-servidor

### Objetivo

Validar la colaboración extremo a extremo entre el cliente real y el servidor
real usando UDP.

### Entregas

- `Test 3 Integración`: pruebas de integración en rojo.
- `Test 3 Integración OK`: implementación mínima para dejar en verde las pruebas
  de integración y todos los tests acumulados.
- `Refactor 3 Integración`: refactorización posterior y separada, si aporta valor.

### Pruebas previstas

- El servidor real se levanta en un hilo de prueba con UDP real.
- El cliente real envía mensajes al servidor real.
- El cliente imprime en salida estándar las respuestas reales del servidor.
- El flujo incluye al menos `NUMERO`, `BUSCAR <cadena>` y `SALIR`.
- El servidor termina correctamente al recibir `SALIR`.
- Los tests unitarios acumulados siguen pasando.

### Archivos afectados

- `tests/test_integracion.py`
- `src/client.py`, solo si fuera necesario ajustar comportamiento observado.
- `src/server.py`, solo si fuera necesario ajustar comportamiento observado.

## Iteración 4 - Servidor modificado

### Objetivo

Modificar el servidor para que imprima por error estándar una línea cada vez que
reciba una petición UDP de un cliente.

La línea deberá incluir:

- dirección IP del cliente;
- mensaje recibido.

### Entregas

- `Test 4 Servidor`: pruebas del servidor modificado en rojo.
- `Test 4 Servidor OK`: implementación mínima para dejar en verde las pruebas.
- `Refactor 4 Servidor`: refactorización posterior y separada, si aporta valor.

### Pruebas previstas

- Por cada datagrama recibido, el servidor escribe una línea en error estándar.
- La línea contiene la IP del cliente.
- La línea contiene el mensaje recibido.
- Las respuestas del protocolo se mantienen correctas.
- Los tests acumulados siguen pasando.

### Archivos afectados

- `src/server.py`
- `tests/test_server.py`
- `tests/test_integracion.py`, si se valida con servidor real.

## Iteración 5 - Cliente modificado

### Objetivo

Modificar el cliente para que pregunte al usuario por la dirección completa del
servidor y muestre un error si no consigue comunicarse con él.

La dirección completa se interpretará como:

```text
host:puerto
```

### Entregas

- `Test 5 Cliente`: pruebas del cliente modificado en rojo.
- `Test 5 Cliente OK`: implementación mínima para dejar en verde las pruebas.
- `Refactor 5 Cliente`: refactorización posterior y separada, si aporta valor.

### Pruebas previstas

- El cliente solicita al usuario la dirección completa del servidor.
- El cliente acepta una dirección en formato `host:puerto`.
- El cliente envía sus mensajes al destino indicado por el usuario.
- Si no recibe respuesta o se produce un error, imprime un mensaje de error y
  termina correctamente.
- Los tests acumulados siguen pasando.

### Archivos afectados

- `src/client.py`
- `src/main.py`
- `tests/test_client.py`
- `tests/test_integracion.py`, si se valida con servidor real.

## Iteración 6 - README

### Objetivo

Crear la documentación final del proyecto según el contrato.

No se aplicará TDD en esta iteración.

### Entregas

- Documentación final.

### Archivos afectados

- `README.txt`
- `INSTALL.txt`

### Contenido previsto

`README.txt` incluirá:

- descripción general del proyecto;
- manual de usuario;
- instrucciones básicas de ejecución;
- ejemplos de uso;
- explicación funcional del sistema.

`INSTALL.txt` incluirá:

- instrucciones completas de instalación;
- dependencias necesarias;
- preparación del entorno;
- comandos de ejecución;
- pasos necesarios para poner el sistema en funcionamiento.
