import functools
from flask import render_template, request, session, redirect, url_for, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.auth import bp


@bp.route('/')
def index():
    pass


@bp.route('/login', methods=['GET', 'POST'])
def login():
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


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                db.execute("INSERT INTO user(username, password) VALUES(?,?)",
                           (username, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kargs)
    return wrapped_view


@bp.route('/profile/<user>')
def profile(user):
    return render_template('profile.html', user=user)
