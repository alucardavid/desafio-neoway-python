from database.base import Base
from sqlalchemy import Column, String, Integer, Date, Numeric

class Cliente(Base):
    """
    Modelo de dados que representa a tabela 'clientes' no banco de dados.

    Esta classe utiliza o SQLAlchemy ORM para mapear a tabela 'clientes' e suas colunas
    no banco de dados. Cada instância desta classe representa um registro na tabela 'clientes'.
    
    Tabela:
    -------
    'clientes' no banco de dados.

    Exemplo de Uso:
    ---------------
    cliente = Cliente(
        cpf='123.456.789-00',
        private=1,
        incompleto=0,
        data_ultima_compra='2023-03-15',
        ticket_medio=150.75,
        ticket_medio_ultima_compra=120.50,
        loja_mais_frequente='Loja A',
        loja_da_ultima_compra='Loja B',
        valido='s'
    )
    """
    __tablename__ = 'clientes'

    cpf = Column(String(18), primary_key=True, )
    private = Column(Integer)
    incompleto = Column(Integer)
    data_ultima_compra = Column(Date)
    ticket_medio = Column(Numeric(16, 2))
    ticket_medio_ultima_compra = Column(Numeric(16, 2))
    loja_mais_frequente = Column(String(18))
    loja_da_ultima_compra = Column(String(18))
    valido = Column(String(1))

