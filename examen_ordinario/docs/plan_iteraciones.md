# Plan de iteraciones - examen ordinario PED

## 1. Requisitos confirmados

Se implementara un sistema cliente-servidor TCP en Python, usando programacion
orientada a objetos, `unittest` y ejecucion mediante `make`.

El servidor atendera peticiones TCP en el puerto `16063` y usara mensajes de
texto codificados en UTF-8.

Formato de mensaje valido:

```text
letra1,letra2,...:<frase>
```

Respuesta esperada:

```text
letra1:n,letra2:n,...
```

Ejemplo:

```text
p,a:me gusta ped
```

Respuesta:

```text
p:1,a:1
```

El conteo es sensible a mayusculas y minusculas. Por tanto, `A` y `a` son
caracteres distintos.

Cualquier mensaje con formato no valido debera recibir:

```text
ERROR
```

## 2. Estructura prevista

```text
examen_ordinario/
├── main.py
├── README.txt
├── INSTALL.txt
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── client.py
│   ├── protocol.py
│   └── server.py
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_integracion.py
│   └── test_server.py
└── docs/
    └── plan_iteraciones.md
```

## 3. Diseno tecnico de alto nivel

### Protocolo

Archivo previsto: `src/protocol.py`.

Responsabilidad:

- Validar mensajes recibidos.
- Separar lista de letras y frase.
- Calcular la respuesta del servidor.
- Devolver `ERROR` ante mensajes invalidos.

Se separa el protocolo para que sea facil de probar y para que servidor y tests
no dupliquen logica.

### Servidor

Archivo previsto: `src/server.py`.

Clase prevista: `LetterCountServer`.

Responsabilidad:

- Escuchar por TCP en `127.0.0.1:16063` por defecto.
- Aceptar conexiones de clientes.
- Leer un mensaje UTF-8.
- Generar la respuesta usando el protocolo.
- Enviar la respuesta al cliente.
- Mantenerse ejecutandose de forma continua.

Para tests se permitira configurar host, puerto y limite de conexiones, evitando
bloqueos.

### Cliente

Archivo previsto: `src/client.py`.

Clase prevista: `LetterCountClient`.

Responsabilidad:

- Conectarse por TCP al servidor.
- Enviar mensajes UTF-8.
- Recibir respuestas.
- Imprimir las respuestas en salida estandar.
- Gestionar errores de conexion.
- En la iteracion 5, preguntar al usuario la direccion completa del servidor.

### Punto de entrada

Archivo previsto: `main.py`.

Responsabilidad:

- Ejecutar servidor con `python main.py servidor`.
- Ejecutar cliente con `python main.py cliente`.
- Mantener compatibilidad con el `Makefile` existente:
  - `make run-server`
  - `make run-client`
  - `make test`

## 4. Plan TDD por iteraciones

El desarrollo seguira obligatoriamente el ciclo TDD pragmatico definido en el
contrato:

```text
RED -> GREEN -> REFACTOR
```

Por tanto, cada iteracion tendra siempre tres entregas separadas:

1. `Test n <ambito>`:
   - Se crean las pruebas de la iteracion.
   - La funcionalidad todavia no estara implementada.
   - Las pruebas deberan quedar en rojo.

2. `Test n <ambito> OK`:
   - Se implementa el codigo minimo necesario.
   - Las pruebas de la iteracion pasan a verde.
   - Todos los tests acumulados deben seguir pasando.

3. `Refactor n <ambito>`:
   - Es obligatorio en este proyecto.
   - Se mejora la estructura interna del codigo sin cambiar comportamiento.
   - No se anaden requisitos nuevos.
   - No se modifican las pruebas salvo que exista una correccion claramente
     necesaria y se justifique.
   - Todos los tests deben seguir en verde.

No se mezclaran estas entregas. Primero se hara el estado rojo, despues el verde
y despues el refactor.

### Iteracion 1 - Servidor

Objetivo:

- Implementar el servidor TCP continuo.
- Aceptar conexiones.
- Recibir mensajes.
- Responder segun el protocolo.

Archivo de pruebas:

- `tests/test_server.py`

Pruebas previstas:

- El servidor responde correctamente a un mensaje con una letra.
- El servidor responde correctamente a un mensaje con varias letras.
- El servidor distingue mayusculas y minusculas.
- El servidor responde `ERROR` ante mensajes invalidos.
- El servidor puede atender mas de una conexion.

Entregas:

- `Test 1 Servidor`: pruebas del servidor en rojo.
- `Test 1 Servidor OK`: implementacion minima para pasar las pruebas.
- `Refactor 1 Servidor`: limpieza interna manteniendo los tests en verde.

Archivos afectados:

- `src/__init__.py`
- `src/protocol.py`
- `src/server.py`
- `tests/__init__.py`
- `tests/test_server.py`
- `main.py`

Riesgos:

- Bloqueos en sockets si no se usan timeouts.
- Conflictos de puerto si se usa siempre `16063` en tests.

Mitigacion:

- Tests con puertos dinamicos o configurables.
- Timeouts en cliente y servidor durante pruebas.
- Limite de conexiones configurable solo para entorno de test.

### Iteracion 2 - Cliente

Objetivo:

- Implementar cliente interactivo.
- Permitir que el usuario escriba mensajes.
- Enviar al menos 3 mensajes al servidor.
- Imprimir respuestas recibidas.
- Desconectar correctamente al terminar.

Archivo de pruebas:

- `tests/test_client.py`

Pruebas previstas:

- El cliente envia un mensaje y devuelve/imprime la respuesta recibida.
- El cliente puede enviar una secuencia de 3 mensajes.
- El cliente informa una condicion de error si falla la conexion.

Entregas:

- `Test 2 Cliente`: pruebas del cliente en rojo.
- `Test 2 Cliente OK`: implementacion minima para pasar las pruebas.
- `Refactor 2 Cliente`: limpieza interna manteniendo los tests en verde.

Archivos afectados:

- `src/client.py`
- `tests/test_client.py`
- `main.py`

Riesgos:

- La entrada interactiva puede dificultar los tests.

Mitigacion:

- Separar la logica de envio de mensajes de la lectura por teclado.
- En tests se usaran entradas controladas sin depender de una terminal real.

### Iteracion 3 - Integracion cliente-servidor

Objetivo:

- Comprobar comunicacion real entre cliente y servidor por TCP.
- Validar el flujo completo extremo a extremo.

Archivo de pruebas:

- `tests/test_integracion.py`

Pruebas previstas:

- Cliente y servidor reales intercambian un mensaje valido.
- Cliente y servidor reales intercambian varios mensajes.
- Cliente y servidor reales manejan un mensaje invalido con respuesta `ERROR`.

Entregas:

- `Test 3 Integracion`: pruebas de integracion en rojo.
- `Test 3 Integracion OK`: implementacion minima para dejar la integracion en verde.
- `Refactor 3 Integracion`: limpieza interna manteniendo todos los tests en verde.

Archivos afectados:

- `tests/test_integracion.py`
- Posibles ajustes pequenos en `src/client.py`, `src/server.py` o `main.py`.

Riesgos:

- Procesos o hilos de servidor que queden abiertos tras los tests.

Mitigacion:

- Servidores de prueba con limite de conexiones.
- Timeouts y cierre explicito de sockets.

### Iteracion 4 - Servidor modificado

Objetivo:

- Modificar el servidor para que imprima en error estandar una linea por cada
  conexion recibida.
- La linea debera contener la IP del cliente y el mensaje recibido.

Archivo de pruebas:

- `tests/test_server.py`

Pruebas previstas:

- El servidor escribe en `stderr` la IP del cliente.
- El servidor escribe en `stderr` el mensaje recibido.
- La respuesta al cliente sigue siendo correcta.

Entregas:

- `Test 4 Servidor`: pruebas del nuevo log en rojo.
- `Test 4 Servidor OK`: implementacion minima del log en `stderr`.
- `Refactor 4 Servidor`: limpieza interna manteniendo todos los tests en verde.

Archivos afectados:

- `src/server.py`
- `tests/test_server.py`

Riesgos:

- Mezclar salida funcional con salida de diagnostico.

Mitigacion:

- Respuestas del protocolo siempre por socket.
- Trazas de conexion siempre por `stderr`.

### Iteracion 5 - Cliente modificado

Objetivo:

- Modificar el cliente para que pregunte al usuario por la direccion completa
  del servidor.
- Imprimir un error si no consigue realizar la conexion.

Archivo de pruebas:

- `tests/test_client.py`

Pruebas previstas:

- El cliente solicita host y puerto al usuario.
- El cliente conecta usando la direccion introducida.
- El cliente imprime error si la conexion falla.

Entregas:

- `Test 5 Cliente`: pruebas del nuevo comportamiento en rojo.
- `Test 5 Cliente OK`: implementacion minima para preguntar direccion y gestionar error.
- `Refactor 5 Cliente`: limpieza interna manteniendo todos los tests en verde.

Archivos afectados:

- `src/client.py`
- `tests/test_client.py`
- Posible ajuste en `main.py`.

Riesgos:

- Ambiguedad en "direccion completa del servidor".

Decision propuesta:

- Pedir la direccion en formato `host:puerto`, por ejemplo:

```text
127.0.0.1:16063
```

Si el usuario introduce un formato incorrecto, el cliente imprimira un mensaje
de error claro y terminara.

### Iteracion 6 - Documentacion

Objetivo:

- Crear documentacion final obligatoria.

Archivos:

- `README.txt`
- `INSTALL.txt`

Contenido previsto de `README.txt`:

- Descripcion general.
- Manual de usuario.
- Instrucciones basicas de ejecucion.
- Ejemplos de uso.
- Explicacion funcional del sistema.

Contenido previsto de `INSTALL.txt`:

- Dependencias.
- Preparacion de entorno virtual.
- Instalacion.
- Comandos `make`.
- Pasos para ejecutar servidor, cliente y tests.

Entregas:

- `Test 6 Documentacion`: comprobaciones en rojo sobre existencia y contenido minimo.
- `Test 6 Documentacion OK`: documentacion minima completa.
- `Refactor 6 Documentacion`: mejora de claridad sin cambiar requisitos.

Archivos afectados:

- `README.txt`
- `INSTALL.txt`
- Posible `tests/test_documentacion.py` si se decide automatizar esta validacion.

## 5. Criterios de aceptacion finales

El proyecto se considerara terminado cuando:

- `make test` ejecute todos los tests con resultado correcto.
- `make run-server` arranque el servidor TCP en el puerto `16063`.
- `make run-client` arranque el cliente interactivo.
- El cliente permita enviar mensajes al servidor y muestre respuestas.
- El servidor responda correctamente a mensajes validos.
- El servidor responda `ERROR` a mensajes invalidos.
- El servidor registre en `stderr` IP y mensaje recibido por conexion.
- El cliente pregunte la direccion completa del servidor.
- El cliente informe errores de conexion.
- Existan `README.txt` e `INSTALL.txt`.

## 6. Confirmacion pendiente

Antes de implementar codigo, queda pendiente confirmar este plan.

Punto a confirmar especialmente:

- En iteracion 5 se propone usar el formato `host:puerto` para la direccion
  completa del servidor.
