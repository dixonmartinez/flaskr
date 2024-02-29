from datetime import datetime
from app.extensions import db


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)
    slug = db.Column(db.String(60))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign key to link Users
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Post "{self.title}">'
