from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from basic.models import User


class Registration(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    mail = StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=18)])
    confirm_pass = PasswordField('Confirm Password',
                                 validators=[DataRequired(), Length(min=8, max=18), EqualTo('password')])
    submit = SubmitField('signup')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('Name already exists please use another name')

    def validate_mail(self, email):
        user = User.query.filter_by(mail=email.data).first()
        if user:
            raise ValidationError('Mail already exists please use another mail')


class Login(FlaskForm):
    mail = StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=18)])
    submit = SubmitField('login')


class Update(FlaskForm):
    name = StringField('Name', validators=[Length(min=2, max=20)])
    mail = StringField('Mail', validators=[Email()])
    submit = SubmitField('Update')

    def validate_name(self, name):
        if current_user.name != name.data:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('Name already exists please use another name')

    def validate_mail(self, email):
        if current_user.mail != email.data:
            user = User.query.filter_by(mail=email.data).first()
            if user:
                raise ValidationError('Mail already exists please use another mail')


class ResetMail(FlaskForm):
    mail = StringField('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset mail')

    def validate_mail(self, mail):
        usr = User.query.filter_by(mail=mail.data).first()
        if usr is None:
            raise ValidationError('The mail doesnt exist try giving a valid mail')


class ResetPassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=18)])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
