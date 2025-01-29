from flask import Blueprint, request, jsonify
from app import db
from app.models import Profissional

# Criação do Blueprint
profissional_bp = Blueprint('profissional', __name__)

# Rota para criar um profissional
@profissional_bp.route('/profissionais', methods=['POST'])
def create_profissional():
    data = request.get_json()

    try:
        novo_profissional = Profissional(
            nome=data['nome'],
            especialidade=data['especialidade'],
            crm=data['crm'],
            tipo_contrato=data['tipo_contrato'],
            disponibilidade=data['disponibilidade'],
            valor_consulta=data['valor_consulta'],
            valor_exame=data['valor_exame']
        )

        db.session.add(novo_profissional)
        db.session.commit()

        return jsonify(novo_profissional.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Rota para obter todos os profissionais
@profissional_bp.route('/profissionais', methods=['GET'])
def get_all_profissionais():
    profissionais = Profissional.query.all()
    return jsonify([profissional.to_dict() for profissional in profissionais]), 200


# Rota para obter um profissional pelo ID
@profissional_bp.route('/profissionais/<int:id>', methods=['GET'])
def get_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    return jsonify(profissional.to_dict()), 200


# Rota para atualizar um profissional
@profissional_bp.route('/profissionais/<int:id>', methods=['PUT'])
def update_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    data = request.get_json()

    try:
        profissional.nome = data['nome']
        profissional.especialidade = data['especialidade']
        profissional.crm = data['crm']
        profissional.tipo_contrato = data['tipo_contrato']
        profissional.disponibilidade = data['disponibilidade']
        profissional.valor_consulta = data['valor_consulta']
        profissional.valor_exame = data['valor_exame']

        db.session.commit()

        return jsonify(profissional.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Rota para deletar um profissional
@profissional_bp.route('/profissionais/<int:id>', methods=['DELETE'])
def delete_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    try:
        db.session.delete(profissional)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400
