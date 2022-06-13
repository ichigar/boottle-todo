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

## Lesson 9. Refactorizando el acceso a la base de datos

En nuestra aplicación solo tenemos una tabla en la base de datos, pero si usamos una base de datos que incluya varias tablas acabaremos repitiendo el mismo código para cada tabla.

Para cumplir con el principio DRY podríamos crear una clase abstracta que permita realizar las operaciones CRUD sobre la base de datos. Las clases que creemos deben extender de esta clase  e incorporar los métodos para las consultas que no sean CRUD.

### Creando la clase abstracta 

Empezamos creando dentro de la carpeta `models` un fichero `table.py` que contendrá la clase abstracta `Table`. Datdo que vamos a trabajar con una base de datos `sqlite` importamos el módulo `sqlite3`:


```python
import sqlite3
from abc import ABC
 
class Table(ABC):
    pass
```

Si queremos que nuestra clase pueda trabajar con cualquier tabla de cualquier base de datos en el constructor hemos de pasarle el nombre de la tabla y el nombre de la base de datos.

```python
...
class Table(ABC):
    def __init__(self, db_name):
        self.db_name = db_name
        self.table_name = ""
```

Agregamos también el método protegido `_connect` que nos permitirá conectarnos a la base de datos.

```python
...
class Table(ABC):
    def __init__(self, db_name):
        self.db_name = db_name
        self.table_name = ""

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        return conn
```

Para aplicar a la clase `todo`

### Operación C - Crear. Insertar registro en base de datos

Debemos generar una cadena de texto que contenga la sentencia SQL para insertar un registro en la tabla. La consulta debe ser de la forma:

```sql
"INSERT INTO table (key1, key2, key3) VALUES (?,?,?)"
```

Y pasarle como segundo parámetro una lista o tupla con los valores que queremos insertar.

```python
...
class Todo(Table):
    ...
    def insert(self, data):
        data_keys = list(data.keys())         # ['key1', 'key2', 'key3']
        data_values = list(data.values())     # ['value1', 'value2', 'value3']
        
        query = f"INSERT INTO {self._table_name} ({', '.join(data_keys)}) VALUES ({', '.join(['?'] * len(data_values))})"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query, data_values)
            conn.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            if conn:
                conn.close()
            return True
    
```
### Operación R - Read.

La operación R es la que nos permitirá leer los datos de la tabla. Para ello creamos el método `select` que devolverá una lista de tuplas con los datos de la tabla.

```python
...
    def select(self):
        rows = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            conn.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return rows
```

### Operación U - Update.

La operación U es la que nos permitirá actualizar los datos de la tabla. 

Creamos el método `update` que recibirá un diccionario con los datos a actualizar y otro diccionario con la clave y su valor para poder localizar el registro a actualizar.

Debemos generar una consulta SQL que actualice los datos de la tabla. La consulta debe ser de la forma:

```sql
UPDATE todo SET key2 = ?, key3 = ?, key4 = ? WHERE key1 = ?
```
Y pasarle como segundo parámetro una lista o tupla con los valores que queremos insertar y como tercer parámetro el valor de la clave que se usará para localizar el registro a actualizar.


```python
    def update(self, data, where):
        data_keys = list(data.keys())
        data_values = list(data.values())
        where_key = list(where.keys())[0]        # 'key1' - nombre del campo clave
        query = f"UPDATE {self._table_name} SET {', '.join([f'{key} = ?' for key in data_keys])} WHERE {where_key} LIKE ?"
        
        values = data_values + [where[where_key]]  # añadimos a la lista de valores a insertar el valor de la clave
        values = tuple(values)        
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            conn.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return True
```

### Operación D - Delete.

La operación `D` es la que nos permite eliminar un registo completo de la base de datos  a partir de un diccionario cuya clave es el campo índice y su valor el valor a buscar. La consulta debe ser de la forma:

```sql
DELETE FROM todo WHERE key1 LIKE ?
```
Al ejecutar la consulta se pasará como segundo parámetro una tupla con el valor de la clave que se usará para localizar el registro a eliminar.

```python
    def delete(self, where):
        clave = list(where.keys())[0] 
        value = where[clave]
        where_clause = f"{clave} LIKE ?"
        query = f"DELETE FROM {self._table_name} WHERE {where_clause}"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query, (value,))
            conn.commit()
            conn.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return True
```

### Obteniendo valor de campos de un registro

Otra de las operaciones típicas de consulta que realizaremos será la de obtener el valor de uno o varios campos para un valor del índice determinado. Para ello creamos el método `get` al que pasaremos una lista con los campos que queremos obtener y un diccionario con la clave y su valor para localizar el registro.

```python
    def get(self, fields, where):
        clave = list(where.keys())[0] 
        value = where[clave]
        where_clause = f"{clave} LIKE ?"
        query = f"SELECT {', '.join(fields)} FROM {self._table_name} WHERE {where_clause}"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query, (value,))
            row = cursor.fetchone()
            conn.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return row
```

El contenido completo del fichero con la definición de la clase se puede encontrar en el fichero [table.py](../models/table.py).

### Reescribiendo clase Todo

Ahora debemos reescribir la clase `Todo` para que utilice la clase abstracta `Table`. En la misma solo debemos sobreescribir el constructor y añadir el método `create()` que usaremos en caso de necesitar crear la tabla desde 0.

```python
import sqlite3
from table import Table


class Todo(Table):
    def __init__(self, db_name):
        super().__init__(db_name)
        self._table_name = TABLE_NAME
    
    def create(self):
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute(conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)"))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        finally:
            if conn:
                conn.close()
            return True
    
```

El resto de métodos los podemos eliminar porque están implementados en la clase abstracta `Table`.

### Reescribiendo las llamadas a la base de datos en la app

También hemos de modificar en `app.py` las funciones que llaman a los métodos `get_task()`, `insert()`, `update()`y `delete()` dado que ahora los parámetros de los métodos son diccionarios. El método `select()` no se modifica porque no necesita de parámetros.

Veamos todos los casos. 

Para almacenar una nueva tarea hemos de pasar ahora los valores de la misma en un diccionario.

```python
@post('/new')
def new_task_save():
    if request.POST.save:  # the user clicked the `save` button
        data = {
            'task': request.POST.task.strip(), 
            'status': 1
        }
        todo.insert(data)

        # se muestra el resultado de la operación
        return redirect('/')
```

Para obtener los datos actuales de una tarea al editarla ahora usamos el método `get()` al que pasamos los campos en una lista y el diccionario con la clave y su valor.

```python
@get('/edit/<no:int>')
def edit_item_form(no):
    fields = ['task', 'status']
    where = {'id': no}
    cur_data = todo.get(fields, where)  # get the current data for the item we are editing
    return template('edit_task', old=cur_data, no=no)
```

Cuando los valores modificados en el formulario deban ser actualizados en la base de datos ahora se los pasamos el método `update()`en forma de diccionario y lo mismo pasa con la clave y su valor.

```python
@post('/edit/<no:int>')
def edit_item(no):
    
    if request.POST.save:
        data = {
            'task': request.POST.task.strip(), 
            'status': request.POST.status.strip()
        }
        where = {'id': no}
        
        todo.update(data, where)
        
    return redirect('/')
```

De forma similar, al borrar debemos cambiar la forma de obtener por `get` los datos actuales del registro a borrar y la forma de eliminar en la base de datos por `delete`.

```python
@get('/delete/<no:int>')
def delete_item_form(no):
    fields = ['task', 'status']
    where = {'id': no}
    cur_data = todo.get(fields, where)  # get the current data for the item we are editing
    return template('delete_task', old=cur_data, no=no)

@post('/delete/<no:int>')
def delete_item(no):
    
    if request.POST.delete:
        where = {'id': no}
        todo.delete(where)

    return redirect('/')
```

Las operaciones de `abrir` y `cerrar` una tarea son consultas de tipo `UPDATE` en las que sólo se modifica el campo `status` a 1 o 0 respectivamente para la tarea que localizamos por su clave:

```python
@post('/open/<no:int>')
def open_task(no):
    
    if request.POST.open:
        data = {
            'status': 1
        }
        where = {'id': no}
        todo.update(data, where)

    return redirect('/')

@post('/close/<no:int>')
def close_task(no):
    
    if request.POST.close:
        data = {
            'status': 0
        }
        where = {'id': no}
        todo.update(data, where)

    return redirect('/')
```

Otra modificiación que tenemos que hacer al fichero `app.py` es añadir al inicio del mismo:

```python
import sys
sys.path.append('models') # add the models directory to the path
```

Este cambio tenemos que hacerlo debido a que cuando se importe la clase `Todo` se importa desde esta la clase `Table`, pero como desde la carpeta raíz del proyecto no se sabe acceder a la carpeta `models` hemos de añadirla al `path` 

El contenido completo del archivo `app.py` se puede encontrar en el fichero [app.py](../app.py).

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson9
```

El tutorial continua en [lesson10](lesson10.md).