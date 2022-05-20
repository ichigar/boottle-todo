import bottle
from bottle import route, run, template, request, get, post, redirect, static_file, error, response
from config.config import DATABASE
from models.todo import Todo


todo = Todo(DATABASE) # Creamos objeto vinculado a la base de datos

@get('/')
def index():
    rows=todo.select()
    return template('index', rows=todo.select())

@route('/todo')
@route('/my_todo_list')
def todo_list():
    return template('make_table', rows=todo.select())


@get('/new')
def new_task_form():
    return template('new_task')

@post('/new')
def new_task_save():
    if request.POST.save:  # the user clicked the `save` button
        new = request.POST.task.strip()    # get the task from the form
        todo.insert_task(new)

        # se muestra el resultado de la operación
        return redirect('/')

@get('/edit/<no:int>')
def edit_item_form(no):
    cur_data = todo.get_task(no)  # get the current data for the item we are editing
    return template('edit_task', old=cur_data, no=no)

@post('/edit/<no:int>')
def edit_item(no):
    
    if request.POST.save:
        edit = request.POST.task.strip()
        status = request.POST.status.strip()
        

        todo.update(no, edit, status)
        
    return redirect('/')

@get('/delete/<no:int>')
def delete_item_form(no):
    cur_data = todo.get_task(no)  # get the current data for the item we are editing
    return template('delete_task', old=cur_data, no=no)

@post('/delete/<no:int>')
def delete_item(no):
    
    if request.POST.delete:
        todo.delete(no)

    return redirect('/')

@post('/open/<no:int>')
def open_task(no):
    
    if request.POST.open:
        todo.open(no)

    return redirect('/')

@post('/close/<no:int>')
def close_task(no):
    
    if request.POST.close:
        todo.close(no)

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
    run(host='localhost', port=8080, debug=True, reloader=True)
