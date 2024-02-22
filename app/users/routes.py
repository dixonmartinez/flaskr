from flask import render_template, flash, request, redirect, url_for
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField, ValidationError
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash

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
        password_hash = form.password_hash.data
        user = Users.query.filter_by(email=email).first()
        if user is None:
            user = Users(name=name, email=email,
                         password_hash=generate_password_hash(password_hash))
            db.session.add(user)
            db.session.commit()
            flash("User Added Successfully!")
        else:
            flash(f"User {user.email} is found!!")
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
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


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user = Users.query.get_or_404(id)
    print(user)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!!')
    except:
        flash('Woops!! There was a problem deleting user, try again...')
    return redirect(url_for('users.index'))

# Create a User Form Class


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_hash2', message='Passwor Must Match!')])
    password_hash2 = PasswordField(
        'Confirm Password', validators=[DataRequired()])

    submit = SubmitField('Submit')
