from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from werkzeug.exceptions import abort
from app.posts import bp
from app.extensions import db
from app.models.posts import Posts
# from app.auth.routes import login_required
from app.web_forms import PostForm
from flask_login import current_user


@bp.route('/categories/')
def categories():
    return render_template('posts/categories.html')


@bp.route('/')
def index():
    # Grab all posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
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
        author = current_user.id
        # clear the form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        form.author_id.data = ''
        if not title:
            pass  # error = 'Title is required.'
        post = Posts(title=title, content=content,
                     slug=slug, author_id=author)
        # Add data post to database
        db.session.add(post)
        db.session.commit()
        # Return a flash message
        flash("Post Added Successfully!")
        # Redirect to the post index
        return redirect(url_for('posts.index'))
    # Return create post page
    return render_template('posts/add-post.html', form=form)


def get_post(id, check_author=True):
    post = Posts.query.get_or_404(id)
    print(post)
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != current_user.id:
        abort(403)
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
