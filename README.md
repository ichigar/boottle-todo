# Introducción a bootle
## Creando el entorno virtual de desarrollo
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

## Instalación de bottle

Utilizando el gestor de paquetes de Python, instalamos bottle.
```bash
(.venv) $ pip install bottle       
Collecting bottle
  Using cached bottle-0.12.19-py3-none-any.whl (89 kB)
Installing collected packages: bottle
Successfully installed bottle-0.12.19
```

## Comprobación de funcionamiento

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