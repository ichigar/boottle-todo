import os
import sys
sys.path.append('models') # add the models directory to the path

import bottle
from bottle import route, run, template, request, get, post, redirect, static_file, error, response
from config.config import DATABASE, TODO_DEFINITION
from models.todo import Todo
from validation.validate import Validate

# Importamos las rutas de la carpeta routes
from routes.routes_todo import *
from routes.routes_static import *



app = bottle.default_app()

if __name__ == '__main__':
    if not os.path.exists(DATABASE) or os.path.getsize(DATABASE) == 0:
        
        todo.create(TODO_DEFINITION)
        
    run(host='localhost', port=8080, debug=True, reloader=True)
