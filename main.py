import sqlite3
from bottle import route, run, template, request
from config.config import db_file

@route('/todo')
@route('/my_todo_list')
def todo_list():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    output = template('make_table', rows=result)
    return output

@route('/new')
def new_item_form():
    return template('new_task')

@route('/new', method='POST')
def new_item_save():
    if request.POST.save:  # the user clicked the `save` button
        new = request.POST.task.strip()    # get the task from the form
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
        new_id = c.lastrowid

        conn.commit()
        c.close()
        # se muestra el resultado de la operación
        return '<p>La tarea se almacenó en la base de datos, El ID es %s</p>' % new_id
        
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
