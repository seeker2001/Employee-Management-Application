import os
from flask import Flask, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "u9uvy7zyqdk7janq"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from api import api_blueprint

app.register_blueprint(api_blueprint)
from application import routes
