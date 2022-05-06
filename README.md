# Introducción a bootle

## Lesson1. Empezando con bootle

### Creando el entorno virtual de desarrollo
Para empezar a usar bottle creamos un entorno virtual de desarrollo.

En la carpeta raíz de nuestro proyecto ejecutamos:

```bash
$ python3 -m venv .venv
```

Lo activamos ejecutando:

```bash
$ source .venv/bin/activate
```

El prompt del sistema aparecerá como:

```bash
(.venv) $
```

Esto nos va a permitir empaquetar nuestra aplicación con todas sus dependencias en una carpeta.

### Instalación de bottle

Utilizando el gestor de paquetes de Python, instalamos bottle.
```bash
(.venv) $ pip install bottle       
Collecting bottle
  Using cached bottle-0.12.19-py3-none-any.whl (89 kB)
Installing collected packages: bottle
Successfully installed bottle-0.12.19
```

### Comprobación de funcionamiento

creamos en el raíz del proyecto un fichero `hello.py` con el siguiente contenido:

```python
from bottle import route, run

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
```
Para combrobar que la aplicación funciona

Ejecutamos el script

```bash
(.venv) $ python hello.py
Bottle v0.12.19 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
```

Y a continuación introducimos en el navegador la URL [http://localhost:8080/hello/world](http://localhost:8080/hello/world).

## Lesson2. Configuración inicial de la aplicación

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

Creamos en la carpeta inicial del proyecto un fichero `bootstrap.py` con el siguiente contenido:

```python
from config.create_database import create_database

if __name__ == '__main__':
    db_file = 'todo.db'
    create_database(db_file)
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

## Lesson3. Dando formato con plantillas


## Recursos

* [Bottle - Web oficial del proyecto](http://bottlepy.org/)
* [Bottle - Documentación](https://bottlepy.org/docs/dev/index.html)
* [Bottle - TODO app tutorial](https://bottlepy.org/docs/dev/tutorial_app.html)