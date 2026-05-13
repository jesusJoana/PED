# Plan de iteraciones - Practica 6

## Objetivo del proyecto

Implementar un sistema cliente-servidor sencillo usando sockets TCP de Internet
orientados a conexion, es decir, sockets del dominio `PF_INET`/`AF_INET` y tipo
`SOCK_STREAM`.

El cliente enviara al servidor la ruta absoluta de un fichero. El servidor
respondera con el contenido de dicho fichero o con un mensaje de error si no
puede leerlo. El cliente mostrara la respuesta recibida por su salida estandar
y finalizara. El servidor permanecera activo hasta que el usuario fuerce su
cierre.

## Requisitos del enunciado

- R1: Los procesos cliente y servidor deben contener en sus nombres las cadenas
  `cli6` y `serv6`, comprobables mediante `ps`.
- R2: La comunicacion debe realizarse mediante sockets TCP de Internet,
  orientados a conexion.
- R3: El cliente se conectara al servidor y le enviara una peticion de fichero.
- R4: El servidor respondera con el contenido del fichero solicitado.
- R5: Si el servidor no puede proporcionar el fichero, respondera con un
  mensaje de error.
- R6: El cliente mostrara por salida estandar la respuesta recibida.
- R7: El cliente terminara despues de imprimir la respuesta.
- R8: El servidor no terminara automaticamente tras atender una peticion; solo
  finalizara si el usuario fuerza su cierre.

## Restricciones del contrato PED

- Lenguaje principal: Python.
- Paradigma: Programacion Orientada a Objetos.
- Punto de entrada unico: `src/main.py`.
- Ejecucion mediante `make`.
- Pruebas mediante `unittest`.
- Separacion entre pruebas unitarias e integracion.
- Uso de `setproctitle` para cambiar el nombre visible del proceso.
- Host y puerto definidos en los constructores de cliente y servidor, no por
  argumentos de terminal.
- Host por defecto: `127.0.0.1`.
- Puerto por defecto: `16063`.

## Estructura prevista

```text
p6/
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
  docs/
    plan_iteraciones.md
  Makefile
  requirements.txt
  README.txt
  INSTALL.txt
  fichero.txt
```

## Diseno tecnico de alto nivel

### Cliente

La clase `FileClient` sera responsable de:

- almacenar host y puerto por defecto;
- validar que la ruta solicitada sea absoluta;
- abrir un socket TCP `AF_INET/SOCK_STREAM`;
- conectarse al servidor;
- enviar la ruta del fichero codificada en UTF-8;
- cerrar la escritura del socket con `shutdown(SHUT_WR)` para indicar fin de
  peticion;
- recibir la respuesta completa hasta que el servidor cierre la conexion;
- devolver la respuesta como texto.

### Servidor

La clase `FileServer` sera responsable de:

- almacenar host y puerto por defecto;
- crear un socket TCP `AF_INET/SOCK_STREAM`;
- enlazarlo a host y puerto;
- escuchar conexiones entrantes;
- aceptar clientes en un bucle permanente;
- atender cada cliente sin finalizar el proceso servidor;
- leer la ruta solicitada hasta fin de peticion;
- responder con el contenido del fichero o con un mensaje `ERROR:`.

### main.py

El fichero `src/main.py` sera el unico punto de entrada:

- `python src/main.py server` arrancara el servidor y asignara el nombre
  `serv6`;
- `python src/main.py client /ruta/absoluta/fichero.txt` arrancara el cliente,
  asignara el nombre `cli6`, imprimira la respuesta y terminara.

## Iteracion 1 - Unitarios de cliente y servidor base

### Test 1 Unitario - RED

Objetivo:

Definir el comportamiento basico de las clases principales sin depender todavia
de procesos reales completos.

Pruebas previstas:

- `tests/test_client.py`
  - El cliente tiene host y puerto por defecto.
  - El cliente rechaza rutas relativas.
  - El cliente envia una ruta mediante TCP a un servidor de prueba y devuelve la
    respuesta recibida.
- `tests/test_server.py`
  - El servidor tiene host y puerto por defecto.
  - El servidor crea un socket `AF_INET/SOCK_STREAM`.
  - El servidor construye una respuesta con el contenido de un fichero
    existente.
  - El servidor devuelve un mensaje que empieza por `ERROR:` si el fichero no
    existe o no puede leerse.

Requisitos cubiertos:

- R2, R3, R4, R5.

Archivos afectados:

- `tests/test_client.py`
- `tests/test_server.py`

Estado esperado:

- Las pruebas fallan porque aun no existen las clases o metodos necesarios.

### Test 1 OK - GREEN

Objetivo:

Implementar el minimo codigo necesario para que pasen los unitarios de cliente
y servidor base.

Archivos afectados:

- `src/config.py`
- `src/client.py`
- `src/server.py`
- `src/__init__.py`

Estrategia:

- Crear constantes compartidas.
- Implementar `FileClient`.
- Implementar `FileServer.create_socket`.
- Implementar `FileServer.build_response`.

### Refactor 1

Solo se realizara si el codigo queda duplicado o poco claro. No se modificaran
tests ni comportamiento observable.

## Iteracion 2 - Unitarios de protocolo y main.py

### Test 2 Unitario - RED

Objetivo:

Definir el procesamiento de una peticion TCP individual y el punto de entrada
del programa.

Pruebas previstas:

- `tests/test_server.py`
  - El servidor procesa una peticion textual y devuelve la respuesta correcta.
  - El servidor puede atender una conexion TCP individual sin cerrar el proceso
    completo.
- `tests/test_client.py`
  - El cliente recibe respuestas completas aunque lleguen en varios fragmentos.
- Opcional, si aporta claridad:
  - `tests/test_main.py`
    - El parser acepta los modos `server` y `client`.
    - El modo `client` exige una ruta de fichero.

Requisitos cubiertos:

- R3, R4, R5, R6, R7, R8.

Archivos afectados:

- `tests/test_client.py`
- `tests/test_server.py`
- opcionalmente `tests/test_main.py`

Estado esperado:

- Las pruebas fallan porque el protocolo TCP completo y/o `main.py` aun no
  estan terminados.

### Test 2 OK - GREEN

Objetivo:

Completar el protocolo interno y el punto de entrada.

Archivos afectados:

- `src/client.py`
- `src/server.py`
- `src/main.py`

Estrategia:

- Implementar recepcion completa en cliente.
- Implementar lectura completa de peticion en servidor.
- Implementar `handle_client`.
- Implementar `process_request`.
- Implementar parser de `main.py`.
- Preparar asignacion de nombres `cli6` y `serv6` con `setproctitle`.

### Refactor 2

Solo se realizara si hay una mejora clara de nombres, responsabilidades o
simplicidad.

## Iteracion 3 - Integracion TCP real

### Test 3 Integracion - RED

Objetivo:

Validar el comportamiento extremo a extremo con procesos reales y sockets TCP
reales.

Pruebas previstas:

- `tests/test_integracion.py`
  - Un servidor real y un cliente real se comunican por TCP.
  - El cliente imprime por salida estandar el contenido del fichero solicitado.
  - El cliente termina despues de imprimir la respuesta.
  - El servidor sigue vivo tras atender una peticion.
  - El servidor atiende varios clientes consecutivos.

Requisitos cubiertos:

- R2, R3, R4, R6, R7, R8.

Archivos afectados:

- `tests/test_integracion.py`

Estado esperado:

- Las pruebas pueden fallar por detalles de sincronizacion, cierre de sockets o
  persistencia del servidor.

### Test 3 Integracion OK - GREEN

Objetivo:

Ajustar la implementacion para superar las pruebas de integracion reales,
manteniendo en verde todos los unitarios acumulados.

Archivos afectados:

- `src/server.py`
- `src/client.py`
- `src/main.py`
- `Makefile`
- `fichero.txt`

Estrategia:

- Asegurar que el servidor queda escuchando en bucle permanente.
- Asegurar que cada conexion se cierra correctamente tras enviar la respuesta.
- Asegurar que el cliente no queda bloqueado y termina tras recibir la
  respuesta.
- Crear objetivos `make server`, `make client`, `make test` y `make install`.

### Refactor 3

Solo se realizara si es necesario simplificar el cierre de conexiones, evitar
duplicidades o mejorar legibilidad.

## Iteracion 4 - Integracion de errores, nombres y documentacion

### Test 4 Integracion - RED

Objetivo:

Validar los requisitos finales de examen: errores, nombres de proceso,
ejecucion mediante `make` y documentacion.

Pruebas previstas:

- `tests/test_integracion.py`
  - El cliente real solicita un fichero inexistente y muestra una respuesta que
    empieza por `ERROR:`.
  - El proceso servidor aparece como `serv6` en `ps`.
  - El proceso cliente aparece como `cli6` en `ps`.
  - El `Makefile` lanza cliente y servidor desde `src/main.py`.
  - El `Makefile` no pasa host ni puerto por linea de comandos.

Requisitos cubiertos:

- R1, R5, R6 y restricciones del contrato PED.

Archivos afectados:

- `tests/test_integracion.py`

Estado esperado:

- Las pruebas fallan si falta `setproctitle`, documentacion o algun objetivo de
  `make`.

### Test 4 Integracion OK - GREEN

Objetivo:

Completar los requisitos finales y dejar el proyecto ejecutable.

Archivos afectados:

- `src/main.py`
- `requirements.txt`
- `README.txt`
- `INSTALL.txt`
- `Makefile`

Estrategia:

- Usar `setproctitle("serv6")` en modo servidor.
- Usar `setproctitle("cli6")` en modo cliente.
- Documentar instalacion, ejecucion, pruebas y funcionamiento.
- Verificar que `make test` ejecuta todas las pruebas con `unittest`.

### Refactor 4

Solo se realizara si queda alguna mejora interna evidente. No se modificaran
tests ni requisitos funcionales.

## Riesgos y medidas de control

- Puerto ocupado:
  - Riesgo: `127.0.0.1:16063` puede estar usado por otra practica.
  - Medida: cerrar servidores anteriores antes de ejecutar integracion.

- Cliente demasiado rapido para comprobar `cli6` con `ps`:
  - Riesgo: el proceso cliente puede terminar antes de que la prueba lo detecte.
  - Medida: usar un escenario controlado de prueba que lo mantenga bloqueado el
    tiempo suficiente sin cambiar el comportamiento normal.

- Bloqueos TCP:
  - Riesgo: cliente o servidor pueden quedarse esperando datos.
  - Medida: el cliente indicara fin de peticion con `shutdown(SHUT_WR)` y ambos
    lados leeran hasta EOF cuando corresponda.

- Ficheros grandes:
  - Riesgo: una unica llamada a `recv` no garantiza recibir todo el contenido.
  - Medida: recibir en bucle por bloques de `BUFFER_SIZE`.

## Criterio de finalizacion

La practica se considerara terminada cuando:

- todos los tests unitarios pasen;
- todos los tests de integracion pasen;
- `make test` funcione desde la carpeta `p6`;
- `make server` deje el servidor activo hasta cierre manual;
- `make client` imprima la respuesta y termine;
- `ps` permita observar `serv6` y `cli6`;
- existan `README.txt`, `INSTALL.txt` y `requirements.txt`.
