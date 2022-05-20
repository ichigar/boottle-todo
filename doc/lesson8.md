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

## Lesson 8. Desplegando con gunicorn en docker

Vamos a dar los pasos para poder desplegar nuestro proyecto con gunicorn en docker.

Hasta ahora para comprobar el funcionamiento de nuestro proyecto ejecutamos `main.py` desde el directorio raíz del proyecto y se lanza un servidor de prueba. Si queremos ejecutar en producción la aplicación deberíamos usar un servidor para aplicaciones con mejores prestaciones como `gunicorn`. Además prepararemos la aplicación para ejecutarla desde un contenedor en `docker` los que nos permitirá ejecutarla en cualquier plataforma.

Empezamos renombrando el programa principal de `main.py` a `app.py`.

```bash
$ mv main.py app.py
```

Importamos en la primera línea del archivo `app.py` la librería `bottle`.

```python
import bottle
...
```

Y creamos una instancia de la aplicación  al final del ficharo. Dicha instancia será usada por `gunicorn` al iniciarse:

```python
....
@error(404)
def error404(error):
    return static_file('404.html', root='static')

app = bottle.default_app()

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
```

Instalamos en el entorno virtual `gunicorn` y lo añadimos a nuestro `requirements.txt`:

```bash
(.venv) $ pip install gunicorn
(.venv) $ pip freeze > requirements.txt
```

Creamos en la carpeta raíz del proyecto un fichero `Dockerfile` con la siguiente configuración:

```dockerfile
FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip3 install -r requirements.txt
ADD . /app
EXPOSE 5000
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]
```

Creamos el fichero `entrypoint.sh` con la siguiente configuración:

```bash
#!/bin/bash
exec gunicorn --config /app/gunicorn_config.py app:app
```

Creamos el fichero con la configuración de `gunicorn`:

```python
bind = "0.0.0.0:5000"
workers = 4
threads = 4
timeout = 120
```

Por último creamos el fichero con la configuración de docker-compose, `docker-compose.yml`, que se encargará de ejecutar el contenedor:

```yaml
version: "3.8"

services:

  bottle-todo:
    build: .
    restart: always
    ports:
      - 5000:5000
    # expose 5000
    volumes:
      - .:/app
```

El contenedor incluye todo lo necesario para desplegar la aplicación por lo que no necesitamos ejecutarlo desde el entorno virtual.

Iniciamos el contenedor con `docker-compose up -d`.

Y accediendo en el navegador a [http://localhost:5000](http://localhost:5000) podremos ver la aplicación desplegada.

### Desplegando con traefik

Subimos la aplicación completa al servidor.

Modificamos el fichero `docker-compose.yml` para que usemos traefik:

```yaml
version: "3.8"

networks:
  web:
    external: true
  internal:
    external: false
services:

  bottle-todo:
    build: .
    restart: always
    ports:
      - 5001:5000
    volumes:
      - .:/app
    labels:
      - traefik.http.routers.apiantony.rule=Host(`todo.labfp.es`)
      - traefik.http.routers.apiantony.tls=true
      - traefik.http.routers.apiantony.tls.certresolver=lets-encrypt
      - traefik.port=5001
    networks:
      - internal
      - web
```

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson8
```

De momento este es el último archivo de la serie