from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import TestingConfig, ProductionConfig


app = Flask(__name__)
app.config.from_object(TestingConfig) 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to log in'
login_manager.login_message_category = 'success'


@app.cli.command("seeder")
def seed_db():
    from .seeder import seed
    seed(db)

from . import views


