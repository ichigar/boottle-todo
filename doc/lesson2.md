# Introducción a bootle. TODO app.

## Antes de empezar

Este proyecto y su documentación están disponibles en [GitHub](https://github.com/ichigar/bottle-todo)

Puedes clonarlo ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
```

El proyecto se ha desarrollado paso por paso en ramas. Pasándote a la rama de cada lección, podrás ver el código fuente de cada una y la documentación:

```bash
$ cd bottle-todo
$ git switch lesson1
$ git switch lesson2
...
```

## Índice de contenidos

* [Lesson 1. Empezando con bottle](doc/lesson1.md)
* [Lesson 2. Configuración inicial](doc/lesson2.md)
* [Lesson 3. Dando formato con plantillas](doc/lesson3.md)
* [Lesson 4. Editando y borrando](doc/lesson4.md)
* [Lesson 5. Mostrando contenido estático](doc/lesson5.md)
* [Lesson 6. Organizando el código](doc/lesson6.md)
* [Lesson 7. Estructurando las plantillas](doc/lesson7.md)
* [Lesson 8. Desplegando con gunicorn y docker](doc/lesson8.md)

## Lesson 2. Configuración inicial

### Creando la base de datos
Empezamos creando la base de datos. Para ello creamos en la subcarpeta `config` un fichero con el nombre `create_database.py` con el siguiente contenido:

```python
import sqlite3
def create_database(db_file):
    conn = sqlite3.connect(db_file) # Warning: This file is created in the current directory
    conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Read A-byte-of-python to get a good introduction into Python',0)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Visit the Python website',1)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Test various editors for and check the syntax highlighting',1)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Choose your favorite WSGI-Framework',0)")
    conn.commit()
```
Creamos en la carpeta `config`también un fichero `config.py`en el que iremos almacenando los parámetros de configuración de la aplicación. De momento guardaremos el nombre de la base de datas en la variable `DATABASE`:

```python
DATABASE = 'todo.db'
```
Creamos en la carpeta inicial del proyecto un fichero `bootstrap.py` con el siguiente contenido:

```python
from config.create_database import create_database
from config.config import DATABASE

if __name__ == '__main__':
    create_database(DATABASE)
```

Solo se debería ejecutar una vez y es el encargado de crear la base de datos e insertar en la misma los datos iniciales.

lo ejecutamos:

```bash
(.venv) $ python bootstrap.py
```

el fichero `hello.py` ya no lo necesitamos, así que lo podemos eliminar:

```bash
(.venv) $ rm hello.py
```

La estructura actual de nuestro proyecto debería ser:

```bash
(.venv) $ tree             
.
├── bootstrap.py
├── config
│   ├── config.py
│   └── create_database.py
└── README.md
```

### Configuración de la aplicación

Nuestra aplicación será una aplicación web que nos permita gestionar una lista de tareas.

El ejecutable de entrada a la misma será `main.py`. Empezaremos con el siguiente contenido para el mismo:

```python
import sqlite3
from bottle import route, run

'

@route('/todo')
def todo_list():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    return str(result)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
```

* `@route` es un decorador que nos permite definir una ruta para una función.
* `/todo` es la ruta que se va a usar para acceder a la lista de tareas.
* `def todo_list()` es la función que se va a ejecutar cuando se accede a la ruta.
* `debug=True` es un parámetro que nos permite activar el modo depuración. Se mostrará información extra cuando se produzca un error.
* `reloader=True` es un parámetro que nos permite activar el modo de recarga. Se actualizará la página cuando se produzca un cambio en el código. Esto nos evita tener que interrumpir el servidor y volver a ejecutarlo cada vez que hagamos un cambio en el código.

Para comprobar el funcionamiento de la aplicación solo necesitamos ejecutar el script

```bash
(.venv) $ python main.py
```

Y en el navegador accederemos a la URL [http://localhost:8080/todo](http://localhost:8080/todo).

Con ello obtenemos el resultado de ejecutar la función `todo_list()`. Podemos vincular más rutas a una misma función, para ello simplemente añadimos decoradores antes de la misma:

```python
@route('/todo')
@route('/my_todo_list')
def todo_list():
    ...
```
Si en el navegador accederemos a la URL [http://localhost:8080/my_todo_list](http://localhost:8080/my_todo_list) obtenemos el mismo resultado

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson2
```

El tutorial continua en [lesson3](lesson3.md).