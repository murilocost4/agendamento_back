from flask import Blueprint, request, jsonify
from app import db
from app.models import Clinica

# Criação do Blueprint
clinica_bp = Blueprint('clinica', __name__)

# Rota para criar uma clínica
@clinica_bp.route('/clinicas', methods=['POST'])
def create_clinica():
    data = request.get_json()

    try:
        nova_clinica = Clinica(
            nome=data['nome'],
            cnpj=data['cnpj'],
            endereco=data['endereco'],
            telefone=data['telefone'],
            email=data['email']
        )

        db.session.add(nova_clinica)
        db.session.commit()

        return jsonify(nova_clinica.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Rota para obter todas as clínicas
@clinica_bp.route('/clinicas', methods=['GET'])
def get_all_clinicas():
    clinicas = Clinica.query.all()
    return jsonify([clinica.to_dict() for clinica in clinicas]), 200


# Rota para obter uma clínica pelo ID
@clinica_bp.route('/clinicas/<int:id>', methods=['GET'])
def get_clinica(id):
    clinica = Clinica.query.get_or_404(id)
    return jsonify(clinica.to_dict()), 200


# Rota para atualizar uma clínica
@clinica_bp.route('/clinicas/<int:id>', methods=['PUT'])
def update_clinica(id):
    clinica = Clinica.query.get_or_404(id)
    data = request.get_json()

    try:
        clinica.nome = data['nome']
        clinica.cnpj = data['cnpj']
        clinica.endereco = data['endereco']
        clinica.telefone = data['telefone']
        clinica.email = data['email']

        db.session.commit()

        return jsonify(clinica.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Rota para deletar uma clínica
@clinica_bp.route('/clinicas/<int:id>', methods=['DELETE'])
def delete_clinica(id):
    clinica = Clinica.query.get_or_404(id)
    try:
        db.session.delete(clinica)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400
