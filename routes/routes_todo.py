
from bottle import template, request, get, post, redirect
from models.todo import Todo
from config.config import DATABASE

todo = Todo(DATABASE) # Creamos objeto vinculado a la base de datos
@get('/')
def index():
    rows=todo.select()
    return template('index', rows=todo.select())

@get('/new')
def new_task_form():
    return template('new_task')

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

@get('/edit/<no:int>')
def edit_item_form(no):
    fields = ['task', 'status']
    where = {'id': no}
    cur_data = todo.get(fields, where)  # get the current data for the item we are editing
    return template('edit_task', old=cur_data, no=no)

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



