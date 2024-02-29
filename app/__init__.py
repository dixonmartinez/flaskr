from flask import Flask, render_template
from config import Config
from app.extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from app.models.users import Users
# export FLASK_APP=app
# export FLASK_ENV=development


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flak extensions here
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

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

    app.add_url_rule('/', endpoint='index')

    return app
