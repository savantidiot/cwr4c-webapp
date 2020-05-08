from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#venv\Scripts\activate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from webapp import routes
