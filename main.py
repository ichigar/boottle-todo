import sqlite3
from bottle import route, run, template, request, get, post, redirect
from config.config import DATABASE

@route('/todo')
@route('/my_todo_list')
def todo_list():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
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
        return redirect('/todo')

@get('/edit/<no:int>')
def edit_item(no):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT task, status FROM todo WHERE id = ?", (no,))
    cur_data = c.fetchone()
    print(cur_data)
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

        return redirect('/todo')
       
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
