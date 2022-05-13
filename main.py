import sqlite3
from bottle import route, run, template
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

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
