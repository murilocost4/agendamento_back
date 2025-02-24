from flask import Blueprint, request, jsonify
from app.models import Profissional, db

profissionais_bp = Blueprint('profissionais', __name__, url_prefix='/api/profissionais')

# Listar todos os profissionais
@profissionais_bp.route('/', methods=['GET'])
def listar_profissionais():
    profissionais = Profissional.query.all()
    return jsonify([profissional.to_dict() for profissional in profissionais])

# Obter um profissional por ID
@profissionais_bp.route('/<int:id>', methods=['GET'])
def obter_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    return jsonify(profissional.to_dict())

# Criar um novo profissional
@profissionais_bp.route('/', methods=['POST'])
def criar_profissional():
    dados = request.get_json()
    novo_profissional = Profissional(
        nome=dados['nome'],
        id_especialidade=dados['id_especialidade'],
        registro_profissional=dados['registro_profissional'],
        telefone=dados.get('telefone'),
        email=dados.get('email'),
        endereco=dados.get('endereco')
    )
    db.session.add(novo_profissional)
    db.session.commit()
    return jsonify(novo_profissional.to_dict()), 201

# Atualizar um profissional
@profissionais_bp.route('/<int:id>', methods=['PUT'])
def atualizar_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    dados = request.get_json()
    profissional.nome = dados.get('nome', profissional.nome)
    profissional.id_especialidade = dados.get('id_especialidade', profissional.id_especialidade)
    profissional.registro_profissional = dados.get('registro_profissional', profissional.registro_profissional)
    profissional.telefone = dados.get('telefone', profissional.telefone)
    profissional.email = dados.get('email', profissional.email)
    profissional.endereco = dados.get('endereco', profissional.endereco)
    db.session.commit()
    return jsonify(profissional.to_dict())

# Excluir um profissional
@profissionais_bp.route('/<int:id>', methods=['DELETE'])
def excluir_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    db.session.delete(profissional)
    db.session.commit()
    return jsonify({'mensagem': 'Profissional excluído com sucesso'}), 200