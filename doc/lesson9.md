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
    def __init__(self, table_name, db_name):
        self.table_name = table_name
        self.db_name = db_name
```

Agregamos también el método protegido `_connect` que nos permitirá conectarnos a la base de datos.

```python
...
class Table(ABC):
    def __init__(self, table_name, db_name):
        self.table_name = table_name
        self.db_name = db_name

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        return conn
```

Para aplicar a la clase `todo`

### Operación C - Crear. Insertar registro en base de datos

Debemos generar una cadena de texto que contenga la sentencia SQL para insertar un registro en la tabla. La consulta debe ser de la forma:

```sql
"INSERT INTO todo (key1, key2, key3) VALUES (?,?,?)"
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

La operación U es la que nos permitirá actualizar los datos de la tabla. Para ello creamos el método `update` que recibirá un diccionario con los datos a actualizar y otro diccionario con la clave y su valor para poder localizar el registro a actualizar.

Debemos generar una consulta SQL que actualice los datos de la tabla. La consulta debe ser de la forma:

```sql
UPDATE todo SET key2 = ?, key3 = ?, key4 = ? WHERE key1 = ?
```
Y pasarle como segundo parámetro una lista o tupla con los valores que queremos insertar y como tercer parámetro el valor de la clave que se usará para localizar el registro a actualizar.

```python

```python

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

Ahora debemos reescribir la clase `Todo` para que utilice la clase abstracta `Table` y que incluya los métodos `insert`, `select`, `update` y `delete`. El resto de métodos de la clase `Todo` se pueden dejar tal cual.

```python
import sqlite3
from table import Table


class Todo(Table):

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
    
    def get_task(self, no):
        data = None
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
            data = c.fetchone()
            conn.commit()
            c.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return data
    
    def insert_task(self, task):
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("INSERT INTO todo (task, status) VALUES (?,?)", (task, 1))
            conn.commit()
            c.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()    
            return True
        
    def open_task(self, no):
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("UPDATE todo SET status = 1 WHERE id LIKE ?", (str(no),))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        finally:
            if conn:
                conn.close()    
            return True
    
    def close_task(self, no):
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("UPDATE todo SET status = 0 WHERE id LIKE ?", (str(no),))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        finally:
            if conn:
                conn.close()
            return True
```

Y hemos de modificar en `app.py` las funciones que llaman a los métodos `update()`y `delete()` dado que ahora los parámetros de los métodos son diccionarios.

```python


### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson8
```