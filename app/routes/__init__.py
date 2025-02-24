from flask import Flask
from .pacientes import pacientes_bp
from .convenios import convenios_bp
from .profissionais import profissionais_bp
from .clinicas import clinicas_bp
from .servicos import servicos_bp
from .agendamentos import agendamentos_bp
from .especialidades import especialidades_bp

def init_app(app: Flask):
    """
    Registra todos os Blueprints das rotas no aplicativo Flask.
    """
    # Registra as rotas de cada módulo
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(convenios_bp)
    app.register_blueprint(profissionais_bp)
    app.register_blueprint(clinicas_bp)
    app.register_blueprint(servicos_bp)
    app.register_blueprint(agendamentos_bp)
    app.register_blueprint(especialidades_bp)