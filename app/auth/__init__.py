from flask import Blueprint
bp = Blueprint('auth', __name__)
# t
from app.auth import routes
