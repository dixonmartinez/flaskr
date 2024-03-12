from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template('public/index.html')


@bp.route('/about')
def about():
    return render_template('public/about.html')


@bp.route('/services')
def services():
    return render_template('public/services.html')
