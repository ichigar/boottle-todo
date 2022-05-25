from email_validator import EmailNotValidError
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField , validators
class RegistrationForm(Form):
    username     = StringField('Username', [validators.Length(min=4, max=25)], default='nombre de usaurio')
    email        = StringField('Email Address', [validators.InputRequired(), validators.Length(min=6, max=60), validators.Email()])
    accept_rules = BooleanField('Acepto las reglas del sitio', [validators.InputRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', 
                           message='Las contraseñas no coinciden')
        ])
    password_confirm = PasswordField('Repeat Password')
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
    
