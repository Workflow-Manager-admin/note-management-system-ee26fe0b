from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# PUBLIC_INTERFACE
class Note(db.Model):
    """Model representing a note."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Note id={self.id} title={self.title}>"
