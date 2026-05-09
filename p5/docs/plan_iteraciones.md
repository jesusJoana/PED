# Plan de iteraciones y entregas - Practica 5

## Objetivo general

Construir un sistema cliente-servidor sencillo mediante sockets UDP de Internet
(`PF_INET`/`AF_INET`, `SOCK_DGRAM`).

El cliente pedira al servidor el contenido de un fichero. El servidor respondera
con el contenido del fichero o con un mensaje de error si no puede devolverlo.
El cliente mostrara por terminal la respuesta recibida.

## Requisitos del enunciado

- R1: Los procesos cliente y servidor deben contener en sus nombres las cadenas
  `cli5` y `serv5`, comprobable mediante `ps`.
- R2: El cliente enviara una peticion al servidor mediante un socket UDP de
  Internet.
- R3: El servidor respondera con el contenido del fichero o con un mensaje de
  error si no puede devolverlo.
- R4: El cliente mostrara la respuesta recibida por terminal.
- R5: El servidor debe permitir la conexion de mas de un cliente
  simultaneamente.
- R6: El servidor no debe cerrarse al terminar una peticion; se cerrara
  manualmente cuando el usuario quiera.

## Decisiones tecnicas iniciales

- Se usara Python con programacion orientada a objetos.
- La ejecucion se hara mediante `make`.
- Las pruebas se haran con `unittest`.
- Primero se completaran las pruebas unitarias.
- Despues, con las unitarias en verde, se completaran las pruebas de
  integracion.
- No se mezclaran pruebas unitarias e integracion en una misma entrega.
- Se usara `setproctitle` para que los procesos aparezcan como `cli5` y
  `serv5` al consultarlos con `ps`.
- El cliente usara un socket UDP con `connect((host, port))`, aunque UDP siga
  siendo no orientado a conexion.
- Host y puerto estaran definidos en los constructores de cliente y servidor.
- Por defecto se usara host `127.0.0.1` y puerto `16063`.
- El cliente enviara la ruta absoluta del fichero como peticion.
- El servidor respondera mediante UDP.
- Se asumiran ficheros pequenos, adecuados para una respuesta en un datagrama
  UDP. Esta limitacion se documentara en `README.txt`.
- El servidor permanecera activo hasta que se cierre manualmente.
- Para justificar la atencion simultanea de mas de un cliente, el servidor
  delegara cada peticion recibida en un hilo.

## Estructura prevista

```text
p5/
  Makefile
  README.txt
  INSTALL.txt
  requirements.txt
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

## Forma de entrega TDD

El desarrollo se divide en dos fases:

1. Fase unitaria: primero se prueban las clases principales por separado.
2. Fase de integracion: despues se prueban procesos reales y flujo extremo a
   extremo.

Cada entrega al repositorio tendra un estado esperado claro:

- `Test n Unitario`: RED.
- `Test n Unitario OK`: GREEN.
- `Test n Integración`: RED.
- `Test n Integración OK`: GREEN.
- `Refactor n`: GREEN.

Las pruebas se organizaran dentro de cada archivo con comentarios de iteracion,
indicando requisitos y comportamiento comprobado.

## Fase 1 - Pruebas unitarias

### Iteracion 1 - Cliente UDP basico

#### Entrega Test 1 Unitario - RED

Objetivo: definir el comportamiento minimo de la clase cliente.

Archivo: `tests/test_client.py`

Pruebas:

- Cliente con host `127.0.0.1` y puerto `16063` por defecto.
  - Requisitos: R2.
  - Comportamiento: el constructor configura el destino UDP por defecto.
- Cliente rechaza rutas relativas.
  - Requisitos: R2.
  - Comportamiento: la peticion debe usar una ruta absoluta.
- Cliente envia una peticion UDP real y recibe una respuesta.
  - Requisitos: R2.
  - Comportamiento: el cliente usa socket UDP real y devuelve el texto recibido.

Estado esperado: RED.

#### Entrega Test 1 Unitario OK - GREEN

Objetivo: implementar lo minimo de `FileClient`.

Archivos previstos:

- `src/config.py`
- `src/client.py`

Implementacion prevista:

- Constantes de host, puerto y tamano de buffer.
- Clase `FileClient`.
- Constructor con host y puerto por defecto.
- Validacion de ruta absoluta.
- Envio UDP con `connect((host, port))`, `send` y `recv`.

Estado esperado: GREEN.

### Iteracion 2 - Servidor UDP basico

#### Entrega Test 2 Unitario - RED

Objetivo: definir el comportamiento minimo de la clase servidor.

Archivo: `tests/test_server.py`

Pruebas:

- Servidor con host `127.0.0.1` y puerto `16063` por defecto.
  - Requisitos: R2, R3.
  - Comportamiento: el constructor configura el punto local UDP por defecto.
- Servidor construye una respuesta con el contenido de un fichero existente.
  - Requisitos: R3.
  - Comportamiento: al recibir una ruta valida, devuelve el contenido.
- Servidor crea un socket UDP de Internet.
  - Requisitos: R2.
  - Comportamiento: usa `AF_INET` y `SOCK_DGRAM`.

Estado esperado: RED.

#### Entrega Test 2 Unitario OK - GREEN

Objetivo: implementar lo minimo de `FileServer`.

Archivos previstos:

- `src/server.py`

Implementacion prevista:

- Clase `FileServer`.
- Constructor con host y puerto por defecto.
- Metodo `create_socket`.
- Metodo `build_response` para fichero existente.

Estado esperado: GREEN.

### Iteracion 3 - Error de lectura en servidor

#### Entrega Test 3 Unitario - RED

Objetivo: definir la respuesta del servidor cuando no puede leer el fichero.

Archivo: `tests/test_server.py`

Pruebas:

- Servidor devuelve mensaje `ERROR:` para fichero inexistente.
  - Requisitos: R3.
  - Comportamiento: la respuesta informa del fallo sin cerrar el programa.

Estado esperado: RED.

#### Entrega Test 3 Unitario OK - GREEN

Objetivo: implementar el manejo de error de lectura.

Archivo previsto:

- `src/server.py`

Implementacion prevista:

- Capturar `OSError` al leer el fichero.
- Devolver una respuesta textual que empiece por `ERROR:`.

Estado esperado: GREEN.

### Iteracion 4 - Procesamiento unitario de peticiones del servidor

#### Entrega Test 4 Unitario - RED

Objetivo: definir una unidad de procesamiento de peticion reutilizable por el
bucle UDP.

Archivo: `tests/test_server.py`

Pruebas:

- Servidor procesa una ruta recibida y devuelve respuesta sin cerrar el socket
  principal.
  - Requisitos: R3, R6.
  - Comportamiento: atender una peticion no implica finalizar el servidor.

Estado esperado: RED.

#### Entrega Test 4 Unitario OK - GREEN

Objetivo: implementar el procesamiento unitario de una peticion.

Archivo previsto:

- `src/server.py`

Implementacion prevista:

- Metodo auxiliar para resolver una peticion individual.
- Separar la construccion de respuesta del bucle permanente del servidor.

Estado esperado: GREEN.

### Iteracion 5 - Punto de entrada main.py

#### Entrega Test 5 Unitario - RED

Objetivo: definir el punto de entrada sin ejecutar todavia integracion real.

Archivo: `tests/test_main.py` o `tests/test_client.py`/`tests/test_server.py`
si se mantiene simple.

Pruebas:

- `main.py` acepta modo `client` con ruta de fichero.
  - Requisitos: R4 y contrato de trabajo.
  - Comportamiento: el modo cliente imprime la respuesta recibida.
- `main.py` acepta modo `server`.
  - Requisitos: contrato de trabajo.
  - Comportamiento: el modo servidor delega en la clase `FileServer`.

Estado esperado: RED.

#### Entrega Test 5 Unitario OK - GREEN

Objetivo: implementar `main.py` de forma minima.

Archivo previsto:

- `src/main.py`

Implementacion prevista:

- Parser con modos `client` y `server`.
- Cliente imprime por terminal la respuesta.
- Servidor arranca desde `main.py`.
- No se pasan host ni puerto por linea de comandos.

Estado esperado: GREEN.

## Fase 2 - Pruebas de integracion

### Iteracion 6 - Flujo UDP real con fichero existente

#### Entrega Test 6 Integración - RED

Objetivo: comprobar el flujo extremo a extremo con procesos y sockets reales.

Archivo: `tests/test_integracion.py`

Pruebas:

- Cliente recibe contenido desde un servidor UDP real.
  - Requisitos: R2, R3, R4.
  - Comportamiento: servidor y cliente reales colaboran mediante UDP y el
    cliente imprime el contenido por terminal.
- `Makefile` lanza cliente y servidor desde `main.py` sin host ni puerto.
  - Requisitos: contrato de trabajo.
  - Comportamiento: la ejecucion se realiza con `make` y la configuracion de
    red queda en los constructores.

Estado esperado: RED.

#### Entrega Test 6 Integración OK - GREEN

Objetivo: ajustar lo minimo para que el flujo real funcione.

Archivos previstos:

- `src/main.py`
- `src/server.py`
- `src/client.py`
- `Makefile` si fuera necesario.

Implementacion prevista:

- Arranque real del servidor UDP.
- Cliente real solicita fichero y muestra respuesta.
- Mantener todas las pruebas unitarias en verde.

Estado esperado: GREEN.

### Iteracion 7 - Integracion con error de fichero

#### Entrega Test 7 Integración - RED

Objetivo: comprobar el flujo real cuando el fichero no existe.

Archivo: `tests/test_integracion.py`

Pruebas:

- Cliente imprime el error recibido del servidor.
  - Requisitos: R3, R4.
  - Comportamiento: ante una ruta inexistente, el flujo completo devuelve y
    muestra un mensaje de error.

Estado esperado: RED.

#### Entrega Test 7 Integración OK - GREEN

Objetivo: ajustar lo minimo para que el error funcione extremo a extremo.

Archivos previstos:

- `src/server.py`
- `src/client.py`

Estado esperado: GREEN.

### Iteracion 8 - Servidor persistente y varios clientes reales

#### Entrega Test 8 Integración - RED

Objetivo: comprobar que el servidor atiende mas de un cliente y permanece vivo.

Archivo: `tests/test_integracion.py`

Pruebas:

- Servidor atiende varios clientes reales.
  - Requisitos: R5, R6.
  - Comportamiento: varios clientes reciben respuesta del mismo servidor.
- Servidor sigue vivo tras responder a varias peticiones.
  - Requisitos: R6.
  - Comportamiento: el proceso servidor no termina automaticamente.

Estado esperado: RED.

#### Entrega Test 8 Integración OK - GREEN

Objetivo: implementar persistencia y atencion concurrente real.

Archivo previsto:

- `src/server.py`

Implementacion prevista:

- Bucle permanente con `recvfrom`.
- Hilo por peticion recibida.
- Respuesta enviada al origen de cada datagrama.

Estado esperado: GREEN.

### Iteracion 9 - Nombres de proceso cli5 y serv5

#### Entrega Test 9 Integración - RED

Objetivo: comprobar con `ps` los nombres de proceso pedidos.

Archivo: `tests/test_integracion.py`

Pruebas:

- Proceso servidor aparece como `serv5` en `ps`.
  - Requisitos: R1.
  - Comportamiento: al arrancar en modo servidor, el proceso cambia su nombre.
- Proceso cliente aparece como `cli5` en `ps`.
  - Requisitos: R1.
  - Comportamiento: al arrancar en modo cliente, el proceso cambia su nombre.

Estado esperado: RED.

#### Entrega Test 9 Integración OK - GREEN

Objetivo: implementar el cambio de nombre de proceso con `setproctitle`.

Archivos previstos:

- `requirements.txt`
- `src/main.py`

Implementacion prevista:

- Anadir dependencia `setproctitle`.
- En modo servidor, llamar a `setproctitle("serv5")`.
- En modo cliente, llamar a `setproctitle("cli5")`.

Estado esperado: GREEN.

### Iteracion 10 - Documentacion final

#### Entrega Test 10 Integración - RED

Objetivo: definir la documentacion obligatoria de cierre.

Archivo: `tests/test_integracion.py`

Pruebas:

- Existe `README.txt` y documenta uso basico.
  - Requisitos: contrato de trabajo.
  - Comportamiento: describe proyecto, ejecucion, ejemplo y limitacion UDP.
- Existe `INSTALL.txt` y documenta instalacion.
  - Requisitos: contrato de trabajo.
  - Comportamiento: describe entorno, dependencias, `make install`,
    `make test`, `make server` y `make client`.

Estado esperado: RED.

#### Entrega Test 10 Integración OK - GREEN

Objetivo: generar la documentacion final.

Archivos previstos:

- `README.txt`
- `INSTALL.txt`

Implementacion prevista:

- Manual de usuario y descripcion funcional en `README.txt`.
- Instrucciones de instalacion y ejecucion en `INSTALL.txt`.

Estado esperado: GREEN.

## Refactorizaciones

Las entregas `Refactor n` solo se haran cuando todos los tests esten en verde.

Reglas:

- No se modificaran tests.
- No se introduciran nuevas funcionalidades.
- Todos los tests acumulados deberan seguir pasando.

Posibles refactorizaciones:

- Extraer constantes compartidas.
- Mejorar nombres de clases y metodos.
- Eliminar duplicidades en tests.
- Simplificar gestion de procesos en pruebas de integracion.
