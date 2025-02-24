from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # Importe o CORS
from app.config import Config

# Instanciando as extensões
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configura o CORS
    CORS(app)

    # Inicializando as extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrando as rotas
    from app.routes import init_app
    init_app(app)

    return app