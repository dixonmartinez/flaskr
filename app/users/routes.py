from flask import render_template, flash, request
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, EmailField
from flask_wtf import FlaskForm
from app.users import bp
from app.models.user import Users
from app.extensions import db


@bp.route('/', methods=['GET', 'POST'])
def index():
    name = None
    email = None
    form = UserForm()
    # validate form
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        user = Users.query.filter_by(email=email).first()
        if user is None:
            user = Users(name=name, email=email)
            db.session.add(user)
            db.session.commit()
            flash("User Added Successfully!")
        form.name.data = ''
        form.email.data = ''
    users_list = Users.query.order_by(Users.created)
    return render_template('users/index.html', form=form, name=name, email=email, users_list=users_list)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    user = Users.query.get_or_404(id)
    if request.method == 'POST':
        if user:
            user.name = request.form['name']
            user.email = request.form['email']
            try:
                db.session.commit()
                flash('User updated Successfully!')
                return render_template('users/update.html', form=form, user=user)
            except:
                flash('Error! Looks like there was a problem... try again!')
                return render_template('users/update.html', form=form, user=user)
    return render_template('users/update.html', form=form, user=user)

# Create a User Form Class


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
