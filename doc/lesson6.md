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

## Lesson 6. Organizando el código

Actualmente nuestro progrma principal incluye para cada ruta operaciones que implican enviar o recuperar valores leidos, realizar consultas a la base de datos y llamadas para mostrar plantillas.

Vamos a refactorizar un poco el código de forma que separemos las operaciones.

Empezamos creando una clase para todas las operaciones sobre la base de datos. Creamos una carpeta de nombre `models` y dentro de ellas un fichero con el mismo nombre de la tabla sobre la que se realizan las operaciones: `todo.py` y en el insertamos:

```python
import sqlite3
class Todo:
    def __init__(self, database):
        self.database = database
    
    def __connect(self):
        conn = sqlite3.connect(self.database)
        return conn

    
    def select(self):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
        data = c.fetchall()
        conn.commit()
        c.close()
        return data
```

Al constructor se le pasa el nombre de la base de datos y se encarga de almacenarlo.

El método privado `__connect()` se encargará de establecer una conexión y devolverá un objeto `conn` para manejar la base de datos. Todas las futuras operaciones con la base de datos se deberán lleva a cabo con dicho objeto.

A continuación iremos añadiendo todos los métodos para las diferentes consultas. 

El método `select()` se encarga de devolver todos los registros de la tabla. Todas las consultas seguirán el mismo esquema:

* Se crea un `cursor` a partir de la conexión. Un cursor es como una localización temporal que almacena el resultado de las consultas.
* Sobre dicho cursor se ejecuta la consulta con el método `execute()` al que se le pasa la consulta SQL.
* Se recuperan los datos de la consulta. Existen varios métodos para ello: 
    * `fetchall()` devuelve todos los registros de la consulta en forma de lista de tuplas
    * `fetchone()` devuelve el primer registro de la consulta 

* Al ser el cursor un apuntador temporal a la tabla tenemos que realizar un `commit()` sobre el objeto `conn` para que se apliquen los cambios (en este caso no es necesario porque no se modifica la tabla sino que simplemente realizamos una consulta)
* Por último cerramos la conexión.
* En este caso devolvemos el resultado de la consulta. Con el método `fetchall()` lo que se obtiene es una lista de t-uplas con todos los registros que cumplen en criterio de la  consulta.

De la misma forma añadimos el resto de métodos para cada uno de los tipos de consulta que se realizan

```python
    def get_task(self, no):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
        data = c.fetchone()
        conn.commit()
        c.close()
        return data
    
    def insert_task(self, task):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("INSERT INTO todo (task, status) VALUES (?,?)", (task, 1))
        conn.commit()
        c.close()
        return True
    
    def update(self, no, task, status):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (task, status, no))
        conn.commit()
        c.close()
        return True
    
    def delete(self, no):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("DELETE FROM todo WHERE id LIKE ?", str(no))
        conn.commit()
        c.close()
        return True
```

En el fichero `main.py` modificamos los controladores para que utilicen los métodos para el acceso a la tabla que acabamos de crear.

Ya no usaremos `sqlite3` en este fichero por lo que podemos quitarlo del `import`

Para poder usar la clase debemos importarla. Lo hacemosen la parte del principio del fichero y creamos un objeto de dicha clase que se utilizará en cada uno de los contralodores que hagan consultas:

```python
...
from config.config import DATABASE
from models.todo import Todo

todo = Todo(DATABASE) # Creamos objeto vinculado a la base de datos


@route('/todo')
...
```

Se modifican los controladores en los que se realizan consultas:

```python
def todo_list():
    return template('make_table', rows=todo.select())


@get('/new')
def new_task_form():
    return template('new_task')

@post('/new')
def new_task_save():
    if request.POST.save:  # the user clicked the `save` button
        new = request.POST.task.strip()    # get the task from the form
        
        todo.insert_task(new)

        return redirect('/todo')

@get('/edit/<no:int>')
def edit_item_form(no):
    cur_data = todo.get_task(no)  # get the current data for the item we are editing
    return template('edit_task', old=cur_data, no=no)

@post('/edit/<no:int>')
def edit_item(no):

    if request.POST.save:
        # get the values of the form
        edit = request.POST.task.strip()
        status = request.POST.status.strip()

        todo.update(no, edit, status)
        
        return redirect('/todo')

@get('/delete/<no:int>')
def delete_item_form(no):
    cur_data = todo.get_task(no)  # get the current data for the item we are editing
    return template('delete_task', old=cur_data, no=no)

@post('/delete/<no:int>')
def delete_item(no):
    if request.POST.delete:
        todo.delete(no)

    return redirect('/todo')
```

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson6
```

El tutorial continua en [lesson7](lesson7.md).