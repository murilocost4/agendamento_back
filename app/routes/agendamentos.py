from flask import Blueprint, request, jsonify
from app.models import Agendamento, db
from datetime import datetime

agendamentos_bp = Blueprint('agendamentos', __name__, url_prefix='/api/agendamentos')

# Listar todos os agendamentos
@agendamentos_bp.route('/', methods=['GET'])
def listar_agendamentos():
    agendamentos = Agendamento.query.all()
    return jsonify([agendamento.to_dict() for agendamento in agendamentos])

# Obter um agendamento por ID
@agendamentos_bp.route('/<int:id>', methods=['GET'])
def obter_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    return jsonify(agendamento.to_dict())

# Criar um novo agendamento
@agendamentos_bp.route('/', methods=['POST'])
def criar_agendamento():
    dados = request.get_json()
    novo_agendamento = Agendamento(
        data_solicitacao=datetime.strptime(dados['data_solicitacao'], '%Y-%m-%d %H:%M:%S'),
        id_solicitante=dados['id_solicitante'],
        id_paciente=dados['id_paciente'],
        id_servico=dados['id_servico'],
        id_profissional=dados.get('id_profissional'),
        id_clinica=dados.get('id_clinica'),
        data_agendamento=datetime.strptime(dados['data_agendamento'], '%Y-%m-%d %H:%M:%S'),
        horario=datetime.strptime(dados['horario'], '%H:%M:%S').time(),
        valor=dados.get('valor'),
        status=dados['status']
    )
    db.session.add(novo_agendamento)
    db.session.commit()
    return jsonify(novo_agendamento.to_dict()), 201

# Atualizar um agendamento
@agendamentos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    dados = request.get_json()
    agendamento.data_solicitacao = datetime.strptime(dados.get('data_solicitacao', agendamento.data_solicitacao.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
    agendamento.id_solicitante = dados.get('id_solicitante', agendamento.id_solicitante)
    agendamento.id_paciente = dados.get('id_paciente', agendamento.id_paciente)
    agendamento.id_servico = dados.get('id_servico', agendamento.id_servico)
    agendamento.id_profissional = dados.get('id_profissional', agendamento.id_profissional)
    agendamento.id_clinica = dados.get('id_clinica', agendamento.id_clinica)
    agendamento.data_agendamento = datetime.strptime(dados.get('data_agendamento', agendamento.data_agendamento.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
    agendamento.horario = datetime.strptime(dados.get('horario', agendamento.horario.strftime('%H:%M:%S')), '%H:%M:%S').time()
    agendamento.valor = dados.get('valor', agendamento.valor)
    agendamento.status = dados.get('status', agendamento.status)
    db.session.commit()
    return jsonify(agendamento.to_dict())

# Excluir um agendamento
@agendamentos_bp.route('/<int:id>', methods=['DELETE'])
def excluir_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()