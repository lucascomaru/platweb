from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b501ecd31a04558a4171bed20430c9a5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gtarefas.database'

database = SQLAlchemy(app)

# Importação das rotas após a inicialização do aplicativo
from platweb import routes
