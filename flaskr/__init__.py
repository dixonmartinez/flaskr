from . import auth
from . import blog
from . import tutorial
from . import users
import os
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='MySecret Pass Dev',
        DATABASE=os.path.join(app.instance_path, 'flasker.sqlite'),
        SQLALCHEMY_DATABASE_URI='sqlite:///flasker.sqlite',
    )

    if test_config:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    else:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # Blueprint
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(tutorial.bp)
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')
    return app

app = create_app()
# Initialize database
my_db = SQLAlchemy(app)

def create_app2(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasker.sqlite'),
        DEBUG=True
    )
    # Invalid URL

    @app.errorhandler(404)
    @app.errorhandler(500)
    def page_not_found(error):
        print(error)
        print(request)
        return render_template('error.html', error=error), 404

    from . import db
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(tutorial.bp)
    app.add_url_rule('/', endpoint='index')
