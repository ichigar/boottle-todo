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

## Lesson1. Empezando con bottle

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
Para poder usar este proyecto en otro equipo debemos añadir las dependiencias del mismo a un fichero. Lo hacemos ejecutando:

```bash
$ pip freeze > requirements.txt
```
Si copiaramos esta carpeta en otro equipo podríamos instalar las dependencias de este proyecto en el equipo destino. Después de crear el entorno virtual ejecutamos:

```bash
$ pip install -r requirements.txt
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

Vemos que se muestra en el navegador el resultado de la función `index()`

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson1
```

El tutorial continua en [lesson2](lesson2.md).