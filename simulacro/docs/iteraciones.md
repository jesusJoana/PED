# Plan de iteraciones

## Proyecto

Sistema cliente-servidor TCP en Python.

El servidor atendera peticiones TCP en el puerto `16063` y respondera a mensajes
de texto codificados en UTF-8.

Mensajes soportados:

- `FECHA`: el servidor responde con la fecha actual del sistema.
- `HORA`: el servidor responde con la hora actual del sistema.
- Cualquier otro mensaje: el servidor responde con `ERROR`.

El cliente sera interactivo: se conectara automaticamente al servidor y quedara
esperando mensajes escritos por teclado. No podra cerrarse antes de haber
enviado al servidor un minimo configurable de mensajes, inicialmente `3`.

## Criterios generales

- Lenguaje: Python.
- Paradigma: Programacion Orientada a Objetos.
- Comunicacion: sockets TCP/IP.
- Host por defecto: `127.0.0.1`.
- Puerto por defecto: `16063`.
- Codificacion: UTF-8.
- Tests: `unittest`.
- Ejecucion: mediante `make`.
- Entrada principal: `main.py`.
- Estructura minima:
  - `src/`
  - `tests/`
  - `docs/`

## Iteracion 1: Servidor

### Objetivo

Implementar un servidor TCP continuo capaz de aceptar conexiones de clientes,
recibir mensajes UTF-8 y generar las respuestas requeridas.

### Entrega: Test 1 Servidor

Se crearan pruebas unitarias del servidor en:

- `tests/test_server.py`

Las pruebas documentaran que pertenecen a la Iteracion 1 y validaran:

- El servidor responde a `FECHA` con una fecha del sistema en formato esperado.
- El servidor responde a `HORA` con una hora del sistema en formato esperado.
- El servidor responde `ERROR` ante cualquier mensaje no reconocido.
- El servidor intercambia texto codificado en UTF-8.
- El servidor puede atender una conexion TCP real de prueba sin bloquear.

Estado esperado de esta entrega: RED.

### Entrega: Test 1 Servidor OK

Se implementara el codigo minimo necesario en:

- `src/server.py`
- `src/config.py`
- `main.py`, solo en la parte necesaria para lanzar el servidor.

Estrategia:

- Crear una clase `ServidorTCP`.
- Definir host y puerto por defecto en el constructor.
- Separar la logica de procesado de mensajes de la logica de sockets.
- Usar timeouts o limites controlados en tests para evitar bloqueos.
- Mantener el servidor real en modo continuo para ejecucion normal.
- Permitir un modo limitado para pruebas cuando sea necesario.

Estado esperado de esta entrega: GREEN.

### Entrega: Refactor 1 Servidor

Se revisara si conviene mejorar:

- nombres de metodos,
- separacion entre protocolo y socket,
- cierre ordenado de conexiones,
- eliminacion de duplicidad.

No se modificara el comportamiento observable ni se anadiran nuevas
funcionalidades. Si no hay mejora interna razonable, se indicara explicitamente.

## Iteracion 2: Cliente

### Objetivo

Implementar un cliente TCP interactivo que se conecte automaticamente al
servidor, permita escribir mensajes por teclado, imprima respuestas por salida
estandar y no permita finalizar antes de enviar un minimo configurable de
mensajes.

### Interpretacion del requisito de 3 mensajes

El cliente permanecera abierto esperando entrada interactiva del usuario.

- El usuario escribira mensajes por teclado.
- Cada mensaje normal se enviara al servidor.
- Cada respuesta del servidor se imprimira por salida estandar.
- El comando local de salida sera `SALIR`.
- `SALIR` no se enviara al servidor y no contara como mensaje.
- Si el usuario escribe `SALIR` antes de enviar el minimo de mensajes, el
  cliente mostrara un aviso y seguira abierto.
- Cuando el usuario ya haya enviado al menos `3` mensajes, `SALIR` cerrara el
  cliente correctamente.

El minimo se definira como parametro configurable, inicialmente:

- `MIN_MENSAJES_CLIENTE = 3`

### Entrega: Test 2 Cliente

Se crearan pruebas unitarias del cliente en:

- `tests/test_client.py`

Las pruebas documentaran que pertenecen a la Iteracion 2 y validaran:

- El cliente usa por defecto el host y puerto configurados.
- El cliente puede enviar un mensaje y recibir una respuesta usando TCP real.
- El cliente imprime por salida estandar las respuestas recibidas.
- El cliente no permite salir antes de enviar el minimo de mensajes.
- El cliente permite salir cuando ya se ha alcanzado el minimo.
- El minimo de mensajes es configurable.

Estado esperado de esta entrega: RED.

### Entrega: Test 2 Cliente OK

Se implementara el codigo minimo necesario en:

- `src/client.py`
- `src/config.py`
- `main.py`, en la parte necesaria para lanzar el cliente.

Estrategia:

- Crear una clase `ClienteTCP`.
- Separar el envio de un mensaje de la ejecucion interactiva completa.
- Mantener el contador de mensajes enviados correctamente.
- Tratar `SALIR` como comando local del cliente.
- Cerrar el socket correctamente al finalizar.
- Capturar errores de conexion o comunicacion y mostrarlos de forma clara.

Estado esperado de esta entrega: GREEN.

### Entrega: Refactor 2 Cliente

Se revisara si conviene mejorar:

- claridad de la gestion interactiva,
- nombres de metodos,
- separacion entre entrada/salida y comunicacion TCP,
- tratamiento de errores.

No se modificara el comportamiento observable ni se anadiran nuevas
funcionalidades. Si no hay mejora interna razonable, se indicara explicitamente.

## Iteracion 3: Integracion cliente-servidor

### Objetivo

Validar la comunicacion real entre cliente y servidor ejecutando ambos
componentes y comprobando el flujo extremo a extremo.

### Entrega: Test 3 Integracion

Se crearan pruebas de integracion en:

- `tests/test_integracion.py`

Las pruebas documentaran que pertenecen a la Iteracion 3 y validaran:

- Un cliente real puede conectarse a un servidor real.
- El flujo `FECHA` devuelve una fecha valida.
- El flujo `HORA` devuelve una hora valida.
- Un mensaje no reconocido devuelve `ERROR`.
- El cliente puede enviar al menos tres mensajes y cerrar correctamente.
- El servidor permanece disponible para aceptar conexiones durante la prueba.

Estado esperado de esta entrega: RED.

### Entrega: Test 3 Integracion OK

Se ajustara el codigo minimo necesario para que la integracion completa pase.

Archivos posiblemente afectados:

- `src/server.py`
- `src/client.py`
- `main.py`
- `Makefile`

Estrategia:

- Levantar el servidor en un proceso o hilo controlado por el test.
- Usar timeouts para evitar bloqueos.
- Cerrar recursos de forma ordenada al terminar cada prueba.
- Comprobar que todos los tests acumulados siguen en verde.

Estado esperado de esta entrega: GREEN.

### Entrega: Refactor 3 Integracion

Se revisara si conviene mejorar:

- utilidades de arranque/parada para pruebas,
- limpieza de recursos,
- organizacion de constantes,
- legibilidad de tests de integracion.

No se modificara el comportamiento observable ni se anadiran nuevas
funcionalidades. Si no hay mejora interna razonable, se indicara explicitamente.

## Iteracion 4: Documentacion

### Objetivo

Crear la documentacion final exigida por el contrato.

### Archivos

- `README.txt`
- `INSTALL.txt`

### Contenido de README.txt

Incluira:

- descripcion general del proyecto,
- explicacion funcional del sistema,
- manual de usuario,
- instrucciones basicas de ejecucion,
- ejemplos de uso del servidor,
- ejemplos de uso del cliente interactivo,
- explicacion de mensajes soportados.

### Contenido de INSTALL.txt

Incluira:

- requisitos previos,
- creacion y activacion de `venv`,
- instalacion de dependencias si las hubiera,
- comandos `make`,
- ejecucion del servidor,
- ejecucion del cliente,
- ejecucion de tests,
- pasos para poner el sistema en funcionamiento.

## Comandos previstos

El `Makefile` debera permitir, como minimo:

- ejecutar tests,
- lanzar el servidor,
- lanzar el cliente.

Comandos previstos:

```bash
make test
make run-server
make run-client
```

## Riesgos y decisiones

- El servidor real sera continuo, pero los tests necesitaran modos controlados
  para no bloquear.
- Las pruebas TCP usaran timeouts y cierre explicito de sockets.
- El comando `SALIR` sera local del cliente y no contara como mensaje enviado.
- La refactorizacion sera obligatoria como revision tras cada GREEN, pero solo
  se aplicaran cambios si aportan mejora interna real.
- No se usaran dependencias externas salvo que aparezca una necesidad clara.
