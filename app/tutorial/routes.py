from app.tutorial import bp
from flask import render_template, flash
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


@bp.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfull")
    return render_template('tutorial/index.html', name=name, form=form)

# a simple page that says hello


@bp.route('/hello')
def hello():
    return "Hello, World!"

# Create a form class


class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

    """
    flask-migrate
    https://flask-migrate.readthedocs.io/en/latest/
    flask db
    flask db init
    flask db migrate -m 'Initial MIgration'
    flask db upgrade
    flask db migrate -m 'Added somthing'

    """
