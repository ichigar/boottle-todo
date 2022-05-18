import sqlite3
from bottle import route, run, template, request, get, post, redirect, static_file, error, response
from config.config import DATABASE


@get('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM todo")
    result = c.fetchall()
    c.close()
    return template('index', rows=result)

@route('/todo')
@route('/my_todo_list')
def todo_list():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    output = template('make_table', rows=result)
    return output

@get('/new')
def new_item_form():
    return template('new_task')

@post('/new')
def new_item_save():
    if request.POST.save:  # the user clicked the `save` button
        new = request.POST.task.strip()    # get the task from the form
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
       
        conn.commit()
        c.close()
        # se muestra el resultado de la operación
        return redirect('/')

@get('/edit/<no:int>')
def edit_item_form(no):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id = ?", (no,))
    cur_data = c.fetchone()
    c.close()
    return template('edit_task', old=cur_data, no=no)

@post('/edit/<no:int>')
def edit_item(no):

    if request.POST.save:
        edit = request.POST.task.strip()
        status = request.POST.status.strip()

        if status == 'pendiente':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()
        c.close()

        return redirect('/')

@get('/delete/<no:int>')
def delete_item_form(no):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", str(no))
    cur_data = c.fetchone()
    c.close()

    return template('delete_task', old=cur_data, no=no)

@post('/delete/<no:int>')
def delete_item(no):
    if request.POST.delete:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("DELETE FROM todo WHERE id LIKE ?", str(no))
        conn.commit()
        c.close()

    return redirect('/')

@get('/favicon.ico')
def about():
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

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
