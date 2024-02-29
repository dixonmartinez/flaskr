from wtforms.validators import DataRequired, EqualTo  # , Length
# , BooleanField, ValidationError
from wtforms import StringField, SubmitField, EmailField, PasswordField
from flask_wtf import FlaskForm
from wtforms.widgets import TextArea

# Create a User Form Class


class UserForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_hash2', message='Passwor Must Match!')])
    password_hash2 = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserEditForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create form posts


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[
                          DataRequired()], widget=TextArea())
    slug = StringField('Slug', validators=[DataRequired()])
    author_id = StringField('Author')
    submit = SubmitField('Submit')

# create a search form


class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Submit')
