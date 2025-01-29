from flask import Blueprint, request, jsonify
from app import db
from app.models import Agendamento, Paciente, Profissional, Clinica, Servico
from datetime import datetime

agendamento_bp = Blueprint('agendamento', __name__)

# Função para criar um novo agendamento
@agendamento_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    data = request.get_json()

    # Verifica se os IDs de relacionamento existem
    paciente = Paciente.query.get(data['id_paciente'])
    if not paciente:
        return jsonify({"message": "Paciente não encontrado"}), 404

    servico = Servico.query.get(data['id_servico'])
    if not servico:
        return jsonify({"message": "Serviço não encontrado"}), 404

    profissional = Profissional.query.get(data.get('id_profissional'))
    if data.get('id_profissional') and not profissional:
        return jsonify({"message": "Profissional não encontrado"}), 404

    clinica = Clinica.query.get(data.get('id_clinica'))
    if data.get('id_clinica') and not clinica:
        return jsonify({"message": "Clínica não encontrada"}), 404

    # Cria o agendamento
    novo_agendamento = Agendamento(
        id_paciente=data['id_paciente'],
        id_servico=data['id_servico'],
        id_profissional=data.get('id_profissional'),
        id_clinica=data.get('id_clinica'),
        data_agendamento=datetime.strptime(data['data_agendamento'], '%Y-%m-%d %H:%M:%S'),
        forma_pagamento=data['forma_pagamento'],
        status=data.get('status', 'pendente'),
        valor=data.get('valor'),
        observacoes=data.get('observacoes')
    )

    db.session.add(novo_agendamento)
    db.session.commit()

    return jsonify({"message": "Agendamento criado com sucesso!", "agendamento": novo_agendamento.to_dict()}), 201


# Rota para listar todos os agendamentos
@agendamento_bp.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    agendamentos = Agendamento.query.all()
    return jsonify([agendamento.to_dict() for agendamento in agendamentos])


# Rota para pegar um agendamento específico
@agendamento_bp.route('/agendamentos/<int:id>', methods=['GET'])
def get_agendamento(id):
    agendamento = Agendamento.query.get(id)
    if agendamento is None:
        return jsonify({'message': 'Agendamento não encontrado'}), 404
    return jsonify(agendamento.to_dict())


# Rota para atualizar um agendamento
@agendamento_bp.route('/agendamentos/<int:id>', methods=['PUT'])
def update_agendamento(id):
    agendamento = Agendamento.query.get(id)
    if agendamento is None:
        return jsonify({'message': 'Agendamento não encontrado'}), 404

    data = request.get_json()

    # Atualiza os campos
    agendamento.id_paciente = data.get('id_paciente', agendamento.id_paciente)
    agendamento.id_profissional = data.get('id_profissional', agendamento.id_profissional)
    agendamento.id_clinica = data.get('id_clinica', agendamento.id_clinica)
    agendamento.id_servico = data.get('id_servico', agendamento.id_servico)
    agendamento.data_agendamento = datetime.strptime(data.get('data_agendamento', agendamento.data_agendamento.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
    agendamento.status = data.get('status', agendamento.status)
    agendamento.valor = data.get('valor', agendamento.valor)
    agendamento.forma_pagamento = data.get('forma_pagamento', agendamento.forma_pagamento)
    agendamento.observacoes = data.get('observacoes', agendamento.observacoes)

    db.session.commit()

    return jsonify({'message': 'Agendamento atualizado com sucesso', 'agendamento': agendamento.to_dict()})


# Rota para deletar um agendamento
@agendamento_bp.route('/agendamentos/<int:id>', methods=['DELETE'])
def delete_agendamento(id):
    agendamento = Agendamento.query.get(id)
    if agendamento is None:
        return jsonify({'message': 'Agendamento não encontrado'}), 404

    db.session.delete(agendamento)
    db.session.commit()

    return jsonify({'message': 'Agendamento deletado com sucesso'})