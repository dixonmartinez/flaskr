from app.main import bp
from flask import render_template
from app.models.posts import Posts


@bp.route('/')
def index():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('public/index.html', posts=posts)


@bp.route('/about')
def about():
    return render_template('public/about.html')


@bp.route('/services')
def services():
    return render_template('public/services.html')


@bp.route('/single/<int:id>')
def single(id):
    post = Posts.query.get_or_404(id)
    return render_template('public/single.html', post=post)
