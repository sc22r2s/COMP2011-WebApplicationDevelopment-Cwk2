from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# To manage login
login_manager = LoginManager()
login_manager.init_app(app)

# To manage encryption
bcrypt = Bcrypt(app)

app.config.from_object('config')

migrate = Migrate(app, db, render_as_batch=True)
admin = Admin(app, template_mode='bootstrap4')

from app import views, models
