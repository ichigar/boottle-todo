from wtforms import Form, StringField, BooleanField, SubmitField, validators


class EditTaskForm(Form):
    
    task = StringField('Tarea', [validators.DataRequired()])
    status = BooleanField('Finalizada')
  
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')