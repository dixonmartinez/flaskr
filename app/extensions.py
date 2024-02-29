from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()
ckeditor = CKEditor()
migrate = Migrate()
