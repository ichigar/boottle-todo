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
* [Lesson 11. Validación personalizada con WTForms](doc/lesson11.md)

## Lesson 11. Validación personalizada con WTForms

Cómo hemos visto, La librería para crear formularios [WTForms](https://wtforms.readthedocs.io/) incluye el objeto `validators` que contiene una serie de validadores que podemos pasar en una lista a cada uno de los campos de un formulario.

En ocasiones vamos a necesitar realizar validaciones que no están incluidas en la librería, en este tutorial vamos a ver cómo implementarlo.

### Formulario para añadir tarea

Vamos a empezar creando un formulario para añadir tareas. Lo almacenaremos en el fichero `forms/new_task.py` en una clase de nombre `NewTaskForm`.


```python
from wtforms import Form, StringField, SubmitField, validators

class NewTaskForm(Form):
    
    task = StringField('Tarea', [validators.DataRequired()], render_kw={"size" : "70", "maxlength" : "100"})
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
```

El formulario tendrá el campo de entrada de texto que lee la tarea `task` y dos botones `save` y `cancel`.

Como validador de entrada de texto vamos a usar el validador `DataRequired` que comprueba que el campo no esté vacío. Además, usando `render_kw` podemos añadir atributos a los campos de formulario, en este caso el tamaño del campo y el máximo de caracteres que puede tener.

Para poder usar el formulario modificamos la ruta `/` de la aplicación en la que se muestra el formulario para añadir una nueva tarea. En `app.py` realizamos las siguientes modificaciones:

```python
...
from forms.new_task import NewTaskForm
...
@get('/')
def index():
    rows = todo.select()
    form = NewTaskForm(request.POST)
    return template('index', rows=todo.select(), form=form)

@post('/')
def index_save():
    form = NewTaskForm(request.POST) 
    if form.save.data and form.validate():
        form_data = {
            'task' : request.POST.task,
            'status': 1
        }
        todo.insert(form_data)
        redirect('/')
    rows=todo.select()
    return template('index', rows=todo.select(), form=form)
...
```
Antes de mostrar la plantilla de la aplicación (ruta @get('/')), vamos a añadir un objeto `form` de la clase `NewTaskForm` que contiene la definición del formulario y se lo pasamos a la página principal.

Para la ruta @post('/') comprobamos si se han recibido los datos del formulario y son válidos. Si es así, los guardamos en la base de datos. En caso contrario mostramos el formulario de nuevo.

La parte de la plantilla `views/index.tpl` que muestra el formulario de nueva tarea se modifica para que incluya el formulario:

```html
% include('header.tpl', title = "TODO app")
<h1>TODO app</h1>
<p><a href="/register">Acceso al formulario de registro</a></p>
<p><b>Añadir una nueva tarea:</b></p>
<form action="/" method="POST">
    <fieldset>
        <div>    
            {{ form.task.label }}:
            {{ form.task }}
            %if form.task.errors:
            <ul class="errors">
                %for error in form.task.errors:
                    <li>{{ error }}</li>
                %end
            </ul>
            %end
        </div>
        <div>
            {{ form.save }}    
        </div>
    
    </fieldset>
</form>
...
```

Vemos que  añade el campo de entrada de texto `task` y el botón `save`. En este formulario no necesitamos el botón `cancel`.

Si accedemos a la ruta `/` de nuestra web veremos que el comportamiento es igual que en el anterior salvo que ahora no podemos añadir una tarea vacia.

### Validando que la tarea no exista

Vamos ahora a validar que al añadir una tarea esta no exista ya. Para ello no solo tendremos que definir una validación personalizada, sino que esta deberá consultar en la base de datos las tareas actualmente almacenadas para comprobar que la nueva tarea no exista ya.

El fichero `forms/new_task.py` se modifica así:

```python
from wtforms import Form, StringField, SubmitField, validators
import sys
sys.path.append('models') # add the models directory to the path
sys.path.append('config')


from models.todo import Todo
from config.config import DATABASE

todo = Todo(DATABASE)

class NewTaskForm(Form):
    
    task = StringField('Tarea', [validators.DataRequired()], render_kw={"size" : "70", "maxlength" : "100"})
    
    def validate_task(form, task):
        result = todo.get(['task'], {'task': task.data})
        if result != None:
            raise validators.ValidationError('La tarea ya existe')
    
    
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
```

Para poder crear un objeto `todo` que acceda a la base de datos debemos añadir al path las rutas a las carpetas `models` y `config`. Con ello ya podemos crear un objeto `todo` que acceda a la base de datos que utilizaremos en la función de validación.

Para añadir una nueva validación personalizada simplemente creamos un método en la clase del formulario `NewTaskForm` llamado `validate_task` que recibe como parámetro el objeto `form` y el objeto `task` que almacena la información del campo de entrada que queremos validar (en nuestro caso la tarea).

En dicho método vamos a comprobar que la tarea no exista en la base de datos. Para ello vamos a consultar en la base de datos buscando si existe una tarea cuyo nombre coincida con el leído en el formulario `todo.get(['task'], {'task': task.data})`.

En caso de no encontrar ningún resultado la consulta devuelve `None`, en caso contrario devuelve una tupla con el resultado de la consulta. Si ya existe lo que hacemos es generar una excepción de validación con el mensaje que queremos que se muestre en el formulario.

```python
raise validators.ValidationError('La tarea ya existe')
```

Si ahora accedemos a la ruta `/` de nuestra web y tratamos de añadir una tarea que ya existe se mostrará el mensaje de error.


## Recursos

* [Bottle - Web oficial del proyecto](http://bottlepy.org/)
* [Bottle - Documentación](https://bottlepy.org/docs/dev/index.html)
* [Bottle - TODO app tutorial](https://bottlepy.org/docs/dev/tutorial_app.html)
* [wtforms - WtForms crash course](https://wtforms.readthedocs.io/en/3.0.x/crash_course/)