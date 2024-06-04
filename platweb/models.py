from platweb import database
from flask_sqlalchemy import SQLAlchemy
class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(128), nullable=False)
