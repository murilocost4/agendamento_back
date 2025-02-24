from flask import Blueprint, request, jsonify
from app.models import Clinica, db

clinicas_bp = Blueprint('clinicas', __name__, url_prefix='/api/clinicas')

# Listar todas as clínicas
@clinicas_bp.route('/', methods=['GET'])
def listar_clinicas():
    clinicas = Clinica.query.all()
    return jsonify([clinica.to_dict() for clinica in clinicas])

# Obter uma clínica por ID
@clinicas_bp.route('/<int:id>', methods=['GET'])
def obter_clinica(id):
    clinica = Clinica.query.get_or_404(id)
    return jsonify(clinica.to_dict())

# Criar uma nova clínica
@clinicas_bp.route('/', methods=['POST'])
def criar_clinica():
    dados = request.get_json()
    nova_clinica = Clinica(
        descricao=dados['descricao'],
        cnpj=dados['cnpj'],
        telefone=dados.get('telefone'),
        whatsapp=dados.get('whatsapp'),
        email=dados.get('email'),
        endereco=dados.get('endereco')
    )
    db.session.add(nova_clinica)
    db.session.commit()
    return jsonify(nova_clinica.to_dict()), 201

# Atualizar uma clínica
@clinicas_bp.route('/<int:id>', methods=['PUT'])
def atualizar_clinica(id):
    clinica = Clinica.query.get_or_404(id)
    dados = request.get_json()
    clinica.descricao = dados.get('descricao', clinica.descricao)
    clinica.cnpj = dados.get('cnpj', clinica.cnpj)
    clinica.telefone = dados.get('telefone', clinica.telefone)
    clinica.whatsapp = dados.get('whatsapp', clinica.whatsapp)
    clinica.email = dados.get('email', clinica.email)
    clinica.endereco = dados.get('endereco', clinica.endereco)
    db.session.commit()
    return jsonify(clinica.to_dict())

# Excluir uma clínica
@clinicas_bp.route('/<int:id>', methods=['DELETE'])
def excluir_clinica(id):
    clinica = Clinica.query.get_or_404(id)
    db.session.delete(clinica)
    db.session.commit()
    return jsonify({'mensagem': 'Clínica excluída com sucesso'}), 200