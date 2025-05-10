import os
import logging

from flask import Flask
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from extensions import db  # Import db from extensions

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)

# Directly set the session secret and database URL here
app.secret_key = "mysecretkey"  # Replace this with your actual secret key
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database with the external database URL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://text_analyzer_user:hGsHSsQMykZYHUsXsnNsF3sfzqi8ZFwq@dpg-d0fkg42dbo4c73aidhn0-a.oregon-postgres.render.com/text_analyzer"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize db with the app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import models inside the user_loader function to avoid circular import
@login_manager.user_loader
def load_user(user_id):
    from models import User  # Lazy import to prevent circular import
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

from routes import *  # noqa: E402, F403
if __name__ == "__main__":
    app.run(debug=True)
