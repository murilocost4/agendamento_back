from flask import Blueprint, request, jsonify
from app.models import Servico, db

servicos_bp = Blueprint('servicos', __name__, url_prefix='/api/servicos')

# Listar todos os serviços
@servicos_bp.route('/', methods=['GET'])
def listar_servicos():
    servicos = Servico.query.all()
    return jsonify([servico.to_dict() for servico in servicos])

# Obter um serviço por ID
@servicos_bp.route('/<int:id>', methods=['GET'])
def obter_servico(id):
    servico = Servico.query.get_or_404(id)
    return jsonify(servico.to_dict())

# Criar um novo serviço
@servicos_bp.route('/', methods=['POST'])
def criar_servico():
    dados = request.get_json()
    novo_servico = Servico(
        tipo=dados['tipo'],
        descricao=dados.get('descricao'),
        id_profissional=dados.get('id_profissional'),
        id_clinica=dados['id_clinica'],
        valor=dados.get('valor'),
        preparo=dados.get('preparo'),
        observacoes=dados.get('observacoes')
    )
    db.session.add(novo_servico)
    db.session.commit()
    return jsonify(novo_servico.to_dict()), 201

# Atualizar um serviço
@servicos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_servico(id):
    servico = Servico.query.get_or_404(id)
    dados = request.get_json()
    servico.tipo = dados.get('tipo', servico.tipo)
    servico.descricao = dados.get('descricao', servico.descricao)
    servico.id_profissional = dados.get('id_profissional', servico.id_profissional)
    servico.id_clinica = dados.get('id_clinica', servico.id_clinica)
    servico.valor = dados.get('valor', servico.valor)
    servico.preparo = dados.get('preparo', servico.preparo)
    servico.observacoes = dados.get('observacoes', servico.observacoes)
    db.session.commit()
    return jsonify(servico.to_dict())

# Excluir um serviço
@servicos_bp.route('/<int:id>', methods=['DELETE'])
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return jsonify({'mensagem': 'Serviço excluído com sucesso'}), 200