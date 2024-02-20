import os
from flask import Flask, render_template, request
from flaskr import blog


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasker.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "Hello, World!"
    # Invalid URL

    @app.errorhandler(404)
    @app.errorhandler(500)
    def page_not_found(error):
        print(error)
        print(request)
        return render_template('error.html', error=error), 404

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
