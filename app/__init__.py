from flask_login import LoginManager
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)
login = LoginManager(app)
