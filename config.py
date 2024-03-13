import os
basedir = os.path.abspath(os.path.dirname(__file__))

# export SECRET_KEY="your secret key"
# export DATABASE_URI="postgresql://username:password@host:port/database_name"


class Config():
    SECRET_KEY = os.environ.get(
        'SECRECT_KEY') or '123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_PKG_TYPE = 'standard'  # basic, standard, full, standard-all, full-all
    # Flag used to enable serving resources from local when use ckeditor.load(), default is to retrieve from CDN.
    CKEDITOR_SERVE_LOCAL = True
    # CKEDITOR_CUSTOM_URL = 'static/ckeditor/ckeditor.js'
    CKEDITOR_CUSTOM_URL = '3static/ckeditor/full/ckeditor.js'
    UPLOAD_FOLDER = 'app/static/images/'
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
