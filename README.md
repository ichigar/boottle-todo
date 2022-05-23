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

## Lesson 7. Estructurando las plantillas

La siguiente parte del curso es la estructuración de las plantillas. Las plantillas que generan el HTML que se muestra a los usuarios tienen una parte común en la que se incluyen los elementos que se repiten en todas las páginas.

Si nos surge la necesidad de modificar algún elemento de dicha parte común nos veremos obligados a hacerlo en todas las platillas del proyecto.

El motor de plantillas de Bottle nos permite insertar en una plantilla las partes comunes que se repite en todas las páginas. Vamos a verlo con un ejemplo. Generamos en la carpeta `views` un archivo de nombre `header.tpl` con el siguiente contenido:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/miligram.css">
    <title>{{title}}</title>
</head>
<body>
```

Y otro archivo de nombre `footer.tpl` con el siguiente contenido:

```html
    <p>(c) ACME INC.</p>
  </body>
</html>
```

Y modificamos una de las plantillas existentes, `edit_task.tpl` de la siguiente forma:

```html
% include('header.tpl', title = "Editar tarea")

    <form action="/edit/{{no}}" method="POST">
      <input type="text" name="task" value="{{old[0]}}" size="100" maxlength="100">
      <select name="status">
        
        <option value="1">pendiente</option>
        <option value="0">finalizada</option>
      </select>
      <br>
      <input type="submit" name="save" value="save">
    </form>   

% include('footer.tpl')
```

* `include()` nos permite insertar una plantilla en otra plantilla 
* `{{title}}` es una variable que se sustituye por el valor que le asignemos en la plantilla `header.tpl` y, por tanto, podemos pasar parámetros a las plantillas

Si accedemos, por ejemplo, a la página `http://localhost:8080/edit/1` y miramos su código fuente veremos que se ha insertado en la plantilla `edit_task.tpl` el contenido de `header.tpl` y `footer.tpl`.

Ya sólo nos resta hacer los mismos cambios en todas las plantillas.

### Archivos de la lección

Puedes obtener los archivos de la lección ejecutando:

```bash
$ git clone https://github.com/ichigar/bottle-todo.git
$ cd bottle-todo
$ git switch lesson7
```

### Lección siguiente

Puedes pasar a la siguiente lección ejecutando:

```bash
$ git switch lesson8
```
