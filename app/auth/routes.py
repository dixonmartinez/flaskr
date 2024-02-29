import functools
from flask import render_template, request, session, redirect, url_for, flash, g
from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.auth import bp
from app.models.user import Users






@bp.route('/login2', methods=['GET', 'POST'])
def login2():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


@bp.route('/logout2')
def logout2():
    session.clear()
    return redirect(url_for('index'))


"""def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kargs)
    return wrapped_view"""


@bp.route('/profile/<user>')
def profile(user):
    return render_template('profile.html', user=user)
