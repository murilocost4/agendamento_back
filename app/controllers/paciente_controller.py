from flask import Blueprint, request, jsonify
from app import db
from app.models import Paciente
from datetime import datetime

paciente_bp = Blueprint('paciente', __name__)

# Função para criar um novo paciente
@paciente_bp.route('/pacientes', methods=['POST'])
def create_paciente():
    data = request.get_json()
    
    nome = data['nome']
    cpf = data['cpf']
    rg = data['rg']
    data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d')
    telefone = data['telefone']
    email = data['email']
    endereco = data['endereco']
    contrato = data['contrato']
    
    novo_paciente = Paciente(
        nome=nome,
        cpf=cpf,
        rg=rg,
        data_nascimento=data_nascimento,
        telefone=telefone,
        email=email,
        endereco=endereco,
        contrato=contrato
    )
    
    db.session.add(novo_paciente)
    db.session.commit()
    
    return jsonify({"message": "Paciente criado com sucesso!"}), 201


# Rota para listar todos os pacientes
@paciente_bp.route('/pacientes', methods=['GET'])
def get_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([paciente.to_dict() for paciente in pacientes])

# Rota para pegar um paciente específico
@paciente_bp.route('/pacientes/<int:id>', methods=['GET'])
def get_paciente(id):
    paciente = Paciente.query.get(id)
    if paciente is None:
        return jsonify({'message': 'Paciente não encontrado'}), 404
    return jsonify(paciente.to_dict())

# Rota para atualizar um paciente
@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def update_paciente(id):
    paciente = Paciente.query.get(id)
    if paciente is None:
        return jsonify({'message': 'Paciente não encontrado'}), 404
    
    data = request.get_json()
    
    paciente.nome = data.get('nome', paciente.nome)
    paciente.cpf = data.get('cpf', paciente.cpf)
    paciente.rg = data.get('rg', paciente.rg)
    paciente.data_nascimento = data.get('data_nascimento', paciente.data_nascimento)
    paciente.telefone = data.get('telefone', paciente.telefone)
    paciente.email = data.get('email', paciente.email)
    paciente.endereco = data.get('endereco', paciente.endereco)
    paciente.contrato = data.get('contrato', paciente.contrato)
    
    db.session.commit()
    
    return jsonify({'message': 'Paciente atualizado com sucesso', 'paciente': paciente.to_dict()})

# Rota para deletar um paciente
@paciente_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def delete_paciente(id):
    paciente = Paciente.query.get(id)
    if paciente is None:
        return jsonify({'message': 'Paciente não encontrado'}), 404
    
    db.session.delete(paciente)
    db.session.commit()
    
    return jsonify({'message': 'Paciente deletado com sucesso'})