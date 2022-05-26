import os
import sys
sys.path.append('models') # add the models directory to the path
sys.path.append('forms')

import bottle
from bottle import route, run, template, request, get, post, redirect, static_file, error
from config.config import DATABASE, TODO_DEFINITION
from models.todo import Todo
from forms.register import RegistrationForm
##################################################################
from forms.upload import UploadForm


@get('/upload')
def upload_file():
    form = UploadForm(request.POST)
    return template('upload', form=form)

@post('/upload')
def do_upload():
    form = UploadForm(request.POST)
    print(form.file.data)
    if form.file.data:
        filename = form.file.data.filename
        
        try:
            form.file.data.save('uploads/' + filename)
        except Exception as e:
            print(e)
            return template('upload', form=form)
        return redirect('/')
        
    
    return template('upload', form=form)
####################################################################
@get('/register')
def register():
    form = RegistrationForm(request.POST)
    return template('register', form=form)

@post('/register')
def register_process():
    form = RegistrationForm(request.POST) 
    if form.save.data and form.validate():
        form_data = {
            'username' : form.username.data,
            'email' : form.email.data,
            'password' : form.password.data,
            'accept_rules' : form.accept_rules.data,
            'historia' : form.historia.data,
            'color' : form.color.data,
            'pais' : form.pais.data
        }
        print(form_data)
        redirect('/')
    print(form.errors)
    return template('register', form=form)
        
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
