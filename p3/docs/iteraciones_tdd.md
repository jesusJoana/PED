# Plan de iteraciones TDD

## Objetivo de la practica

El proyecto consiste en implementar un sistema cliente-servidor de ficheros de texto usando tuberias FIFO de UNIX.

La aplicacion se desarrollara en Python y con programacion orientada a objetos. Aunque el enunciado pide un unico fichero principal llamado `main.py`, dentro de ese fichero organizaremos el codigo mediante clases y metodos para que sea mas facil de probar, mantener y explicar.

El programa debera crear dos procesos mediante `fork()`:

- El proceso hijo actuara como cliente y se llamara `cli3`.
- El proceso padre actuara como servidor y se llamara `serv3`.
- El cliente pedira al servidor el contenido de un fichero `.txt`.
- El servidor leera el fichero solicitado y devolvera su contenido al cliente.
- El cliente mostrara por pantalla la respuesta recibida.

## Enfoque general

Para poder aplicar TDD de forma sencilla, primero construiremos y probaremos las partes internas del sistema sin usar todavia procesos ni FIFO. Despues integraremos esas piezas en la ejecucion real con `fork()`.

La idea es separar responsabilidades en clases:

- `FileRequest`: representa y valida la peticion del cliente.
- `FileResponse`: representa la respuesta enviada por el servidor.
- `FileServer`: procesa peticiones y lee ficheros de texto.
- `FileClient`: envia peticiones y muestra respuestas.
- `FifoManager`: crea, gestiona y elimina las tuberias FIFO.

Estas clases estaran en `main.py`, pero sus metodos podran probarse desde los tests.

## Regla de entregas

Cada entrega indicada en este plan debera subirse al repositorio remoto de forma independiente.

El asistente preparara el estado de cada entrega y avisara cuando este lista, pero no realizara la subida al repositorio remoto. La subida la realizara siempre el usuario.

En las entregas de tipo `Test n`, el estado esperado sera que pasen los tests anteriores y fallen unicamente los tests nuevos de esa entrega. Cada entrega `Test n` podra contener uno o varios tests, pero siempre seran un conjunto minimo y centrado en el comportamiento funcional planificado para esa iteracion.

En las entregas de tipo `Test n OK`, el estado esperado sera que pasen todos los tests acumulados. En las entregas de tipo `Refactor n`, no se anadiran nuevos tests y todos los tests deberan seguir pasando.

## Iteracion 1: crear peticiones del cliente

### Entrega: Test 1

Crear un conjunto minimo de tests que compruebe que una instancia de `FileRequest` genera correctamente el mensaje de peticion para un fichero.

Ejemplo:

```txt
GET datos.txt
```

En esta entrega los tests nuevos deberan fallar porque el metodo todavia no estara implementado.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 1` esta listo para subir al repositorio remoto.

### Entrega: Test 1 OK

Implementar el metodo minimo en `FileRequest` para que los tests pasen.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 1 OK` esta listo para subir al repositorio remoto.

## Iteracion 2: interpretar peticiones y validar formato

### Entrega: Test 2

Crear un conjunto minimo de tests funcionalmente distinto que compruebe que `FileRequest` puede interpretar una peticion recibida y extraer el nombre del fichero solicitado.

Ejemplo:

```txt
GET datos.txt
```

Resultado esperado:

```txt
datos.txt
```

Al terminar esta entrega, el asistente avisara al usuario de que `Test 2` esta listo para subir al repositorio remoto.

### Entrega: Test 2 OK

Implementar el metodo que analiza el mensaje y extrae el nombre del fichero solicitado.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 2 OK` esta listo para subir al repositorio remoto.

## Iteracion 3: procesar ficheros en el servidor

### Entrega: Test 3

Crear un conjunto minimo de tests funcionalmente distinto que compruebe que `FileServer` lee correctamente el contenido de un fichero `.txt` existente.

Los tests usaran ficheros temporales para no depender de ficheros creados manualmente.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 3` esta listo para subir al repositorio remoto.

### Entrega: Test 3 OK

Implementar el metodo de lectura de ficheros en `FileServer`.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 3 OK` esta listo para subir al repositorio remoto.

## Iteracion 4: construir respuestas correctas y de error

### Entrega: Test 4

Crear un conjunto minimo de tests funcionalmente distinto que compruebe que `FileResponse` genera correctamente una respuesta con contenido y una respuesta de error cuando el fichero pedido no existe.

El programa no debe finalizar con una excepcion no controlada.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 4` esta listo para subir al repositorio remoto.

### Entrega: Test 4 OK

Implementar `FileResponse` y el control de error del servidor. Una respuesta de error podra ser:

```txt
ERROR: fichero no encontrado
```

Al terminar esta entrega, el asistente avisara al usuario de que `Test 4 OK` esta listo para subir al repositorio remoto.

## Refactor 1

Reorganizar el codigo sin cambiar el comportamiento ni los tests.

Objetivos:

- Mejorar nombres de clases, metodos y variables.
- Eliminar duplicacion si aparece.
- Anadir comentarios breves en metodos y tests.
- Mantener un nivel de codigo claro y medio, evitando soluciones demasiado complejas.

Al terminar esta entrega, el asistente avisara al usuario de que `Refactor 1` esta listo para subir al repositorio remoto.

## Iteracion 5: integrar FIFO, cliente y servidor

### Entrega: Test 5

Crear un conjunto minimo de tests funcionalmente distinto que compruebe que `FifoManager` crea correctamente las tuberias FIFO necesarias.

Usaremos dos tuberias:

- Una para enviar la peticion del cliente al servidor.
- Otra para enviar la respuesta del servidor al cliente.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 5` esta listo para subir al repositorio remoto.

### Entrega: Test 5 OK

Implementar `FifoManager` y completar la integracion principal:

- Crear las FIFO.
- Ejecutar `fork()`.
- Nombrar el proceso hijo como `cli3`.
- Nombrar el proceso padre como `serv3`.
- Lanzar el cliente en el proceso hijo.
- Lanzar el servidor en el proceso padre.
- Enviar la peticion por FIFO.
- Devolver la respuesta por FIFO.
- Mostrar en la terminal del hijo el contenido recibido.

Al terminar esta entrega, el asistente avisara al usuario de que `Test 5 OK` esta listo para subir al repositorio remoto.

## Comprobacion manual de ejecucion

Despues de `Test 5 OK`, se realizara una comprobacion manual documentada, sin crear una entrega TDD nueva, para verificar:

- Que el hijo muestra por terminal la respuesta recibida.
- Que los procesos pueden comprobarse con `ps`.
- Que aparecen los nombres `cli3` y `serv3` mientras el programa esta en ejecucion.

Esta comprobacion formara parte de la validacion final de la practica, pero no sustituye a las entregas TDD.

## Refactor 2

Realizar una limpieza final manteniendo todos los tests en verde.

Objetivos:

- Revisar comentarios.
- Revisar nombres.
- Limpiar recursos temporales.
- Comprobar que la estructura final sigue cumpliendo el enunciado.

Al terminar esta entrega, el asistente avisara al usuario de que `Refactor 2` esta listo para subir al repositorio remoto.

## Documentacion final

Al terminar la implementacion se actualizaran los ficheros obligatorios:

- `README`: manual de usuario.
- `INSTALL`: manual de instalacion.

Tambien se documentara como ejecutar los tests, como lanzar la aplicacion y como comprobar los procesos con `ps`.

## Secuencia prevista de entregas

La secuencia recomendada de commits o subidas al repositorio remoto sera:

```txt
Test 1
Test 1 OK
Test 2
Test 2 OK
Test 3
Test 3 OK
Test 4
Test 4 OK
Refactor 1
Test 5
Test 5 OK
Refactor 2
```

Cada linea de esta secuencia representa una subida independiente que realizara el usuario cuando el asistente indique que la entrega esta preparada.
