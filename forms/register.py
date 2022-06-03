from email_validator import EmailNotValidError
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField , RadioField, TextAreaField, SelectField, validators
import sys
sys.path.append('models') # add the models directory to the path
sys.path.append('config')


from models.todo import Todo
from config.config import DATABASE

COUNTRIES = [('', 'Select country'), ('ES', 'Spain'), ('US', 'United States'), ('UK', 'United Kingdom')]

todo = Todo(DATABASE) # Creamos objeto vinculado a la base de datos

    
class RegistrationForm(Form):
    
    id = StringField('id', [validators.DataRequired()])
    
    def validate_id(form, id):
        print(id.data)
        result = todo.get(['id'], {'id': id.data})
        print(result)
        if result != None:
            # form.id.errors.append('id already exists')
            raise validators.ValidationError('Id already exists')
    
    
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
    
