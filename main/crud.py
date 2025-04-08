from sqlalchemy import create_engine, Column, Integer, String, Date, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

# Define a enumeração para o status do histórico
class StatusHistorico(enum.Enum):
    PRONTO = "Pronto"
    ENTREGUE = "Entregue"
    SOLICITADO = "Solicitado"
    FALTA_DOCUMENTOS = "Falta Documentos"

# Define a classe base do SQLAlchemy
Base = declarative_base()

# Define a classe Aluno
class Aluno(Base):
    __tablename__ = 'alunos'

    numero_pasta = Column(Integer, primary_key=True, autoincrement=True)
    nome_aluno = Column(String(100), nullable=False)
    status_historico = Column(Enum(StatusHistorico), nullable=False)
    data_solicitacao = Column(Date, nullable=False)
    data_entrega = Column(Date, nullable=True)
    observacoes = Column(Text, nullable=True)
    ultima_serie_ano = Column(String(50), nullable=False)
    ultimo_ano_letivo = Column(Integer, nullable=False)

# Configura o banco de dados
engine = create_engine('sqlite:///escola.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Funções CRUD
def criar_aluno(nome, status, data_solicitacao, ultima_serie, ultimo_ano, observacoes=None, data_entrega=None):
    novo_aluno = Aluno(
        nome_aluno=nome,
        status_historico=status,
        data_solicitacao=data_solicitacao,
        data_entrega=data_entrega,
        observacoes=observacoes,
        ultima_serie_ano=ultima_serie,
        ultimo_ano_letivo=ultimo_ano
    )
    session.add(novo_aluno)
    session.commit()
    print("Aluno criado com sucesso!")

def ler_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f"ID: {aluno.numero_pasta}, Nome: {aluno.nome_aluno}, Status: {aluno.status_historico.value}")

def atualizar_aluno(numero_pasta, **kwargs):
    aluno = session.query(Aluno).filter_by(numero_pasta=numero_pasta).first()
    if aluno:
        for key, value in kwargs.items():
            if hasattr(aluno, key):
                setattr(aluno, key, value)
        session.commit()
        print("Aluno atualizado com sucesso!")
    else:
        print("Aluno não encontrado.")

def deletar_aluno(numero_pasta):
    aluno = session.query(Aluno).filter_by(numero_pasta=numero_pasta).first()
    if aluno:
        session.delete(aluno)
        session.commit()
        print("Aluno deletado com sucesso!")
    else:
        print("Aluno não encontrado.")

# Exemplo de uso
if __name__ == "__main__":
    # Criar um aluno
    criar_aluno(
        nome="Maria Silva",
        status=StatusHistorico.SOLICITADO,
        data_solicitacao="2025-04-08",
        ultima_serie="3° Ano",
        ultimo_ano=2024,
        observacoes="Aguardando documentos"
    )

    # Ler alunos
    ler_alunos()

    # Atualizar aluno
    atualizar_aluno(1, nome_aluno="Maria Aparecida Silva", status_historico=StatusHistorico.ENTREGUE)

    # Deletar aluno
    deletar_aluno(1)