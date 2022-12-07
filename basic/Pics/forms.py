from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class Upload(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['png', 'jpg'])])
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Upload')


class EditUpload(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')
