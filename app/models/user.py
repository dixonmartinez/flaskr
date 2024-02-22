from app.extensions import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return f"<Name {self.name}"
