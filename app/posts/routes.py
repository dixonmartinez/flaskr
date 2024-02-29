from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from werkzeug.exceptions import abort
from app.posts import bp
from app.extensions import db
from app.models.post import Post
# from app.auth.routes import login_required
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired  # , EqualTo, Length
# EmailField, PasswordField, BooleanField, ValidationError
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea


@bp.route('/categories/')
def categories():
    return render_template('posts/categories.html')


@bp.route('/')
def index():
    # Grab all posts from the database
    posts = Post.query.order_by(Post.date_posted)
    """posts = db.execute(
        'SELECT p.id, title, body, SUBSTR(body, 0, 300) AS body_index, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()"""
    print(posts)
    # page = request.args.get('page', 1, type=int)
    # per_page = 5
    # start = (page - 1) * per_page
    # end = start + per_page
    # total_pages = (len(posts) + per_page - 1) // per_page
    # items_on_page = posts[start:end]
    return render_template('posts/index.html',
                           # items_on_page=items_on_page, total_pages=total_pages, page=page
                           posts=posts
                           )


@bp.route('/add-post', methods=('GET', 'POST'))
@login_required
def add_post():
    form = PostForm()
    # validate form
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        slug = form.slug.data
        # author_id = form.author_id.data
        # clear the form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        form.author_id.data = ''
        if not title:
            pass  # error = 'Title is required.'
        post = Post(title=title, content=content,
                    slug=slug, author_id=1)
        # Add data post to database
        db.session.add(post)
        db.session.commit()
        # Return a flash message
        flash("Post Added Successfully!")
        # Redirect to the post index
        return redirect(url_for('posts.index'))
    # Return create post page
    return render_template('posts/add-post.html', form=form)


"""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('posts.index'))
"""


def get_post(id, check_author=True):
    post = Post.query.get_or_404(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    # if check_author and post['author_id'] != g.user['id']:
    #    abort(403)
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    form = PostForm()
    # validate form
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        # author_id = form.author_id.data
        # clear the form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        form.author_id.data = ''
        # Add data post to database
        db.session.add(post)
        db.session.commit()
        # Return a flash message
        flash("Post updated Successfully!")
        # Redirect to the post index
        return redirect(url_for('posts.index'))
    form.title.data = post.title
    form.content.data = post.content
    form.slug.data = post.slug
    form.author_id.data = post.author_id

    return render_template('posts/update.html', form=form)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Blog post was delted!')
    except:
        # Return a error
        flash("Woops! There was a problem delteting post, try again...")
    return redirect(url_for('posts.index'))


@bp.route('/<int:id>/show')
def show(id):
    post = get_post(id)
    return render_template('posts/show.html', post=post)


"""
Una vista detallada para mostrar una sola entrada. 
Haga clic en el título de una entrada para ir a su página. Listo

Visualización por páginas. Sólo muestra 5 posts por página. Listo

Me gusta/no me gusta una entrada.

Comentarios.

Etiquetas. Al hacer clic en una etiqueta se muestran todos los mensajes con esa etiqueta.

Una caja de búsqueda que filtra la página del índice por nombre.

Cargar una imagen para acompañar un mensaje.

Formatear los posts usando Markdown.

Una fuente RSS de nuevos mensajes.
"""

# Create form posts


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[
                          DataRequired()], widget=TextArea())
    slug = StringField('Slug', validators=[DataRequired()])
    author_id = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Submit')
