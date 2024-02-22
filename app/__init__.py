from flask import Flask
from config import Config
from app.extensions import db
# export FLASK_APP=app
# export FLASK_ENV=development


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flak extensions here
    db.init_app(app)
    # Register Blueprint here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')
    from app.questions import bp as question_bp
    app.register_blueprint(question_bp, url_prefix='/questions')

    @app.route('/test')
    def test():
        return "Test App"

    return app
