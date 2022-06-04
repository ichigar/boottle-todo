from turtle import width
from wtforms import Form, StringField, SubmitField, validators
import sys
sys.path.append('models') # add the models directory to the path
sys.path.append('config')


from models.todo import Todo
from config.config import DATABASE

todo = Todo(DATABASE)

class NewTaskForm(Form):
    
    task = StringField('Tarea', [validators.DataRequired()])
    
    def validate_task(form, task):
        result = todo.get(['task'], {'task': task.data})
        if result != None:
            raise validators.ValidationError('La tarea ya existe')
    
    
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')