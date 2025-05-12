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

# Session secret key — replace with a secure one in production!
app.secret_key = "mysecretkey"

# Fix for HTTPS and reverse proxy (needed for url_for and secure cookies)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database config (from Render PostgreSQL)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://text_analyzer_user:hGsHSsQMykZYHUsXsnNsF3sfzqi8ZFwq@dpg-d0fkg42dbo4c73aidhn0-a.oregon-postgres.render.com/text_analyzer"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User  # Lazy import to avoid circular dependencies
    return User.query.get(int(user_id))

# Create tables if not exist
with app.app_context():
    db.create_all()

# Import routes (should be at the end to avoid circular imports)
from routes import *  # noqa: E402, F403

# Entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT in env
    app.run(host="0.0.0.0", port=port, debug=False)
