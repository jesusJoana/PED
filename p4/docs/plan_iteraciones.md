# Plan de iteraciones - Practica 4

## Objetivo general

Construir un sistema cliente-servidor sencillo en Python utilizando sockets UDS
de tipo `SOCK_STREAM`.

El cliente enviara al servidor el path absoluto de un fichero. El servidor
respondera con el contenido del fichero o con un mensaje de error si no puede
proporcionarlo. El cliente mostrara en terminal la respuesta recibida.

El servidor debera permanecer en ejecucion tras atender a un cliente y aceptar
mas conexiones. Todos los sockets se crearan dentro de `/tmp`. Los procesos
cliente y servidor deberan poder identificarse mediante `ps` con nombres que
contengan `cli4` y `serv4`.

## Archivos previstos

- `src/main.py`
- `src/server.py`
- `src/client.py`
- `tests/test_client.py`
- `tests/test_server.py`
- `tests/test_integracion.py`
- `README.txt`
- `INSTALL.txt`
- `Makefile`

Tambien se valorara crear wrappers ejecutables `cli4` y `serv4` si son necesarios
para cumplir de forma fiable el requisito de nombres visibles mediante `ps`.

## Criterio de testing

Las pruebas unitarias no mockearan sockets por defecto. Se usaran sockets UDS
reales porque forman parte del requisito tecnico principal de la practica.

La diferencia entre pruebas unitarias e integracion sera el alcance:

- Las pruebas unitarias validaran responsabilidades concretas de cliente o servidor.
- Las pruebas de integracion validaran el flujo completo entre cliente y servidor
  ejecutandolos como procesos reales.

## Criterio de refactorizacion

No se realizara una fase de refactor obligatoria en cada iteracion. Solo se hara
refactor cuando aporte una mejora clara: simplificar codigo, eliminar duplicidad,
mejorar nombres, reducir riesgo o preparar una siguiente iteracion sin cambiar
el comportamiento observable.

## Flujo por entrega

Cada iteracion se dividira en entregas separadas:

- `Test n`: solo se preparan los tests nuevos y la bateria debe quedar en rojo.
- `Test n OK`: se implementa el codigo minimo para hacer pasar los tests anteriores.
- `Refactor n`: se realiza solo si aporta una mejora clara y siempre manteniendo
  los tests en verde.

No se avanzara automaticamente de `Test n` a `Test n OK` dentro de la misma entrega.

## Iteracion 1 - Comunicacion basica UDS

### Test 1

Objetivo: introducir las primeras pruebas fallidas para validar la comunicacion
basica mediante sockets UDS.

Pruebas previstas:

- `tests/test_server.py`
  - Verificar que el servidor usa una ruta de socket dentro de `/tmp`.
  - Verificar que el servidor puede devolver el contenido de un fichero existente.
  - Verificar que el servidor devuelve un mensaje de error si el fichero no existe.
- `tests/test_client.py`
  - Verificar que el cliente exige un path absoluto.
  - Verificar que el cliente puede enviar un path y recibir una respuesta usando
    un socket UDS real controlado por la prueba.
- `tests/test_integracion.py`
  - Arrancar servidor real.
  - Ejecutar cliente real.
  - Comprobar que el cliente imprime el contenido del fichero solicitado.

Resultado esperado: tests en rojo porque todavia no existe implementacion.

### Test 1 OK

Objetivo: implementar el minimo codigo para pasar las pruebas de la iteracion 1.

Implementacion prevista:

- Crear `src/server.py` con una clase `FileServer`.
- Crear `src/client.py` con una clase `FileClient`.
- Crear `src/main.py` como punto de entrada.
- Implementar socket UDS `SOCK_STREAM`.
- Implementar envio de path y respuesta con contenido o error.
- Actualizar `Makefile` con `make test`, `make server` y `make client FILE=...`.

Resultado esperado: todos los tests de la iteracion 1 en verde.

### Refactor opcional

Objetivo: mejorar nombres, constantes y separacion de responsabilidades sin
cambiar comportamiento observable.

Refactor previsto:

- Centralizar constantes como ruta del socket y tamano de buffer.
- Revisar nombres de metodos publicos.
- Eliminar duplicidades en tests.

Resultado esperado: todos los tests siguen en verde.

## Iteracion 2 - Servidor persistente y multiples clientes

### Test 2

Objetivo: validar que el servidor no termina tras atender a un cliente.

Pruebas previstas:

- `tests/test_integracion.py`
  - Arrancar servidor real.
  - Ejecutar un primer cliente y comprobar respuesta.
  - Ejecutar un segundo cliente y comprobar respuesta.
  - Comprobar que el proceso servidor sigue vivo despues de ambos clientes.

Resultado esperado: tests en rojo si el servidor solo atiende una conexion.

### Test 2 OK

Objetivo: implementar el bucle de aceptacion de conexiones.

Implementacion prevista:

- Mantener el servidor escuchando en un bucle.
- Cerrar cada conexion cliente despues de responder.
- Permitir detener el servidor limpiamente desde las pruebas.
- Eliminar el fichero socket antiguo antes de hacer `bind` si existe.

Resultado esperado: todos los tests acumulados en verde.

### Refactor opcional

Objetivo: simplificar el ciclo de vida del servidor.

Refactor previsto:

- Aislar la atencion de una conexion en un metodo pequeno.
- Revisar cierre de sockets con context managers cuando sea posible.
- Mejorar limpieza del socket UDS en `/tmp`.

Resultado esperado: todos los tests siguen en verde.

## Iteracion 3 - Procesos `cli4` y `serv4`

### Test 3

Objetivo: comprobar que los procesos contienen las cadenas requeridas en sus
nombres al consultarlos con `ps`.

Pruebas previstas:

- `tests/test_integracion.py`
  - Arrancar servidor mediante el mecanismo definitivo.
  - Comprobar con `ps` que aparece `serv4`.
  - Ejecutar cliente mediante el mecanismo definitivo.
  - Comprobar con `ps` o con la linea de comando capturada que aparece `cli4`.

Resultado esperado: tests en rojo si los procesos solo aparecen como `python`.

### Test 3 OK

Objetivo: hacer fiable el requisito de nombres de proceso.

Implementacion prevista:

- Crear wrappers ejecutables `serv4` y `cli4`, si se aprueba su inclusion.
- Ajustar `Makefile` para lanzar servidor y cliente mediante esos wrappers.
- Mantener `src/main.py` como punto de entrada real de la aplicacion.

Resultado esperado: todos los tests acumulados en verde.

### Refactor opcional

Objetivo: dejar la ejecucion limpia y facil de explicar.

Refactor previsto:

- Revisar comandos del `Makefile`.
- Evitar argumentos duplicados.
- Documentar claramente como lanzar `serv4` y `cli4`.

Resultado esperado: todos los tests siguen en verde.

## Iteracion 4 - Documentacion final y validacion completa

### Test 4

Objetivo: validar que la practica queda ejecutable mediante `make` y documentada.

Pruebas previstas:

- Comprobar que `README.txt` existe y describe uso basico.
- Comprobar que `INSTALL.txt` existe y describe instalacion.
- Comprobar que `make test` ejecuta todas las pruebas.

Resultado esperado: tests en rojo si falta documentacion o targets.

### Test 4 OK

Objetivo: completar documentacion y comandos finales.

Implementacion prevista:

- Crear `README.txt`.
- Crear `INSTALL.txt`.
- Revisar `Makefile`.
- Ejecutar bateria completa con `make test`.

Resultado esperado: todos los tests acumulados en verde.

### Refactor opcional

Objetivo: revision final orientada a entrega.

Refactor previsto:

- Revisar claridad de mensajes de error.
- Revisar comentarios en espanol.
- Confirmar que no hay dependencias externas innecesarias.
- Confirmar que los sockets se crean exclusivamente en `/tmp`.

Resultado esperado: proyecto listo para entrega.
