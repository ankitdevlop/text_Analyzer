# create_tables.py
from app import app
from extensions import db

with app.app_context():
    db.create_all()
    print("✅ All tables created.")
