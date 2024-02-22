
from flask import Blueprint

bp = Blueprint('tutorial', __name__)
from app.tutorial import routes