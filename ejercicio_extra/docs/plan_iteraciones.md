# Plan de iteraciones - ejercicio_extra

## Contexto del ejercicio

Se desarrollara un sistema cliente-servidor sencillo usando sockets Unix Domain
Socket, de tipo `SOCK_STREAM`.

El cliente enviara al servidor el path completo de un fichero. El servidor
respondera con el contenido del fichero o con un mensaje de error si no puede
proporcionarlo. El cliente mostrara por terminal la respuesta recibida.

Requisitos principales:

- El servidor debe aceptar mas de un cliente y no finalizar tras atender una
  unica peticion.
- El servidor se detendra manualmente con `Control + C`.
- Todos los sockets UDS se crearan dentro de `/tmp`.
- El socket estara personalizado para el grupo 6.
- La direccion del socket sera configurable sin recompilar ni modificar codigo.
- Los procesos deberan contener en su nombre:
  - `serv4` para el servidor.
  - `cli4` para el cliente.
- La practica se implementara en Python, con OOP, `unittest` y ejecucion
  mediante `make`.

## Decisiones tecnicas

- Carpeta de trabajo: `ejercicio_extra`.
- Lenguaje: Python.
- Paradigma: Programacion Orientada a Objetos.
- Tests: `unittest`.
- IPC: Unix Domain Sockets, `SOCK_STREAM`.
- Ruta por defecto del socket:

```text
/tmp/ped_g6_serv4.sock
```

- La ruta se guardara en:

```text
config.txt
```

Cliente y servidor leeran el mismo fichero de configuracion. Para cambiar la
direccion del socket, bastara con editar `config.txt`.

- Para los nombres de proceso se usara `setproctitle`.

## Estructura prevista

```text
ejercicio_extra/
├── Makefile
├── config.txt
├── requirements.txt
├── README.txt
├── INSTALL.txt
├── docs/
│   └── plan_iteraciones.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── server.py
│   ├── client.py
│   └── main.py
└── tests/
    ├── test_config.py
    ├── test_server.py
    ├── test_client.py
    ├── test_main.py
    └── test_integracion.py
```

## Iteraciones

### Test 1 Unitario - Configuracion y servidor

Objetivo:

Definir en rojo las pruebas de configuracion del socket UDS y de la logica
basica del servidor, sin usar todavia sockets reales.

Archivos afectados:

```text
tests/test_config.py
tests/test_server.py
```

Pruebas previstas:

- La configuracion lee correctamente la ruta del socket desde `config.txt`.
- La ruta configurada no puede estar vacia.
- La ruta configurada debe estar dentro de `/tmp`.
- El servidor guarda la ruta del socket configurada.
- El servidor devuelve el contenido de un fichero existente.
- El servidor devuelve un mensaje con `ERROR` si el fichero no existe.

Estado esperado:

```text
RED
```

Las pruebas deben fallar porque aun no existen `src/config.py` ni
`src/server.py`.

### Test 1 OK - Implementacion minima de configuracion y servidor

Objetivo:

Implementar el codigo minimo para pasar las pruebas de `Test 1 Unitario`.

Archivos afectados:

```text
src/__init__.py
src/config.py
src/server.py
config.txt
```

Implementacion prevista:

- Clase `SocketConfig`.
- Clase `FileServer`.
- Metodo para generar una respuesta a partir de un path de fichero.

Documentacion breve en codigo:

- Comentario breve en la clase de configuracion.
- Comentario breve en la clase servidor.
- Comentario breve en el metodo que construye la respuesta.

Estado esperado:

```text
GREEN
```

### Refactor 1 - Claridad en la logica del servidor

Objetivo:

Mejorar la organizacion interna del servidor sin cambiar comportamiento.

Archivos afectados:

```text
src/server.py
```

Refactor previsto:

Extraer responsabilidades internas:

```text
build_response(path)
_read_file(path)
_build_error(path, error)
```

Motivo:

- Separar la lectura del fichero de la construccion del mensaje de error.
- Dejar el metodo publico mas claro.
- Mantener todos los tests en verde.

Estado esperado:

```text
GREEN
```

## Test 2 Unitario - Cliente y main

Objetivo:

Definir en rojo las pruebas de la clase cliente y del punto de entrada
obligatorio `main.py`.

Archivos afectados:

```text
tests/test_client.py
tests/test_main.py
```

Pruebas previstas:

- El cliente se conecta a un socket UDS.
- El cliente envia el path completo del fichero.
- El cliente devuelve la respuesta recibida del servidor.
- `main.py` acepta el modo `server`.
- `main.py` acepta el modo `client <path>`.
- El modo servidor configura un nombre de proceso que contiene `serv4`.
- El modo cliente configura un nombre de proceso que contiene `cli4`.
- El cliente exige un path de fichero cuando se usa el modo `client`.

Estado esperado:

```text
RED
```

Las pruebas deben fallar porque aun no existen `src/client.py` ni `src/main.py`.

### Test 2 OK - Implementacion minima de cliente y main

Objetivo:

Implementar el codigo minimo para pasar las pruebas de `Test 2 Unitario` y
mantener en verde todos los tests acumulados.

Archivos afectados:

```text
src/client.py
src/main.py
requirements.txt
```

Implementacion prevista:

- Clase `FileClient`.
- Metodo para pedir un fichero al servidor.
- Punto de entrada `main.py`.
- Modos:
  - `server`
  - `client <path>`
- Uso de `setproctitle` para incluir `serv4` y `cli4` en los nombres de
  proceso.

Documentacion breve en codigo:

- Comentario breve en la clase cliente.
- Comentario breve en el metodo que envia la peticion.
- Comentario breve en las funciones principales de `main.py`.

Estado esperado:

```text
GREEN
```

## Test 3 Integracion - Cliente-servidor real con UDS

Objetivo:

Definir en rojo las pruebas del sistema completo usando sockets UDS reales de
tipo `SOCK_STREAM`.

Archivos afectados:

```text
tests/test_integracion.py
```

Pruebas previstas:

- El servidor real arranca y crea un socket dentro de `/tmp`.
- El cliente pide un fichero existente y recibe su contenido.
- El cliente pide un fichero inexistente y recibe un mensaje con `ERROR`.
- Dos clientes pueden conectarse de forma consecutiva.
- El servidor sigue vivo despues de atender al primer cliente.

Estado esperado:

```text
RED
```

La prueba puede fallar si falta completar el bucle real del servidor, la
limpieza del socket o algun detalle de comunicacion.

### Test 3 Integracion OK - Sistema completo funcionando

Objetivo:

Ajustar cliente, servidor y punto de entrada para que las pruebas de integracion
pasen manteniendo tambien en verde todos los tests unitarios.

Archivos afectados posiblemente:

```text
src/server.py
src/client.py
src/main.py
```

Implementacion prevista:

- Servidor con socket UDS `SOCK_STREAM`.
- `bind` sobre la ruta leida desde `config.txt`.
- `listen` y bucle continuo de `accept`.
- Atencion de cada cliente sin finalizar el servidor.
- Cliente conectado al mismo socket configurado.
- Limpieza del socket UDS al cerrar el servidor.

Estado esperado:

```text
GREEN
```

### Refactor 2 - Separacion de responsabilidades del servidor UDS

Objetivo:

Mejorar la legibilidad del servidor real una vez que la integracion este en
verde.

Archivos afectados:

```text
src/server.py
```

Refactor previsto:

Separar el bucle principal de las operaciones auxiliares:

```text
serve_forever()
_prepare_socket()
_handle_connection(connection)
close()
```

Motivo:

- Hacer mas claro el bucle que acepta multiples clientes.
- Separar la preparacion del socket de la atencion de cada conexion.
- Facilitar la explicacion en examen.
- Mantener todos los tests en verde.

Estado esperado:

```text
GREEN
```

## Entrega 4 - Makefile y documentacion

Objetivo:

Dejar la practica lista para ejecutar y entregar. Esta entrega no requiere tests
propios.

Archivos afectados:

```text
Makefile
README.txt
INSTALL.txt
```

Contenido previsto del `Makefile`:

```text
make install
make test
make server
make client FILE=/ruta/completa/fichero.txt
make clean
```

Contenido previsto de `README.txt`:

- Descripcion general del proyecto.
- Explicacion del sistema cliente-servidor.
- Explicacion de sockets UDS `SOCK_STREAM`.
- Explicacion de `config.txt`.
- Instrucciones de uso.
- Ejemplos de ejecucion.
- Como detener el servidor con `Control + C`.

Contenido previsto de `INSTALL.txt`:

- Creacion del entorno virtual.
- Instalacion de dependencias.
- Dependencia `setproctitle`.
- Ejecucion de pruebas.
- Ejecucion del servidor.
- Ejecucion del cliente.

Estado esperado:

```text
Practica documentada y lista para entrega.
```

## Resumen de entregas

```text
1. Test 1 Unitario
2. Test 1 OK
3. Refactor 1
4. Test 2 Unitario
5. Test 2 OK
6. Test 3 Integracion
7. Test 3 Integracion OK
8. Refactor 2
9. Entrega 4 - Makefile y documentacion
```

Total: 9 pasos.

Se mantiene por debajo del maximo de 10 iteraciones solicitado y se respeta el
ciclo:

```text
RED -> GREEN -> REFACTOR
```
