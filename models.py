from datetime import datetime
from app import db
from extensions import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    text_entries = db.relationship('TextEntry', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class TextEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    word_count = db.Column(db.Integer, nullable=False)
    char_count = db.Column(db.Integer, nullable=False)
    reading_time = db.Column(db.Float, nullable=False)  # in minutes
    font_style = db.Column(db.String(50), default='sans-serif')
    background_color = db.Column(db.String(20), default='#ffffff')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<TextEntry {self.id} by User {self.user_id}>'
