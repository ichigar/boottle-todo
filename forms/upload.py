from wtforms import Form, SubmitField, FileField, validators

class UploadForm(Form):
    file = FileField('File', [validators.InputRequired()])
    submit = SubmitField('Upload')

