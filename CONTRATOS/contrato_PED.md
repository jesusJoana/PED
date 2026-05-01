## Implementación con TDD

Implemente una o varias clases que genere los mensajes y sus respuestas adecuadas (tanto de la parte cliente como de la parte servidor) definidos en la especificación de requisitos, utilizando la metodología **TDD (Test-Driven Development, Desarrollo dirigido por pruebas)**.

Para la valoración de la práctica se asignará a las diferentes entregas realizadas en el repositorio, con las siguientes condiciones:

---

### Regla general de entregas y subidas al repositorio remoto

- Cada entrega definida en el plan de iteraciones deberá realizarse como una subida independiente al repositorio remoto.
- No se deberán agrupar varias entregas en una única subida.
- Cada subida deberá corresponderse con un estado concreto del desarrollo y con un mensaje de entrega claro.
- En cada iteración TDD habrá, como mínimo, dos subidas:
  - Una subida para la entrega **"Test n"**, donde se añade un conjunto mínimo de tests nuevos que demuestra el comportamiento planificado para esa iteración y que todavía falla.
  - Una subida para la entrega **"Test n OK"**, donde se implementa el código mínimo necesario para que esos tests pasen.
- Las entregas de tipo **"Refactor n"** también deberán subirse de forma independiente.
- Antes de cada subida, se deberá comprobar el estado de los tests correspondiente a la entrega:
  - En una entrega **"Test n"**, deben pasar los tests acumulados anteriores y deben fallar únicamente los tests nuevos añadidos en esa entrega.
  - En una entrega **"Test n OK"**, deben pasar todos los tests acumulados.
  - En una entrega **"Refactor n"**, deben pasar todos los tests y no deben haberse añadido nuevos casos de prueba.
- El asistente deberá recordar esta regla durante la implementación y avisar cuando una entrega esté lista para ser subida al repositorio remoto.
- El asistente nunca realizará la entrega al directorio. Siempre las entregas serán realizadas por el usuario tras informar la disponibilidad de la entrega el asistente.

---

### a) Entregas "Test n"

- Deberán contener un conjunto mínimo de casos de prueba relacionados con el comportamiento funcional planificado para esa iteración.
- Los tests nuevos de la entrega deberán ser los únicos que no funcionen en dicha entrega.
- Deberán subirse al repositorio remoto antes de implementar la solución del test.
- Es necesario que los casos de prueba de las diferentes entregas sean **funcionalmente distintos**.
- Cada caso de prueba correctamente ejecutado y adecuado a los requisitos del enunciado sumará **0.2 puntos**.
- Se pueden escribir todos los casos de prueba que se estimen oportunos (**máximo 1 punto**).

---

### b) Entregas "Test n OK"

- Deberán hacerse funcionar los casos de prueba que fallaban en la entrega anterior.
- Deberán subirse al repositorio remoto en una subida distinta a la entrega **"Test n"** correspondiente.
- Cada una de estas entregas sumará **0.2 puntos** si todos los casos de prueba acumulados funcionan.
- (**Máximo 1 punto**).

---

### c) Entregas "Refactor n"

- Deberán contener una recodificación (**refactoring**) del código.
- Se diferenciarán de la entrega anterior **solo en la recodificación**, no en los casos de prueba (que deberán ser los mismos).
- Deberán subirse al repositorio remoto como una entrega independiente.
- Sumará **0.2 puntos** si todos los casos de prueba funcionan.
- (**Máximo 0.4 puntos**).

---

### d) Características del código implementado

- Todo el código y los test deberán estar comentados brevemente para que se entienda que hace cada una de las funciones y cada uno de los test.
- El estilo de programación deberá adecuarse a un nivel medio de tal forma que se evitarán lineas de código complejo de interpretación o entendimiento.

---
### e) Características de la aplicación a desarrollar

- Se definirán en el momento en el que te pide apoyo en la implementación del código y de la definición de las iteraciones necesarias.

--- 

### f) Entrega de contenido
En el directorio de la práctica (dentro del repositorio) deberá figurar el siguiente material:
- Manual de usuario (en un fichero de texto simple llamado README)
- Manual de instalación (en un fichero de texto simple llamado INSTALL)

---
