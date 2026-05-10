# Plan de iteraciones y entregas

## Contexto

El proyecto se desarrollara en la carpeta `examen` siguiendo el contrato PED.

La aplicacion sera cliente-servidor mediante UDP, implementada en Python con
programacion orientada a objetos. Las pruebas se escribiran con `unittest` y la
ejecucion se realizara mediante `make`.

Valores por defecto:

- Host del servidor: `127.0.0.1`
- Puerto del servidor: `16063`
- Codificacion de mensajes: UTF-8

Mensajes validos del protocolo:

- `BUSCAR <cadena>`: busca la cadena como subcadena, diferenciando mayusculas y
  minusculas, en `/etc/passwd` y `/etc/services`.
- `NUMERO`: devuelve el numero de busquedas ejecutadas.
- `SALIR`: solicita al servidor que termine.

Cualquier otro mensaje o formato incorrecto debera responder `ERROR`.

## Estructura prevista

```text
examen/
  src/
    main.py
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

## Iteracion 1: Servidor

### Objetivo

Implementar el servidor UDP. El servidor debera ejecutarse de forma continua,
recibir mensajes de cualquier cliente y responder segun el protocolo.

### Entrega Test 1

Estado esperado: RED.

Pruebas unitarias previstas en `tests/test_server.py`:

- Validar que `BUSCAR <cadena>` devuelve `RESULTADO <n>` y las lineas completas
  encontradas.
- Validar que `BUSCAR <cadena>` distingue mayusculas y minusculas.
- Validar que una busqueda sin resultados devuelve `RESULTADO 0`.
- Validar que `NUMERO` devuelve `OK <n>` con el numero de busquedas ejecutadas.
- Validar que `SALIR` devuelve `OK`.
- Validar que mensajes desconocidos devuelven `ERROR`.
- Validar que mensajes mal formados devuelven `ERROR`, por ejemplo:
  - `BUSCAR`
  - `BUSCAR a ver que encuentro`
  - `NUMERO algo`
  - `SALIR algo`

Archivos afectados:

- `tests/test_server.py`

### Entrega Test 1 OK

Estado esperado: GREEN.

Implementacion minima prevista:

- Crear clase `Server`.
- Implementar el parseo de mensajes.
- Implementar la logica de respuestas.
- Implementar contador de busquedas.
- Implementar busqueda en ficheros.
- Implementar bucle UDP de recepcion y respuesta.
- Permitir parada controlada al recibir `SALIR`.

Archivos afectados:

- `src/server.py`
- `src/main.py`
- `tests/test_server.py`

### Entrega Refactor 1

Objetivo:

- Separar la logica pura del protocolo de la logica de socket si fuera necesario.
- Mantener nombres simples y orientados a examen.
- Eliminar duplicacion evidente sin introducir sobreingenieria.
- Confirmar que todos los tests acumulados siguen en verde.

Archivos afectados:

- `src/server.py`
- `src/main.py`
- `tests/test_server.py`

### Etiqueta requerida

Cuando esta iteracion este terminada y verificada, se avisara al usuario para
que etiquete la entrega como:

```text
Servidor
```

## Iteracion 2: Cliente

### Objetivo

Implementar el cliente UDP. El cliente se conectara automaticamente a la
direccion del servidor definida en los requisitos, enviara un minimo de 3
mensajes, imprimira por salida standard las respuestas recibidas y terminara
tras el ultimo mensaje.

### Entrega Test 2

Estado esperado: RED.

Pruebas unitarias previstas en `tests/test_client.py`:

- Validar que el cliente tiene configurados por defecto host `127.0.0.1` y
  puerto `16063`.
- Validar que envia una secuencia minima de 3 mensajes.
- Validar que imprime las respuestas recibidas por salida standard.
- Validar que informa de errores de comunicacion cuando se producen.

Archivos afectados:

- `tests/test_client.py`

### Entrega Test 2 OK

Estado esperado: GREEN.

Implementacion minima prevista:

- Crear clase `Client`.
- Implementar envio UDP de mensajes.
- Implementar recepcion de respuestas UDP.
- Implementar impresion de respuestas por salida standard.
- Implementar cierre correcto del socket.
- Adaptar `main.py` para poder lanzar servidor o cliente.

Archivos afectados:

- `src/client.py`
- `src/main.py`
- `tests/test_client.py`

### Entrega Refactor 2

Objetivo:

- Revisar nombres, responsabilidades y errores.
- Evitar duplicacion entre cliente y servidor.
- Mantener todos los tests acumulados en verde.

Archivos afectados:

- `src/client.py`
- `src/main.py`
- `tests/test_client.py`

### Etiqueta requerida

Cuando esta iteracion este terminada y verificada, se avisara al usuario para
que etiquete la entrega como:

```text
cliente
```

## Iteracion 3: Servidor modificado

### Objetivo

Modificar el servidor para que imprima en error standard una linea cada vez que
reciba un mensaje de un cliente, indicando la direccion IP del cliente y el
mensaje recibido.

### Entrega Test 3

Estado esperado: RED.

Pruebas unitarias previstas en `tests/test_server.py`:

- Validar que, al procesar un mensaje recibido, el servidor escribe en
  `stderr` la direccion IP del cliente.
- Validar que la linea escrita en `stderr` contiene tambien el mensaje recibido.
- Validar que esta traza no altera la respuesta UDP generada.

Archivos afectados:

- `tests/test_server.py`

### Entrega Test 3 OK

Estado esperado: GREEN.

Implementacion minima prevista:

- Anadir al servidor una salida de trazas por `stderr`.
- Registrar cada mensaje recibido junto con la IP del cliente.
- Mantener intacta la logica del protocolo.

Archivos afectados:

- `src/server.py`
- `tests/test_server.py`

### Entrega Refactor 3

Objetivo:

- Centralizar la escritura de trazas en un metodo pequeno si mejora la claridad.
- Confirmar que las trazas se escriben en `stderr`, no en `stdout`.
- Mantener todos los tests acumulados en verde.

Archivos afectados:

- `src/server.py`
- `tests/test_server.py`

### Etiqueta requerida

Cuando esta iteracion este terminada y verificada, se avisara al usuario para
que etiquete la entrega como:

```text
servidor modificado
```

## Iteracion 4: Cliente modificado

### Objetivo

Modificar el cliente para que pregunte al usuario por la direccion completa del
servidor e imprima un error si no consigue realizar la comunicacion.

### Entrega Test 4

Estado esperado: RED.

Pruebas unitarias previstas en `tests/test_client.py`:

- Validar que el cliente solicita al usuario la direccion completa del servidor.
- Validar que interpreta una direccion con formato `host:puerto`.
- Validar que muestra un error si el formato de direccion es incorrecto.
- Validar que muestra un error si no consigue comunicarse con el servidor.
- Validar que, con una direccion valida, sigue enviando los mensajes previstos e
  imprimiendo las respuestas.

Archivos afectados:

- `tests/test_client.py`

### Entrega Test 4 OK

Estado esperado: GREEN.

Implementacion minima prevista:

- Anadir lectura interactiva de direccion del servidor.
- Parsear `host:puerto`.
- Gestionar errores de formato.
- Gestionar errores de comunicacion.
- Mantener cierre correcto del socket.

Archivos afectados:

- `src/client.py`
- `src/main.py`
- `tests/test_client.py`

### Entrega Refactor 4

Objetivo:

- Separar el parseo de direccion de la comunicacion UDP.
- Revisar mensajes de error para que sean claros y utiles en examen.
- Mantener todos los tests acumulados en verde.

Archivos afectados:

- `src/client.py`
- `src/main.py`
- `tests/test_client.py`

### Etiqueta requerida

Cuando esta iteracion este terminada y verificada, se avisara al usuario para
que etiquete la entrega como:

```text
cliente modificado
```

## Iteracion 5: Documentacion final

### Objetivo

Documentar el puerto elegido para el servidor y el procedimiento completo para
ejecutar el codigo desarrollado.

### Entrega Test 5

Estado esperado: RED.

Pruebas documentales previstas:

- Comprobar que `README.txt` existe.
- Comprobar que `README.txt` documenta el puerto de escucha del servidor.
- Comprobar que `README.txt` indica como ejecutar servidor y cliente.
- Comprobar que `INSTALL.txt` existe.
- Comprobar que `INSTALL.txt` indica sistema operativo, herramientas
  necesarias, preparacion de entorno y comandos `make`.

Archivos afectados:

- `tests/test_documentacion.py`

### Entrega Test 5 OK

Estado esperado: GREEN.

Implementacion minima prevista:

- Crear o completar `README.txt`.
- Crear o completar `INSTALL.txt`.
- Documentar:
  - sistema operativo previsto,
  - Python,
  - `venv`,
  - `make`,
  - `unittest`,
  - comandos de instalacion,
  - comandos de ejecucion,
  - ejemplos de uso,
  - puerto de escucha `16063`.

Archivos afectados:

- `README.txt`
- `INSTALL.txt`
- `tests/test_documentacion.py`

### Entrega Refactor 5

Objetivo:

- Revisar claridad, ortografia y coherencia de la documentacion.
- Confirmar que los comandos documentados coinciden con el `Makefile`.
- Mantener todos los tests acumulados en verde.

Archivos afectados:

- `README.txt`
- `INSTALL.txt`
- `Makefile`
- `tests/test_documentacion.py`

## Pruebas de integracion

Las pruebas de integracion se iran incorporando cuando las pruebas unitarias de
cliente y servidor esten en verde.

Archivo previsto:

- `tests/test_integracion.py`

Cobertura prevista:

- Arrancar un servidor UDP real en proceso auxiliar o hilo controlado.
- Enviar `BUSCAR <cadena>` desde un cliente real y validar la respuesta.
- Enviar `NUMERO` tras varias busquedas y validar el contador.
- Enviar un mensaje invalido y validar `ERROR`.
- Enviar `SALIR` y validar `OK` y parada controlada.

Estas pruebas se ejecutaran tambien con:

```bash
make test
```

## Secuencia resumida

1. `Test 1` -> `Test 1 OK` -> `Refactor 1` -> avisar para etiqueta
   `Servidor`.
2. `Test 2` -> `Test 2 OK` -> `Refactor 2` -> avisar para etiqueta `cliente`.
3. `Test 3` -> `Test 3 OK` -> `Refactor 3` -> avisar para etiqueta
   `servidor modificado`.
4. `Test 4` -> `Test 4 OK` -> `Refactor 4` -> avisar para etiqueta
   `cliente modificado`.
5. `Test 5` -> `Test 5 OK` -> `Refactor 5` -> documentacion final.

En cada entrega se ejecutara:

```bash
make test
```

En las entregas `Test n` se espera fallo por funcionalidad aun no implementada.
En las entregas `Test n OK` y `Refactor n` se espera que todos los tests
acumulados esten en verde.
