from app import db
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = 'paciente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(20), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)
    contrato = db.Column(db.String(9), nullable=True)

    # Relacionamento com agendamentos
    agendamentos = db.relationship('Agendamento', backref='paciente', lazy=True)

    def __init__(self, nome, cpf, rg, data_nascimento, telefone=None, email=None, endereco=None, contrato=None):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.contrato = contrato

    def __repr__(self):
        return f'<Paciente {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'rg': self.rg,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'contrato': self.contrato
        }


class Profissional(db.Model):
    __tablename__ = 'profissionais'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(50), unique=True, nullable=False)
    tipo_contrato = db.Column(db.Enum('autonomo', 'contratado', 'conveniado'), nullable=False)
    disponibilidade = db.Column(db.String(255))
    valor_consulta = db.Column(db.Numeric(10, 2))
    valor_exame = db.Column(db.Numeric(10, 2))

    # Relacionamento com agendamentos
    agendamentos = db.relationship('Agendamento', backref='profissional', lazy=True)

    def __repr__(self):
        return f'<Profissional {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'especialidade': self.especialidade,
            'crm': self.crm,
            'tipo_contrato': self.tipo_contrato,
            'disponibilidade': self.disponibilidade,
            'valor_consulta': str(self.valor_consulta) if self.valor_consulta else None,
            'valor_exame': str(self.valor_exame) if self.valor_exame else None
        }


class Clinica(db.Model):
    __tablename__ = 'clinicas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    endereco = db.Column(db.String(255))
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100))

    # Relacionamento com agendamentos
    agendamentos = db.relationship('Agendamento', backref='clinica', lazy=True)

    def __repr__(self):
        return f'<Clinica {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email
        }


class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_servico = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    tipo_servico = db.Column(db.Enum('consulta', 'exame'), nullable=False)

    # Relacionamento com agendamentos
    agendamentos = db.relationship('Agendamento', backref='servico', lazy=True)

    def __repr__(self):
        return f'<Servico {self.nome_servico}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_servico': self.nome_servico,
            'descricao': self.descricao,
            'tipo_servico': self.tipo_servico
        }

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    id_profissional = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=True)
    id_clinica = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=True)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pendente', 'confirmado', 'realizado', 'cancelado'), default='pendente', nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=True)
    forma_pagamento = db.Column(db.Enum('credito', 'debito', 'dinheiro', 'pix'), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos

    def __init__(self, id_paciente, id_servico, data_agendamento, forma_pagamento, id_profissional=None, id_clinica=None, status='pendente', valor=None, observacoes=None):
        self.id_paciente = id_paciente
        self.id_profissional = id_profissional
        self.id_clinica = id_clinica
        self.id_servico = id_servico
        self.data_agendamento = data_agendamento
        self.status = status
        self.valor = valor
        self.forma_pagamento = forma_pagamento
        self.observacoes = observacoes

    def __repr__(self):
        return f'<Agendamento {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_paciente': self.id_paciente,
            'id_profissional': self.id_profissional,
            'id_clinica': self.id_clinica,
            'id_servico': self.id_servico,
            'data_agendamento': self.data_agendamento.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'valor': str(self.valor) if self.valor else None,
            'forma_pagamento': self.forma_pagamento,
            'observacoes': self.observacoes
        }