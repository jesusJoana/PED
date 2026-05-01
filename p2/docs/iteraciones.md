# Plan de iteraciones TDD

## Objetivo del proyecto

Construir un sistema cliente-servidor de lectura de ficheros `.txt` usando procesos UNIX y tuberias.

El proyecto tendra un unico punto de entrada, `src/main.py`, que creara un proceso hijo mediante `fork()`.
El proceso hijo actuara como cliente y se llamara `cli2`; el proceso padre actuara como servidor y se llamara `serv2`.

La comunicacion se hara con dos pipes:

- Pipe de peticion: el hijo envia al padre el nombre del fichero solicitado.
- Pipe de respuesta: el padre devuelve al hijo el contenido del fichero o un mensaje de error controlado.

La estructura prevista del proyecto sera:

```text
p2/
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
├── docs/
│   └── iteraciones.md
├── Makefile
├── README.md
├── INSTALL
└── requirements.txt
```

## Iteracion 1: estructura inicial y prueba minima

### Objetivo

Crear la estructura `src/` y `tests/` y dejar preparado el entorno para trabajar con `unittest`.

### Pruebas esperadas

- Existe el modulo principal `src/main.py`.
- El comando `make test` ejecuta las pruebas desde `tests/`.

### Implementacion prevista

- Crear `src/main.py`.
- Crear `tests/test_main.py`.
- Ajustar la importacion del modulo si fuera necesario.
- Mantener el `Makefile` como punto unico para ejecutar pruebas.

## Iteracion 2: validacion de argumentos

### Objetivo

Validar que el programa recibe exactamente un parametro: la ruta del fichero solicitado por el cliente.

### Pruebas esperadas

- Si no se pasa ningun parametro, se devuelve error de uso.
- Si se pasan demasiados parametros, se devuelve error de uso.
- Si se pasa un unico parametro, la validacion lo acepta.

### Implementacion prevista

- Crear una funcion testeable para validar argumentos.
- Separar la logica de validacion del arranque real con `fork()`.

## Iteracion 3: lectura del fichero por parte del servidor

### Objetivo

Implementar la logica que usara el servidor para leer el fichero solicitado.

### Pruebas esperadas

- Si el fichero existe, se devuelve su contenido.
- Si el fichero no existe, se devuelve un mensaje de error controlado.
- Si la ruta no corresponde a un fichero valido, se devuelve un mensaje de error controlado.

### Implementacion prevista

- Crear una funcion que reciba una ruta y devuelva una respuesta textual.
- No usar todavia pipes ni `fork()` en esta iteracion.

## Iteracion 4: utilidades de comunicacion por pipes

### Objetivo

Preparar funciones pequenas para enviar y recibir mensajes por descriptores de fichero UNIX.

### Pruebas esperadas

- Un mensaje escrito en un pipe se puede leer completo desde el otro extremo.
- Un mensaje vacio se gestiona sin bloquear indebidamente.

### Implementacion prevista

- Crear funciones para escribir bytes en un descriptor.
- Crear funciones para leer bytes hasta EOF.
- Cerrar correctamente los extremos del pipe cuando corresponda.

## Iteracion 5: fork cliente-servidor minimo

### Objetivo

Crear el proceso hijo con `fork()` y comprobar la comunicacion basica entre cliente y servidor.

### Pruebas esperadas

- El hijo puede enviar una peticion simple al padre.
- El padre puede responder al hijo.
- El hijo muestra la respuesta recibida.
- El padre espera al hijo para evitar procesos zombis.

### Implementacion prevista

- Crear dos pipes: uno para peticiones y otro para respuestas.
- En el hijo, cerrar los extremos que no usa y ejecutar la logica de cliente.
- En el padre, cerrar los extremos que no usa y ejecutar la logica de servidor.
- Usar `os.waitpid()` en el padre.

## Iteracion 6: integracion con lectura real de ficheros

### Objetivo

Unir la comunicacion cliente-servidor con la lectura real del fichero indicado por parametro.

### Pruebas esperadas

- Al ejecutar `python3 src/main.py fichero.txt`, el hijo imprime el contenido del fichero.
- Si el fichero no existe, el hijo imprime el error recibido del servidor.

### Implementacion prevista

- El hijo enviara al padre la ruta recibida por parametro.
- El padre leera esa ruta usando la funcion ya probada.
- El padre devolvera la respuesta por el pipe de respuesta.

## Iteracion 7: nombres de proceso `cli2` y `serv2`

### Objetivo

Nombrar los procesos para que puedan comprobarse con el comando `ps`.

### Pruebas esperadas

- El proceso hijo aparece como `cli2`.
- El proceso padre aparece como `serv2`.
- La funcionalidad de lectura sigue funcionando.

### Implementacion prevista

- Usar la libreria `setproctitle`.
- Anadir `setproctitle` a `requirements.txt`.
- Ajustar `make install` para instalar dependencias desde `requirements.txt`.
- Incluir una forma sencilla de ver los procesos durante una ejecucion de prueba si hiciera falta.

## Iteracion 8: documentacion final

### Objetivo

Documentar como instalar, probar y ejecutar el proyecto.

### Pruebas esperadas

- `README.md` explica que hace el proyecto y como se usa.
- `INSTALL` explica los pasos de instalacion.
- Se indica claramente que `make install` instala `setproctitle`.
- Se documenta como comprobar los nombres de proceso con `ps`.

### Implementacion prevista

- Completar `README.md`.
- Completar `INSTALL`.
- Revisar que `make install`, `make test` y `make run` funcionan como se describe.

## Criterios de finalizacion

El proyecto se considerara terminado cuando:

- La implementacion este en `src/main.py`.
- Las pruebas esten en `tests/`.
- `make install` cree el entorno e instale dependencias.
- `make test` ejecute correctamente la suite de pruebas.
- `make run FILE=...` ejecute el cliente-servidor.
- El hijo imprima la respuesta enviada por el padre.
- Los procesos puedan verse como `cli2` y `serv2` mediante `ps`.
- `README.md` e `INSTALL` documenten el uso completo.
