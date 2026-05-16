# Plan de Iteraciones

Proyecto: sistema cliente-servidor mediante sockets TCP.

- Carpeta de trabajo: `examen_ordinaria`
- Lenguaje: Python
- Testing: `unittest`
- Ejecucion: `make`
- Entrada principal: `src/main.py`

## Criterio de Pruebas Unitarias con Sockets

De acuerdo con el contrato actualizado, en este ejercicio las pruebas unitarias del cliente y del servidor pueden usar sockets TCP reales.

Esto significa que:

- no se usaran mocks de `socket`;
- el socket TCP se considera parte de la unidad probada cuando estamos probando cliente o servidor;
- los tests unitarios podran crear sockets reales, conectar, enviar y recibir datos;
- para evitar bloqueos se usaran timeouts, puertos de prueba y limites de conexiones;
- la diferencia con integracion estara en el alcance: unitario prueba una clase concreta, integracion prueba el flujo completo entre cliente y servidor reales.

## Objetivo General

Implementar un servidor TCP continuo y un cliente TCP que se comunican usando mensajes de texto codificados en UTF-8.

El servidor debe:

- escuchar conexiones TCP en el puerto definido por contrato;
- aceptar conexiones indefinidamente;
- recibir un mensaje de cada cliente;
- calcular la respuesta;
- enviarla por la misma conexion;
- cerrar la conexion con ese cliente;
- continuar esperando nuevos clientes;
- imprimir en error estandar la IP del cliente y el mensaje recibido.

El cliente debe:

- preguntar al usuario la direccion completa del servidor;
- conectarse por TCP;
- enviar un minimo de 3 mensajes;
- imprimir en salida estandar las respuestas recibidas;
- informar si no consigue conectar;
- terminar tras el ultimo mensaje.

## Iteracion 1: Protocolo de Mensajes

### Entrega: Test 1 Unitario

Objetivo:

Definir mediante pruebas la logica de interpretacion de mensajes del servidor, sin usar todavia sockets TCP.

Archivo de pruebas previsto:

- `tests/test_server.py`

Pruebas previstas:

- Un mensaje de un caracter y una frase devuelve el numero de apariciones.

```text
m:combinaciones momentaneas de palabras -> m:3
```

- Un mensaje con varios caracteres separados por comas devuelve el conteo de cada uno respetando el orden recibido.

```text
m,e,z:Combinaciones momentaneas de palabras -> m:3,e:4,z:0
```

- Un mensaje sin separador `:` devuelve `ERROR`.
- Un mensaje con lista de caracteres vacia devuelve `ERROR`.
- Un mensaje con algun elemento que no sea un unico caracter devuelve `ERROR`.

Estado esperado:

Las pruebas deben fallar porque la implementacion aun no existe.

### Entrega: Test 1 OK

Objetivo:

Implementar la minima logica necesaria para que pasen las pruebas del protocolo.

Archivos previstos:

- `src/protocol.py`
- `tests/test_server.py`

Implementacion prevista:

- Crear una clase `MessageProcessor`.
- Implementar un metodo `process(message)` que devuelva la respuesta del servidor.
- Validar formato.
- Separar caracteres y frase.
- Contar apariciones exactas de cada caracter en la frase.
- Devolver `ERROR` ante cualquier mensaje no reconocido.

### Refactor

No se planifica refactor obligatorio en esta iteracion.

Solo se hara si `process(message)` queda confuso por mezclar demasiada validacion con el conteo. En ese caso se extraera un metodo privado sencillo para parsear la lista de caracteres.

## Iteracion 2: Servidor TCP Unitario con Sockets Reales

### Entrega: Test 2 Unitario

Objetivo:

Definir mediante pruebas la clase servidor usando sockets TCP reales como parte de la unidad bajo prueba.

Archivo de pruebas previsto:

- `tests/test_server.py`

Pruebas previstas:

- El servidor usa por defecto host `127.0.0.1`.
- El servidor usa por defecto el puerto `16063`, salvo que el enunciado o contrato indique otro valor.
- El servidor responde correctamente a un mensaje valido.
- El servidor devuelve `ERROR` ante un mensaje invalido.
- El servidor puede escuchar en un puerto de prueba.
- El servidor acepta una conexion TCP real.
- El servidor recibe un mensaje codificado en UTF-8.
- El servidor envia la respuesta por la misma conexion TCP.
- El servidor cierra la conexion con ese cliente tras responder.

Condiciones de prueba:

- Se usara un puerto libre o puerto de prueba.
- Se usaran timeouts para evitar bloqueos.
- El servidor se ejecutara con un limite de conexiones durante el test.

Estado esperado:

Las pruebas deben fallar porque la clase servidor aun no existe.

### Entrega: Test 2 OK

Objetivo:

Implementar la clase servidor con sockets TCP reales, limitada a lo exigido por los tests unitarios.

Archivos previstos:

- `src/server.py`
- `src/protocol.py`
- `tests/test_server.py`

Implementacion prevista:

- Crear una clase `TCPServer`.
- Definir host y puerto por defecto en el constructor.
- Implementar un metodo `handle_message(message)` que delegue en `MessageProcessor`.
- Implementar escucha TCP mediante `bind`, `listen` y `accept`.
- Implementar recepcion y envio usando UTF-8.
- Permitir limitar el numero de conexiones en tests para no bloquear.
- Cerrar la conexion del cliente tras responder.

### Refactor

Si se hara refactor en esta iteracion si el metodo principal del servidor queda demasiado largo.

Motivo:

En esta iteracion el servidor ya mezcla socket, recepcion, respuesta y cierre de conexion. Si el codigo queda poco legible, conviene separar responsabilidades.

Refactor previsto si es necesario:

- Extraer `handle_client(connection, address)`.
- Mantener `handle_message(message)` como metodo de logica pura.

## Iteracion 3: Cliente TCP Unitario con Sockets Reales

### Entrega: Test 3 Unitario

Objetivo:

Definir mediante pruebas la clase cliente usando sockets TCP reales como parte de la unidad bajo prueba.

Archivo de pruebas previsto:

- `tests/test_client.py`

Pruebas previstas:

- El cliente usa por defecto host `127.0.0.1`.
- El cliente usa por defecto el puerto `16063`.
- El cliente dispone de un minimo de 3 mensajes por defecto para enviar al servidor.
- El cliente gestiona errores de conexion devolviendo o mostrando una condicion de error controlada.
- El cliente abre una conexion TCP real contra un servidor de prueba.
- El cliente envia mensajes codificados en UTF-8.
- El cliente recibe respuestas codificadas en UTF-8.
- El cliente cierra correctamente la conexion tras cada mensaje.

Condiciones de prueba:

- El test podra levantar un servidor auxiliar minimo usando `socket`.
- No se usaran mocks de sockets.
- Se usaran timeouts para evitar bloqueos.

Estado esperado:

Las pruebas deben fallar porque la clase cliente aun no existe.

### Entrega: Test 3 OK

Objetivo:

Implementar la clase cliente con sockets TCP reales.

Archivos previstos:

- `src/client.py`
- `tests/test_client.py`

Implementacion prevista:

- Crear una clase `TCPClient`.
- Definir host y puerto por defecto en el constructor.
- Definir una lista de al menos 3 mensajes por defecto.
- Preparar metodos para enviar un mensaje y varios mensajes.
- Abrir una conexion TCP real para enviar cada mensaje.
- Codificar mensajes en UTF-8.
- Recibir respuestas en UTF-8.
- Cerrar la conexion correctamente.
- Encapsular la gestion basica de errores de conexion.

### Refactor

No se planifica refactor obligatorio en esta iteracion.

Solo se hara si la gestion de conexion, envio, recepcion y errores queda mezclada de forma poco clara.

## Iteracion 4: Integracion Cliente-Servidor

### Entrega: Test 4 Integracion

Objetivo:

Comprobar que el cliente real y el servidor real colaboran correctamente en el flujo extremo a extremo.

Archivo de pruebas previsto:

- `tests/test_integracion.py`

Pruebas previstas:

- Levantar una instancia real de `TCPServer` en un hilo usando un puerto de prueba.
- Conectar una instancia real de `TCPClient` al servidor.
- Enviar:

```text
m:combinaciones momentaneas de palabras
```

- Recibir:

```text
m:3
```

- Enviar:

```text
m,e,z:Combinaciones momentaneas de palabras
```

- Recibir:

```text
m:3,e:4,z:0
```

- Enviar un mensaje invalido.
- Recibir:

```text
ERROR
```

Estado esperado:

Las pruebas deben fallar hasta que cliente y servidor funcionen juntos en el flujo completo.

### Entrega: Test 4 Integracion OK

Objetivo:

Ajustar cliente y servidor para que el flujo extremo a extremo quede validado.

Archivos previstos:

- `src/server.py`
- `src/client.py`
- `src/main.py`
- `tests/test_integracion.py`

Implementacion prevista:

- Confirmar que `TCPServer` y `TCPClient` usan el mismo protocolo.
- Confirmar que el servidor puede atender varias conexiones sucesivas.
- Confirmar que el cliente puede enviar varios mensajes y recoger varias respuestas.
- Mantener limites de conexiones en tests para evitar bloqueos.
- Preparar `src/main.py` como punto de entrada comun.

### Refactor

No se planifica refactor obligatorio en esta iteracion.

Se hara solo si la integracion revela duplicacion o mezcla innecesaria entre cliente, servidor y `main.py`.

Refactor previsto si es necesario:

- Ajustar responsabilidades entre `TCPServer`, `TCPClient` y `main.py`.

## Iteracion 5: Entrega `servidor`

### Entrega: servidor

Objetivo:

Dejar operativo el servidor requerido por el enunciado.

Validacion prevista:

- Ejecutar `make server`.
- Comprobar que el servidor queda escuchando de forma continua.
- Comprobar que acepta conexiones sucesivas.
- Comprobar que responde y cierra cada conexion cliente.

Archivos previstos:

- `src/main.py`
- `src/server.py`
- `Makefile`

### Aviso de etiqueta

Al terminar esta iteracion, si el servidor queda implementado y validado, se debe crear la etiqueta:

```text
servidor
```

Yo avisare explicitamente antes de pasar a la siguiente iteracion.

### Refactor

No se planifica refactor especifico.

Solo se ajustara el `Makefile` si el comando existente no encaja con la ejecucion real del servidor.

## Iteracion 6: Entrega `cliente`

### Entrega: cliente

Objetivo:

Dejar operativo un cliente que envie un minimo de 3 mensajes al servidor y termine correctamente.

Mensajes propuestos:

- `m:combinaciones momentaneas de palabras`
- `m,e,z:Combinaciones momentaneas de palabras`
- `mensaje incorrecto`

Salida esperada:

- `m:3`
- `m:3,e:4,z:0`
- `ERROR`

Archivos previstos:

- `src/client.py`
- `src/main.py`
- `Makefile`

### Aviso de etiqueta

Al terminar esta iteracion, si el cliente automatico queda implementado y validado, se debe crear la etiqueta:

```text
cliente
```

Yo avisare explicitamente antes de pasar a la siguiente iteracion.

### Refactor

No se planifica refactor especifico.

La prioridad en esta entrega es que el cliente cumpla el comportamiento pedido y que imprima por salida estandar las respuestas recibidas.

## Iteracion 7: Entrega `Servidor modificado`

### Entrega: Test 7 Unitario o Integracion

Objetivo:

Definir mediante prueba que el servidor imprime en error estandar una linea por cada conexion recibida.

Archivo de pruebas previsto:

- `tests/test_server.py` o `tests/test_integracion.py`

Pruebas previstas:

- Simular o ejecutar una conexion de cliente.
- Capturar error estandar.
- Verificar que se imprime la direccion IP del cliente.
- Verificar que se imprime el mensaje recibido.

### Entrega: Servidor modificado OK

Objetivo:

Modificar el servidor para registrar cada conexion recibida.

Archivos previstos:

- `src/server.py`

Implementacion prevista:

- Al recibir una conexion, obtener la IP desde `address[0]`.
- Al recibir el mensaje, imprimir en `sys.stderr` una linea con IP y mensaje.
- Despues responder normalmente al cliente.
- Cerrar la conexion del cliente.

### Aviso de etiqueta

Al terminar esta iteracion, si el servidor modificado queda implementado y validado, se debe crear la etiqueta:

```text
Servidor modificado
```

Yo avisare explicitamente antes de pasar a la siguiente iteracion.

### Refactor

Si se hara refactor si el logging queda mezclado de forma poco clara con la gestion de sockets.

Motivo:

El logging es una responsabilidad distinta de calcular respuestas y manejar la conexion. Un metodo pequeno mejora legibilidad y facilita pruebas.

Refactor previsto si es necesario:

- Extraer `log_connection(client_ip, message)`.

## Iteracion 8: Entrega `Cliente modificado`

### Entrega: Test 8 Unitario

Objetivo:

Definir mediante pruebas el parseo de la direccion completa del servidor y la gestion de errores de conexion.

Archivo de pruebas previsto:

- `tests/test_client.py`

Pruebas previstas:

- La direccion `127.0.0.1:16063` se interpreta como host `127.0.0.1` y puerto `16063`.
- Una direccion sin puerto se considera invalida.
- Una direccion con puerto no numerico se considera invalida.
- Si el cliente no consigue conectar, devuelve o imprime un error controlado.

### Entrega: Cliente modificado OK

Objetivo:

Modificar el cliente para que pregunte al usuario la direccion completa del servidor.

Archivos previstos:

- `src/client.py`
- `src/main.py`
- `tests/test_client.py`

Implementacion prevista:

- Preguntar:

```text
Direccion completa del servidor (host:puerto):
```

- Parsear la direccion introducida.
- Crear el cliente con ese host y ese puerto.
- Enviar los 3 mensajes previstos.
- Imprimir las respuestas recibidas.
- Si no se puede conectar, imprimir un error claro.

### Aviso de etiqueta

Al terminar esta iteracion, si el cliente modificado queda implementado y validado, se debe crear la etiqueta:

```text
Cliente modificado
```

Yo avisare explicitamente al cerrar la entrega final.

### Refactor

Si se hara refactor si la interaccion por teclado queda mezclada con la clase de comunicacion TCP.

Motivo:

La clase `TCPClient` debe encargarse de conectarse, enviar y recibir. La entrada por teclado y la impresion pertenecen mejor a `main.py`. Esta separacion hace que las pruebas del cliente sean mas simples.

Refactor previsto si es necesario:

- Extraer `parse_server_address(address_text)`.
- Mantener la pregunta al usuario en `main.py`.
- Mantener `TCPClient` centrado en sockets.

## Documentacion Final

### Entrega final de documentacion

Objetivo:

Completar la documentacion obligatoria del contrato.

Archivos previstos:

- `README.txt`
- `INSTALL.txt`

Contenido previsto de `README.txt`:

- Descripcion general.
- Funcionamiento del servidor.
- Funcionamiento del cliente.
- Formato de mensajes.
- Ejemplos de uso.

Contenido previsto de `INSTALL.txt`:

- Requisitos.
- Creacion del entorno virtual.
- Instalacion.
- Ejecucion de tests.
- Ejecucion del servidor.
- Ejecucion del cliente.

### Refactor

No aplica como refactor de codigo.

Solo se revisaran los comandos del `Makefile` para que coincidan con la documentacion final.

## Resumen de Refactors Realmente Previstos

No se hara refactor en todas las iteraciones.

Los refactors que considero realmente utiles son:

1. Iteracion 2, si el servidor TCP queda demasiado largo: extraer `handle_client(connection, address)`.
2. Iteracion 3, si el cliente mezcla conexion, envio, recepcion y errores de forma poco clara: separar metodos pequenos dentro de `TCPClient`.
3. Iteracion 7, si el registro en error estandar ensucia el manejo de conexiones: extraer `log_connection(client_ip, message)`.
4. Iteracion 8, si el cliente mezcla entrada por teclado con comunicacion TCP: extraer `parse_server_address(address_text)` y dejar la interaccion en `main.py`.

El resto de iteraciones se mantendran sin refactor salvo que el codigo quede claramente menos legible de lo esperado.

## Resumen de Etiquetas

Durante el desarrollo avisare en estos cuatro momentos:

- Tras completar y validar la iteracion 5: crear etiqueta `servidor`.
- Tras completar y validar la iteracion 6: crear etiqueta `cliente`.
- Tras completar y validar la iteracion 7: crear etiqueta `Servidor modificado`.
- Tras completar y validar la iteracion 8: crear etiqueta `Cliente modificado`.
