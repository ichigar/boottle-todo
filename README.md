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
## Tutoriales en ramas

Algunas funcionalidades extra no se incluyen en el proyecto, pero pueden ser accedas cambiando a determianadas ramas:

* `feature/auth`: autenticación básica de usuarios al acceder a una ruta
* `feature/upload-file`: subir archivos a la aplicación
* `feature/interactive-tables`: tablas interactivas con la librería de Javascript [DataTables](https://datatables.net/)

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
* [Lesson 10. Generando formularios y validación con WTForms](doc/lesson10.md)

## Tablas interactivas 

La librería de javascript [DataTables](https://datatables.net/) permite de forma sencilla dar interactividad a tablas de datos. Incluye funcionalidades como filtrado, ordenación, paginación, etc.

### Modificando las vistas

Usaremos `bootstrap` como framework css para dar estilo a las tablas.

En la web de prueba, en lugar de usar la plantilla del encabezado `header.tpl` insertamos un encabezado personalizado.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.25/css/dataTables.bootstrap5.css">
    <title>Tareas</title>
  </head>
<body>
```

Empezamos modificando la vista `views/index.tpl` añadiendo a la tabla un `id` y las etiquetas `thead` y `tbody`. En la tabla no se puede usar el atributo `colspan` ya que la librería intenta poner en concordancia los encabezados con los contenidor de la tabla.

```html
...
<div class="container">
<h1>TODO app</h1>
...
<table class="table table-striped" id="tasks">
    <thead>
    <tr>
        <th>ID</th>
        <th>Tarea</th>
        <th>Estado</th>
        <th>Editar</th>
        <th>Borrar</th>
        <th>Acciones</th>
    </tr>
    </thead>
    <tbody>
    %for row in rows:
    <tr>
    ...
    </tr>
    %end
    </tbody>
</table>
</div>
```

### Generando datos aleatorios para nuestra base de datos

Instalamos la librería `faker` para generar datos aleatorios:

```bash
$ pip install faker
```

Agregamos a `requirements.txt` la nueva dependencia:

```bash
$ pip freeze > requirements.txt
```


Utilizando la librería `Faker` generamos una lista de tareas aleatorias. Creamos el fichero `create_fake_tasks.py` en la carpeta raíz del proyecto:

```python
import random
import sys
sys.path.append('models')
from faker import Faker
from models.todo import Todo
from config.config import DATABASE

todo = Todo(DATABASE)

def create_fake_tasks(n):
    """Generate fake users."""
    generic_tasks = ['call to ', 'email to ', 'text to ', 'call from ', 'email from ', 'text from ']
    faker = Faker()
    for i in range(n):
        data = {
            'task': random.choice(generic_tasks) + faker.name(), 
            'status': random.choice([0, 1])
        }
        todo.insert(data)
        
    print(f'Added {n} fake tasks to the database.')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Pass the number of users you want to create as an argument.')
        sys.exit(1)
    create_fake_tasks(int(sys.argv[1]))
```

Si, por ejemplo queremos crear 10 tareas ejecutamos:

```bash
$ python create_fake_tasks.py 10
```

Al acceder a la ruta `/` se muestran las 10 tareas generadas.

### Insertando Javascript

Cómo el javascript solo se usara en la vista raíz lo añadimos al final del fichero `views/index.tpl` antes de cerrar el HTML:

```html
...
<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.js"></script>
</body>
</html>
```

### Ejecutando `DataTables`

A continuación del código fuente de javascript insertamos:

```html
</table>
</div>
<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/dataTables.bootstrap5.js"></script>
<script>
    $(document).ready(function () {
      $('#data').DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
        },
        columns: [
          null,
          null,
          null,
          {orderable: false, searchable: false},
          {orderable: false, searchable: false},
          {orderable: false, searchable: false},
          ],
      });
    });
</script>
</body>
</html>
```

Invocamos la librería `DataTables` para que nos muestre la tabla de tareas de forma interactiva y le pasamos los parámetros `language` y `columns` para que muestre el idioma español y las columnas `orderable` y `searchable` para que no se pueda ordenar o buscar por esas columnas. Las columnas con valor `null` indican que no se aplica ninguna restricción a las mismas.

Si ahora accedemos a la ruta `/` veremos que nuestra tabla tiene ahora nuevas herramientas que la dotan de interactividad.

![](doc/imgs/data_tables.png)
## Recursos

* [Bottle - Web oficial del proyecto](http://bottlepy.org/)
* [Bottle - Documentación](https://bottlepy.org/docs/dev/index.html)
* [Bottle - TODO app tutorial](https://bottlepy.org/docs/dev/tutorial_app.html)
* [wtforms - WtForms crash course](https://wtforms.readthedocs.io/en/3.0.x/crash_course/)