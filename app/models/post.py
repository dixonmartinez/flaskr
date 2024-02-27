from datetime import datetime
from app.extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)
    slug = db.Column(db.String(60))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Post "{self.title}">'
