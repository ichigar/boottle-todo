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
* [Lesson 9. Refactorizando el acceso a la base de datos](doc/lesson9.md)


## Lesson3. Dando formato con plantillas

### Las plantillas

Las plantillas permiten dar formato en HTML a los datos que nos devuelven las funciones.

Bottle incluye su propio motor de plantillas:
* Las plantillas se almacenan en archivos separados con la extensión `.tpl`. 
* Las plantillas pueden ser llamadas desde las funciones que devuelven los datos.
* Las plantillas pueden incluir texto y código en Python que se ejecutará cuando se llame a la plantilla. 
* A la plantilla se le pueden pasar parámetros, como por ejemplo el resultado de una consulta a una base de datos, que luego podrán ser formateados y presentar en la página.

### Mostrando resultados

Para que el resultado de una consulta sea presentado por una plantilla se utiliza la función `template()`. 

A la función se le pasa el nombre de la plantilla y un diccionario con los parámetros que se le pasarán a la plantilla:

```python
from bottle import route, run, debug, template
...
result = c.fetchall()
c.close()
output = template('make_table', rows=result)
return output
...
```
Importamos `template` para poder utilizarla y le pasamos como primer parámetro el nombre de la plantilla y como segundo parámetro el resultado de la consulta que se le pasará a la plantilla en la variable `rows`.

El nombre del fichero de la plantilla debe ser `make_table.tpl` y debe estar en la misma carpeta que la aplicación o en la subcarpta `views`

Creamos la subcarpeta `views` y dentro de ella creamos el fichero `make_table.tpl` con el siguiente contenido:

```html
%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Las tareas pendientes son las siguientes:</p>
<table border="1">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>
```

El motor de plantillas se encarga de interpretar en Python las líneas que empiezan por `%`

### Recibiendo datos de entrada

Las plantillas las usaremos también para recoger información de los usuarios.

Vamos a crear una plantilla que será un formulario para añadir una nueva tarea. Dentro de la carpeta `views` crearemos el fichero `new_task.tpl` con el siguiente contenido:

```html
<p>Añadir una nueva tarea a la lista:</p>
<form action="/new" method="POST">
  <input type="text" size="100" maxlength="100" name="task">
  <input type="submit" name="save" value="save">
</form>
```

En el atributo `action` de `form` indicamos que la ruta que ha de procesar los datos recibidos por el formulario es `/new` y en el atributo `method` indicamos que se trata de un formulario de tipo `POST`.

El formulario contiene un campo de entrada de texto que almacena en la variable `task` el texto que el usuario introduce en el campo de entrada y un botón que al pulsarlo envía los datos al servidor y le pasa en la variable `save` el valor `save`.

Para mostrar el formulario añadimos la ruta correspondiente al programa y la función que se debe ejecutar.:

```python
@route('/new')
def new_item_form():
    return template('new_task')
```

Con esto conseguimos que al acceder a la URL [http://localhost:8080/new](http://localhost:8080/new) se muestre el formulario.

Tenemos que añadir una nueva ruta para procesar los datos recibidos por el formulario. En el formulario hemos especificado en el atributo `action` la ruta `/new` para procesaar los datos y en el atributo `method` indicamos que se trata de un formulario de tipo `POST`.

Por defecto las rutas de Bottle son `GET` y para indicar que se trata de un formulario de tipo `POST` se le pasa al decorador de la ruta el parámetro `method='POST'`.

```python
@route('/new', method='POST')
...
```

Dentro de la función encargada de procesar los datos recibidos estos han de poder recogerse. Bottle se encarga de hacer esto en el objeto `request` que para poder utilizarlo hemos de importar:

```python
from bottle import route, run, template, request
```

La función que procesa el formulario quedaría de la forma:


```python
@route('/new', method='POST')
def new_item_save():
    if request.POST.save:  # the user clicked the `save` button
        new = request.POST.task.strip()    # get the task from the form
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
        new_id = c.lastrowid

        conn.commit()
        c.close()
        # se muestra el resultado de la operación
        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id
```

* `request.POST` es un diccionario que contiene los datos recibidos por el formulario.
  * `request.POST.save` es una cadena que contiene el valor `save` que se ha introducido en el botón de envío.
  * `request.POST.task` es una cadena que contiene el texto que el usuario ha introducido en el campo de entrada.

### Los decoradores @get y @post

Bottle incluye los decoradores @get y @post para indicar que se trata de una ruta de tipo `GET` o `POST` respectivamente. Podemos sustituir:

```python 
@route('/new)
...
@route('/new', method='POST')
...
```
Por:

```python
@get('/new')
...
@post('/new')
```

Para poder usarlos debemos importarlos:

```python
from bottle import route, run, template, request, get, post
```

### Redireccionando a otra página

En la parte del código anterior en la que procesábamos el formulario al finalizar se devuelve una plantilla con un resumen de la operación realizada. En este caso podríamos tambien querer que se muestre la página con todas las tareas. Para ello tendríamos que redireccionar la página a la ruta `/todo`. Lo podemos hacer utilizando la función `redirect` de Bottle que previamente debemos importar:

```python
...
from bottle import route, run, template, request, get, post, redirect
...
@post('/new')
def new_item_save():
    if request.POST.save:  # the user clicked the `save` button
        ...
        # se redirecciona a la página `/todo`
        return redirect('/todo')
...
```

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson3
```

### Lección siguiente

Puedes pasar a la siguiente lección ejecutando:

```bash
$ git switch lesson4
```