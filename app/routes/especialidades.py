from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.models import Especialidade, db

especialidades_bp = Blueprint('especialidades', __name__, url_prefix='/api/especialidades')

# Listar todas as especialidades
@especialidades_bp.route('', methods=['GET'], strict_slashes=False)
@cross_origin()
def listar_especialidades():
    try:
        especialidades = Especialidade.query.all()
        return jsonify([especialidade.to_dict() for especialidade in especialidades])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obter uma especialidade por ID
@especialidades_bp.route('/<int:id>', methods=['GET'])
@cross_origin()
def obter_especialidade(id):
    try:
        especialidade = Especialidade.query.get_or_404(id)
        return jsonify(especialidade.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Criar uma nova especialidade
@especialidades_bp.route('', methods=['POST'], strict_slashes=False)
@cross_origin()
def criar_especialidade():
    try:
        dados = request.get_json()
        nova_especialidade = Especialidade(
            nome_especialidade=dados['nome_especialidade']
        )
        db.session.add(nova_especialidade)
        db.session.commit()
        return jsonify(nova_especialidade.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Atualizar uma especialidade
@especialidades_bp.route('/<int:id>', methods=['PUT'])
@cross_origin()
def atualizar_especialidade(id):
    try:
        especialidade = Especialidade.query.get_or_404(id)
        dados = request.get_json()
        especialidade.nome_especialidade = dados.get('nome_especialidade', especialidade.nome_especialidade)
        db.session.commit()
        return jsonify(especialidade.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Excluir uma especialidade
@especialidades_bp.route('/<int:id>', methods=['DELETE'])
@cross_origin()
def excluir_especialidade(id):
    try:
        especialidade = Especialidade.query.get_or_404(id)
        db.session.delete(especialidade)
        db.session.commit()
        return jsonify({'mensagem': 'Especialidade excluída com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500