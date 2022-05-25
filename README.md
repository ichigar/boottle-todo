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

Y modificamos `requirements.txt` para que incluya la dependencia:

```python
$ pip freeze > requirements.txt
```

## Recursos

* [Bottle - Web oficial del proyecto](http://bottlepy.org/)
* [Bottle - Documentación](https://bottlepy.org/docs/dev/index.html)
* [Bottle - TODO app tutorial](https://bottlepy.org/docs/dev/tutorial_app.html)
* [wtforms - WtForms crash course](https://wtforms.readthedocs.io/en/3.0.x/crash_course/)