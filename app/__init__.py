from flask import Flask
from config import Config
from app.extensions import db
from flask_migrate import Migrate
# export FLASK_APP=app
# export FLASK_ENV=development


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flak extensions here
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprint here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')
    from app.questions import bp as question_bp
    app.register_blueprint(question_bp, url_prefix='/questions')
    from app.tutorial import bp as tutorial_bp
    app.register_blueprint(tutorial_bp, url_prefix='/tutorial')
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    app.add_url_rule('/', endpoint='index')

    @app.route('/test')
    def test():
        return "Test App"

    return app
