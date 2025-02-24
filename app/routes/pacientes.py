from flask import Blueprint, request, jsonify
from flask_cors import cross_origin  # Importe o cross_origin
from app.models import Paciente, db
from datetime import datetime

pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/api/pacientes')

# Listar todos os pacientes
@pacientes_bp.route('', methods=['GET'], strict_slashes=False)
@cross_origin()  # Habilita CORS para esta rota
def listar_pacientes():
    try:
        pacientes = Paciente.query.all()
        return jsonify([paciente.to_dict() for paciente in pacientes])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obter um paciente por ID
@pacientes_bp.route('/<int:id>', methods=['GET'])
@cross_origin()  # Habilita CORS para esta rota
def obter_paciente(id):
    try:
        paciente = Paciente.query.get_or_404(id)
        return jsonify(paciente.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Criar um novo paciente
@pacientes_bp.route('', methods=['POST'], strict_slashes=False)
@cross_origin()  # Habilita CORS para esta rota
def criar_paciente():
    try:
        dados = request.get_json()
        novo_paciente = Paciente(
            nome=dados['nome'],
            cpf=dados['cpf'],
            data_nascimento=datetime.strptime(dados['data_nascimento'], '%Y-%m-%d'),
            telefone=dados.get('telefone'),
            email=dados.get('email'),
            endereco=dados.get('endereco'),
            numero=dados.get('numero'),
            bairro=dados.get('bairro'),
            cidade=dados.get('cidade'),
            estado_civil=dados['estado_civil'],
            profissao=dados.get('profissao')
        )
        db.session.add(novo_paciente)
        db.session.commit()
        return jsonify(novo_paciente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Atualizar um paciente
@pacientes_bp.route('/<int:id>', methods=['PUT'])
@cross_origin()  # Habilita CORS para esta rota
def atualizar_paciente(id):
    try:
        paciente = Paciente.query.get_or_404(id)
        dados = request.get_json()
        paciente.nome = dados.get('nome', paciente.nome)
        paciente.cpf = dados.get('cpf', paciente.cpf)
        paciente.data_nascimento = datetime.strptime(dados.get('data_nascimento', paciente.data_nascimento.strftime('%Y-%m-%d')), '%Y-%m-%d')
        paciente.telefone = dados.get('telefone', paciente.telefone)
        paciente.email = dados.get('email', paciente.email)
        paciente.endereco = dados.get('endereco', paciente.endereco)
        paciente.numero = dados.get('numero', paciente.numero)
        paciente.bairro = dados.get('bairro', paciente.bairro)
        paciente.cidade = dados.get('cidade', paciente.cidade)
        paciente.estado_civil = dados.get('estado_civil', paciente.estado_civil)
        paciente.profissao = dados.get('profissao', paciente.profissao)
        db.session.commit()
        return jsonify(paciente.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Excluir um paciente
@pacientes_bp.route('/<int:id>', methods=['DELETE'])
@cross_origin()  # Habilita CORS para esta rota
def excluir_paciente(id):
    try:
        paciente = Paciente.query.get_or_404(id)
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'mensagem': 'Paciente excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500