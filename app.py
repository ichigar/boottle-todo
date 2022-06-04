import os
import sys
sys.path.append('models') # add the models directory to the path
sys.path.append('forms')

import bottle
from bottle import route, run, template, request, get, post, redirect, static_file, error
from config.config import DATABASE, TODO_DEFINITION
from models.todo import Todo

from forms.new_task import NewTaskForm
from forms.edit_task import EditTaskForm

        
todo = Todo(DATABASE) # Creamos objeto vinculado a la base de datos

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


@get('/edit/<no:int>')
def edit_item_form(no):
    # Obtenemos la tarea a editar
    fields = ['task', 'status']
    where = {'id': no}
    cur_data = todo.get(fields, where)  
    
    # Creamos formulario y le pasamos los valores actuales de la tarea
    form = EditTaskForm(request.POST)
    form.task.data = cur_data[0]
    form.status.data = True if cur_data[1] == 0 else False
    
    return template('edit_task', form=form, no=no)
    

@post('/edit/<no:int>')
def edit_item(no):
    form = EditTaskForm(request.POST)
    if form.save.data and form.validate():
        status = 0 if form.status.data else 1
        data = {
            #'task': request.forms.getunicode('task'),    # Forma alternativa
            'task': request.POST.task,
            #'task': form.task.data,                      # Forma alternativa
            'status': status,
        }

        where = {'id': no}
        
        todo.update(data, where)
        
    return redirect('/')

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

@get('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='static')

@get('/about')
def about():
    return static_file('about.html', root='static') 

@get("/static/<filepath:path>")
def html(filepath):
    return static_file(filepath, root = "static")

@error(404)
def error404(error):
    return static_file('404.html', root='static')

app = bottle.default_app()

if __name__ == '__main__':
    if not os.path.exists(DATABASE) or os.path.getsize(DATABASE) == 0:
        
        todo.create(TODO_DEFINITION)
        
    run(host='localhost', port=8080, debug=True, reloader=True)
