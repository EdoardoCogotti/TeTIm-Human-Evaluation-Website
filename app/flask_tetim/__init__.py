from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_tetim.config import Config
from flask_tetim.db_loader import DatabaseLoader

app = Flask(__name__)

app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(minutes=60)
db = SQLAlchemy(app)

from flask_tetim.models import Question, Answer

db.create_all()
dl = DatabaseLoader()
dl.load()
