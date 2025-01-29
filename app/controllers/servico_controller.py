from flask import Blueprint, request, jsonify
from app import db
from app.models import Servico

# Criação do Blueprint
servico_bp = Blueprint('servico', __name__)

# Rota para criar um serviço
@servico_bp.route('/servicos', methods=['POST'])
def create_servico():
    data = request.get_json()

    try:
        novo_servico = Servico(
            nome_servico=data['nome_servico'],
            descricao=data['descricao'],
            tipo_servico=data['tipo_servico']
        )

        db.session.add(novo_servico)
        db.session.commit()

        return jsonify(novo_servico.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Rota para obter todos os serviços
@servico_bp.route('/servicos', methods=['GET'])
def get_all_servicos():
    servicos = Servico.query.all()
    return jsonify([servico.to_dict() for servico in servicos]), 200


# Rota para obter um serviço pelo ID
@servico_bp.route('/servicos/<int:id>', methods=['GET'])
def get_servico(id):
    servico = Servico.query.get_or_404(id)
    return jsonify(servico.to_dict()), 200


# Rota para atualizar um serviço
@servico_bp.route('/servicos/<int:id>', methods=['PUT'])
def update_servico(id):
    servico = Servico.query.get_or_404(id)
    data = request.get_json()

    try:
        servico.nome_servico = data['nome_servico']
        servico.descricao = data['descricao']
        servico.tipo_servico = data['tipo_servico']

        db.session.commit()

        return jsonify(servico.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Rota para deletar um serviço
@servico_bp.route('/servicos/<int:id>', methods=['DELETE'])
def delete_servico(id):
    servico = Servico.query.get_or_404(id)
    try:
        db.session.delete(servico)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400
