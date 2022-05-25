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
* [Lesson 10. Generando formularios y validación con WTForms](doc/lesson10.md)

## Lesson 10. Generando formularios y validación con WTForms

La librería **WTForms** simplifica la generación del HTML de los formularios y la validación de los datos de entrada. Está incluida en los frameworks para desarrollo web más populares de Python como Flask y Django. Dada su flexibilidad es bastante sencillo utilizarla también en bottle.

En esta lección veremos como añadir un formulario de registro a nuestra aplicación y como validar los datos de entrada.

### Instalación

Cómo siempre, empezamos creando una rama en nuestro proyecto para la nueva funcionalidad

```bash
$ git switch -c feature/wtforms
```

Para poder utilizar la librería **WTForms**, debemos instalarla. En un terminal con el entorno virtual de nuestro proyecto, ejecutamos:

```bash
$ pip install wtforms
```

También vamos a necesitar la librería `email_validator` para validar el formato de los correos electrónicos.

```bash
$ pip install email_validator
```

Y modificamos `requirements.txt` para que incluya la dependencia:

```python
$ pip freeze > requirements.txt
```

Deberíamos hacer, al menos, un `commit` cada vez que hayamos completado el contenido de uno de los archivos de la rama.

```bash
$ git commit -am "requirements.txt con wtforms y email_validator"
```

## Definiendo un formulario

Empezamos creando en la carpeta raíz del proyecto una carpeta de nombre `forms` y dentro de ella un archivo `register.py`:

```python
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField , validators

class RegistrationForm(Form):
    
    username = StringField('Username', [validators.Length(min=4, max=25)], default='nombre de usuario')
    email = StringField('Email Address', [validators.InputRequired(), validators.Length(min=6, max=60), validators.Email()])
    accept_rules = BooleanField('Acepto las reglas del sitio', [validators.InputRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', 
                           message='Las contraseñas no coinciden')
        ])
    password_confirm = PasswordField('Repeat Password')
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
```

Para cada formulario que queramos añadir a nuestra aplicación creamos una clase que herede de `Form` y que contenga los campos que incluirá el formulario.

Para añadir un campo empezamos poniendo el nombre de la variable que representará el 


## Recursos

* [Bottle - Web oficial del proyecto](http://bottlepy.org/)
* [Bottle - Documentación](https://bottlepy.org/docs/dev/index.html)
* [Bottle - TODO app tutorial](https://bottlepy.org/docs/dev/tutorial_app.html)
* [wtforms - WtForms crash course](https://wtforms.readthedocs.io/en/3.0.x/crash_course/)