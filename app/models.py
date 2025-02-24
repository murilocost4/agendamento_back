from app import db
from datetime import datetime

class Convenio(db.Model):
    __tablename__ = 'convenios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_convenio = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Convenio {self.nome_convenio}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_convenio': self.nome_convenio
        }
    
class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado_civil = db.Column(db.Enum('solteiro', 'casado', 'divorciado', 'viúvo'), nullable=False)
    profissao = db.Column(db.String(100), nullable=True)

    # Relacionamento com convenios
    convenios = db.relationship('Convenio', secondary='paciente_convenio', backref='pacientes')

    def __repr__(self):
        return f'<Paciente {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'numero': self.numero,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado_civil': self.estado_civil,
            'profissao': self.profissao
        }
    
class PacienteConvenio(db.Model):
    __tablename__ = 'paciente_convenio'

    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), primary_key=True)
    id_convenio = db.Column(db.Integer, db.ForeignKey('convenios.id'), primary_key=True)

    def __repr__(self):
        return f'<PacienteConvenio {self.id_paciente}-{self.id_convenio}>'
    
class Especialidade(db.Model):
    __tablename__ = 'especialidades'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_especialidade = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Especialidade {self.nome_especialidade}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_especialidade': self.nome_especialidade
        }
    
class Profissional(db.Model):
    __tablename__ = 'profissionais'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    id_especialidade = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    registro_profissional = db.Column(db.String(50), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)

    # Relacionamento com especialidade
    especialidade = db.relationship('Especialidade', backref='profissionais')
    # Relacionamento com clinicas
    clinicas = db.relationship('Clinica', secondary='clinica_profissional', backref='profissionais')

    def __repr__(self):
        return f'<Profissional {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'id_especialidade': self.id_especialidade,
            'registro_profissional': self.registro_profissional,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco
        }
    
class Clinica(db.Model):
    __tablename__ = 'clinicas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    whatsapp = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Clinica {self.descricao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'cnpj': self.cnpj,
            'telefone': self.telefone,
            'whatsapp': self.whatsapp,
            'email': self.email,
            'endereco': self.endereco
        }
    
class ClinicaProfissional(db.Model):
    __tablename__ = 'clinica_profissional'

    id_clinica = db.Column(db.Integer, db.ForeignKey('clinicas.id'), primary_key=True)
    id_profissional = db.Column(db.Integer, db.ForeignKey('profissionais.id'), primary_key=True)

    def __repr__(self):
        return f'<ClinicaProfissional {self.id_clinica}-{self.id_profissional}>'
    
class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.Integer, nullable=False)  # 1 para consulta, 2 para exame
    descricao = db.Column(db.Text, nullable=True)
    id_profissional = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=True)
    id_clinica = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=True)
    preparo = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    profissional = db.relationship('Profissional', backref='servicos')
    clinica = db.relationship('Clinica', backref='servicos')

    def __repr__(self):
        return f'<Servico {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'id_profissional': self.id_profissional,
            'id_clinica': self.id_clinica,
            'valor': str(self.valor) if self.valor else None,
            'preparo': self.preparo,
            'observacoes': self.observacoes
        }
    
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_solicitacao = db.Column(db.DateTime, nullable=False)
    id_solicitante = db.Column(db.Integer, nullable=False)  # Pode ser paciente ou profissional
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    id_profissional = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=True)
    id_clinica = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=True)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=True)
    status = db.Column(db.Integer, nullable=False)  # 0 - pendente, 1 - confirmado, etc.

    # Relacionamentos
    paciente = db.relationship('Paciente', backref='agendamentos')
    servico = db.relationship('Servico', backref='agendamentos')
    profissional = db.relationship('Profissional', backref='agendamentos')
    clinica = db.relationship('Clinica', backref='agendamentos')

    def __repr__(self):
        return f'<Agendamento {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'data_solicitacao': self.data_solicitacao.strftime('%Y-%m-%d %H:%M:%S'),
            'id_solicitante': self.id_solicitante,
            'id_paciente': self.id_paciente,
            'id_servico': self.id_servico,
            'id_profissional': self.id_profissional,
            'id_clinica': self.id_clinica,
            'data_agendamento': self.data_agendamento.strftime('%Y-%m-%d %H:%M:%S'),
            'horario': self.horario.strftime('%H:%M:%S'),
            'valor': str(self.valor) if self.valor else None,
            'status': self.status
        }
    
from app import db

class Especialidade(db.Model):
    __tablename__ = 'especialidades'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_especialidade = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Especialidade {self.nome_especialidade}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_especialidade': self.nome_especialidade
        }