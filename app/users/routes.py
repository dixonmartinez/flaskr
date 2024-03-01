from flask import render_template, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
import uuid as uuid
import os
from app.users import bp
from app.models.users import Users
from app.extensions import db
from app.web_forms import UserForm, LoginForm
from flask import current_app


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password_hash = form.password_hash.data
        email = form.email.data
        about_author = form.about_author.data
        error = None
        if username is None:
            error = 'Username is required.'
        elif name is None:
            error = 'Name is required.'
        elif password_hash is None:
            error = 'Password is required.'
        elif email is None:
            error = 'Email is required.'
        else:
            user = Users.query.filter_by(username=username).first()
            if user:
                flash('That User Exists! Try Again...!')
                if not current_user:
                    return redirect(url_for('users.login'))
            else:
                user = Users(name=name, username=username, password_hash=generate_password_hash(
                    password_hash), email=email, about_author=about_author)
                try:
                    db.session.add(user)
                    db.session.commit()
                    # login_user(user)
                    flash('Users Added Successful...!')
                    if not current_user:
                        return redirect(url_for('users.login'))
                    return redirect(url_for('users'))
                except:
                    flash('That User Doesn\'t Exists! Try Again...!')
        if error:
            flash(error)
    return render_template('users/add-user.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                flash('Login successfully...!')
                return redirect(url_for('users.dashboard'))
            else:
                flash('Wrong Password-Try Again...!')
        else:
            flash('That User Doesn\'t Exists! Try Again...!')

    return render_template('users/login.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Hava Been Logged Out! Thanks For Stopping By...')
    return redirect(url_for('index'))


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    user = Users.query.get_or_404(current_user.id)
    print(user.about_author)
    if request.method == 'POST':
        if user:
            user.name = request.form['name']
            user.username = request.form['username']
            user.email = request.form['email']
            user.about_author = request.form['about_author']
            if request.files['profile_pic'].filename:
                user.profile_pic = request.files['profile_pic']
                print(user.profile_pic)
                # Save That Image
                saver = user.profile_pic
                # Grab image name
                pic_filename = secure_filename(saver.filename)
                file_ext = os.path.splitext(pic_filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    pass #abort(400)
                # Set UUID
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                # Change it to string to save to db
                user.profile_pic = pic_name
                file_target = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], pic_name.strip())
                saver.save(file_target)
            try:
                db.session.commit()
                flash('User Updated Successfully!')
            except:
                flash('Error! Looks like there was a problem... try again!')
        else:
            flash('Error! User not found... try again!')
    return render_template('users/dashboard.html', form=form)


@bp.route('/', methods=['GET', 'POST'])
@login_required
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
@login_required
def update(id):
    form = UserForm()
    user = Users.query.get_or_404(id)
    if request.method == 'POST':
        if user:
            user.name = request.form['name']
            user.username = request.form['username']
            user.email = request.form['email']
            try:
                db.session.commit()
                flash('User Updated Successfully!')
            except:
                flash('Error! Looks like there was a problem... try again!')
    return render_template('users/update.html', form=form, user=user)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    if id == current_user.id:
        user = Users.query.get_or_404(id)
        print(user)
        try:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!!')
        except:
            flash('Woops!! There was a problem deleting user, try again...')
    else:
        flash('Sorry, you can\'t delete that user!')
    return redirect(url_for('dashboard'))
