from flask import Flask
from app.controllers.paciente_controller import paciente_bp
from app.controllers.profissional_controller import profissional_bp
from app.controllers.clinica_controller import clinica_bp
from app.controllers.servico_controller import servico_bp
from app.controllers.agendamento_controller import agendamento_bp

def setup_routes(app):
    app.register_blueprint(paciente_bp)
    app.register_blueprint(profissional_bp)
    app.register_blueprint(clinica_bp)
    app.register_blueprint(servico_bp)
    app.register_blueprint(agendamento_bp)
