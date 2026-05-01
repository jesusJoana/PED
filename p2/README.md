# Cliente-servidor de ficheros con pipes UNIX

Este proyecto implementa un sistema cliente-servidor en Python usando procesos UNIX y tuberias.

El programa principal es `src/main.py`. Al ejecutarlo, crea un proceso hijo con `fork()`:

- El proceso padre actua como servidor y se llama `serv2`.
- El proceso hijo actua como cliente y se llama `cli2`.
- El hijo pide al padre el contenido de un fichero `.txt`.
- El padre lee el fichero y devuelve su contenido al hijo usando una tuberia.
- El hijo muestra en pantalla la respuesta recibida.

## Estructura

```text
p2/
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
├── docs/
│   └── iteraciones.md
├── prueba.txt
├── requirements.txt
├── Makefile
├── README.md
└── INSTALL
```

## Instalacion

Para crear el entorno virtual e instalar dependencias:

```bash
make install
```

La dependencia principal es `setproctitle`, usada para que los procesos aparezcan como `cli2` y `serv2` al ejecutar `ps`.

## Ejecutar pruebas

```bash
make test
```

Las pruebas usan `unittest` y cubren:

- validacion de argumentos,
- lectura de ficheros,
- comunicacion por pipes,
- ejecucion con `fork()`,
- nombres de proceso `cli2` y `serv2`.

## Ejecutar el programa

Con el fichero de prueba incluido:

```bash
make run
```

Con otro fichero que exista:

```bash
make run FILE=prueba.txt
```

Tambien se puede ejecutar directamente:

```bash
venv/bin/python src/main.py prueba.txt
```

Si se quiere usar otro fichero, hay que cambiar `prueba.txt` por una ruta real que exista en el sistema.

## Comprobar nombres de proceso

Como el programa termina rapido, se puede usar la variable `PED_PROCESS_SLEEP` para pausar unos segundos ambos procesos y verlos con `ps`:

```bash
PED_PROCESS_SLEEP=2 venv/bin/python src/main.py prueba.txt & pid=$!
sleep 0.4
ps -o pid,ppid,comm,args -p $pid --ppid $pid
wait $pid
```

La salida debe mostrar algo parecido a:

```text
PID    PPID COMMAND  COMMAND
8461   8456 serv2    serv2
8463   8461 cli2     cli2
```

## Limpieza

Para borrar caches de Python:

```bash
make clean
```
