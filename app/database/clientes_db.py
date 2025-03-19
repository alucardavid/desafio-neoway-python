import logging
from pandas import DataFrame
from sqlalchemy import create_engine
from models.cliente import Cliente
from database.base import Base
import os

logger = logging.getLogger(__name__)

engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")

def criar_tabelas():
    '''
    Cria as tabelas necessárias no banco de dados se ainda não existirem.

    Utiliza a configuração do SQLAlchemy para criar todas as tabelas mapeadas pelo ORM a partir do modelo `Base`.
    
    Ações Realizadas:
    -----------------
    1. Verifica se as tabelas definidas no modelo `Base` já existem no banco de dados.
    2. Cria as tabelas se elas ainda não existirem.

    Exemplo de Uso:
    ---------------
    criar_tabelas()
    '''
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine, checkfirst=False)

def salvar_clientes(clientes: DataFrame) -> int: 
    '''
    Salva os dados de clientes no banco de dados.

    A função insere os dados de um DataFrame de clientes na tabela 'clientes' do banco de dados.
    Antes de salvar, verifica se as tabelas estão criadas e, se necessário, cria as tabelas.

    Parâmetros:
    -----------
    clientes : pandas.DataFrame
        DataFrame contendo os dados dos clientes que devem ser persistidos no banco de dados.

    Retorno:
    --------
    int
        Número de linhas salvas no banco de dados.
        Retorna `None` em caso de erro durante a operação.

    Ações Realizadas:
    -----------------
    1. Cria as tabelas no banco de dados, caso não existam, utilizando a função `criar_tabelas`.
    2. Insere os dados do DataFrame na tabela 'clientes'.
    3. Registra logs detalhados durante o processo, incluindo o número de linhas salvas.

    Exceções Tratadas:
    -----------------
    - Qualquer exceção durante o processo de inserção no banco de dados será capturada, registrada no log, e a função retornará `None`.

    Exemplo de Uso:
    ---------------
    linhas_salvas = salvar_clientes(clientes_dataframe)
    '''

    logger.info('Iniciando a persistencia dos clientes na base de dados.')

    criar_tabelas()

    try:
        clientes.to_sql('clientes', engine, if_exists='append', index=False)
        logger.info(f'Foi salvo na base de dados um total de {clientes.shape[0]}.')
        return clientes.shape[0]
    except Exception as err:
        logger.error(f'Erro não esperado: {err=}, {type(err)=}')
        return None
    finally:
        logger.info('A persistência dos clientes na base de dados foi concluída.')


    

    

    