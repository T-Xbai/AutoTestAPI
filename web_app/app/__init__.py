__all__ = ['login_port','models']

from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/auto_port'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)