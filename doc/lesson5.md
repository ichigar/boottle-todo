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

## Lesson5. Mostrando contenido estático

Hasta ahora hemos creado rutas para mostrar páginas dinámicas, pero nuestra web también contendrá contenido estático como una página de bienvenida o una página de error; imágenes, CSS, etc.

Igual que con el contenido dinámico, cuando queremos acceder directamente o desde las plantillas a contenido estático **Bottle** ha de saber como acceder al mismo.

### La función `static_file`

Para estructurar mejor nuestro código podemos crear la carpeta `static` y usarla como base para las rutas estáticas. Si creamos en dicha carpeta un archivo `about.html` con el siguiente contenido:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/miligram.css">
    <title>Acerca de</title>
</head>
<body>
  <h1>Acerca de</h1>
  <p>Aplicación para gestión de tareas</p>
</body>
</html>
```

Y queremos acceder al mismo desde la ruta `/about` primero importamos la función `static_file` de la librería `bottle`.

```python
...
from bottle import route, run, template, request, get, post, redirect, static_file
...
```

Y añadimos la siguiente ruta al fichero `main.py`:


```python
@get('/about')
def about():
    return static_file('about.html', root='static')
```

En la que indicamos que al acceder a dicha ruta se llamara a la función `static_file()` cuyo primer parámetro es el nombre del archivo que queremos mostrar y el segundo (`root`) es la ruta de la carpeta donde se encuentra.

Si todo el contenido estático cuelga de la carpeta `static` y queremos que de manera genérica se pudiese acceder a cualquier archivo estático a partir de su ruta  lo podemos hacer añadiendo en `main.py` la siguiente ruta:

```python
...
@get("/static/<filepath:path>")
def html(filepath):
    return static_file(filepath, root = "static")
...
```

Donde:
* `filepath` es la ruta del nombre del archivo que queremos mostrar.
* `path` lo reconoce Bottle como de tipo ruta a archivo


Así, si copiamos en la carpeta `static/img` una imagen de nobre `todo.png` podemos mostrala en la página `about.html` de la siguiente forma:

```html
...
<h1>Acerca de</h1>
<p>Aplicación para gestión de tareas</p>
<img src="/static/img/todo.png" alt="Imagen TODO">
...
```

Si en la carpeta `static/css` insertamos un archivo con los estilos a aplicar también bottle lo serviría al ser insertado en cualquier página o plantilla.

```html
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/miligram.css">
    <title>Acerca de</title>
</head>
...
```

### Mostrando el favicon

Todos los navegadores buscan en la raíz del sitio un archivo `favicon.ico` para mostrar un icono en la pestaña del navegador. Por tanto, los navegadores solicitan cuando accedemos a [http://localhost:8080/](http://localhost:8080/) el archivo `favicon.ico` que se encuentra en la raíz del sitio.

Para poder servirlo, buscamos o generamos el `favicon.ico`que nos interese y lo guardamos en la carpeta `static`.

A continuación, en el fichero `main.py` añadimos la siguiente ruta:

```python
...
@get('/favicon.ico')
def about():
    return static_file('favicon.ico', root='static')
...
```

A partir de este momento, al acceder a cualquier página de nuestro sitio se mostrará en la pestaña del navegador dicho archivo.

### Personalizando la página de error 404

Cuando en un servidor accedemos a una ruta que no existe se suele mostrar una página de error 404.

Bottle dispone de un decorador que permite crear la ruta de error 404.

```python
@error(404)
def error404(error):
    return static_file('404.html', root='static')
```

En el caso anterior devolvemos el contenido estático `404.html` que se encuentra en la carpeta `static`. El contenido de dicha página podría ser:

```html
...
<body>
    <h1>Parece que se ha producido un error</h1>
    <h2>el servidor retorno un error 404</h2>  
    <p>En el <a href="/todo" >siguiente enlace</a> podrás acceder a la página de inicio</p> 
</body>
</html>
```

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson5
```

### Lección siguiente

Puedes pasar a la siguiente lección ejecutando:

```bash
$ git switch lesson5
```