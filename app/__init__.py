from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

# Instanciando as extensões
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializando as extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrando as rotas
    from app.routes import setup_routes
    setup_routes(app)

    return app
