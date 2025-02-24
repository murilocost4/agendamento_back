from flask import Blueprint, request, jsonify
from app.models import Convenio, db

convenios_bp = Blueprint('convenios', __name__, url_prefix='/api/convenios')

# Listar todos os convênios
@convenios_bp.route('/', methods=['GET'])
def listar_convenios():
    convenios = Convenio.query.all()
    return jsonify([convenio.to_dict() for convenio in convenios])

# Obter um convênio por ID
@convenios_bp.route('/<int:id>', methods=['GET'])
def obter_convenio(id):
    convenio = Convenio.query.get_or_404(id)
    return jsonify(convenio.to_dict())

# Criar um novo convênio
@convenios_bp.route('/', methods=['POST'])
def criar_convenio():
    dados = request.get_json()
    novo_convenio = Convenio(nome_convenio=dados['nome_convenio'])
    db.session.add(novo_convenio)
    db.session.commit()
    return jsonify(novo_convenio.to_dict()), 201

# Atualizar um convênio
@convenios_bp.route('/<int:id>', methods=['PUT'])
def atualizar_convenio(id):
    convenio = Convenio.query.get_or_404(id)
    dados = request.get_json()
    convenio.nome_convenio = dados.get('nome_convenio', convenio.nome_convenio)
    db.session.commit()
    return jsonify(convenio.to_dict())

# Excluir um convênio
@convenios_bp.route('/<int:id>', methods=['DELETE'])
def excluir_convenio(id):
    convenio = Convenio.query.get_or_404(id)
    db.session.delete(convenio)
    db.session.commit()
    return jsonify({'mensagem': 'Convênio excluído com sucesso'}), 200