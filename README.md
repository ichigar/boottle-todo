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

## feature/auth

En esta rama se muestra un ejemplo para usar autenticación básica al acceder a una ruta.

Las modificaciones a realizar son:

```python
...
from bottle import route, run, template, request, get, post, redirect, static_file, error, auth_basic
...
def is_authenticated_user(user, password):
    if user == "ivan" and password=="daw1234":
        return True
    return False
....     

@get('/')
@auth_basic(is_authenticated_user)
def index():
    rows=todo.select()
    return template('index', rows=todo.select())
...
```

* Importar el módulo `auth_basic` de la librería `bottle`
* Crear una función `is_authenticated_user` que reciba el nombre de usuario y la contraseña
    * La función debe devolver `True` si el usuario y la contraseña son correctos, `False` en caso contrario
* Agregar a la ruta en la que queremos que nos autentiquen el decorador `@auth_basic()` pasándole como parámetro la función utilizada para validar al usuario


## Recursos

* [Bottle - Web oficial del proyecto](http://bottlepy.org/)
* [Bottle - Documentación](https://bottlepy.org/docs/dev/index.html)
* [Bottle - TODO app tutorial](https://bottlepy.org/docs/dev/tutorial_app.html)
