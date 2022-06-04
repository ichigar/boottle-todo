from wtforms import Form, StringField, BooleanField, SubmitField, validators


class EditTaskForm(Form):
    
    task = StringField('Tarea', [validators.DataRequired()], render_kw={"size" : "70", "maxlength" : "100"})
    status = BooleanField('Finalizada')
  
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
    
