from app import app
from extensions import db

with app.app_context():
    db.drop_all()  # ❗ This will delete all tables and data
    db.create_all()
