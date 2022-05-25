from email_validator import EmailNotValidError
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField , validators


class RegistrationForm(Form):
    
    username     = StringField('Username', 
                               [validators.Length(min=4, max=25)], 
                               default='nombre de usuario', 
                               render_kw={'class':'myclass'}
                            )
    email        = StringField('Email Address', [
                                    validators.InputRequired(), 
                                    validators.Length(min=6, max=60), 
                                    validators.Email( message='Correo incorrecto')
                                ])
    accept_rules = BooleanField('Acepto las reglas del sitio', [validators.InputRequired()])
    password = PasswordField('New Password', [
                                    validators.Length(min=10, max=60),
                                    validators.EqualTo('password_confirm', message='Las contraseñas no coinciden')
                                ])
    password_confirm = PasswordField('Repeat Password', render_kw=styles)
    save = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
    
