import logging
import pandas as pd
from models.cliente import Cliente
from validate_docbr import CPF

logger = logging.getLogger(__name__)

def converter_para_dataframe(dir_arquivo: str) -> pd.DataFrame:
    '''
    Converte um arquivo de texto para um DataFrame do pandas.

    O arquivo de texto contém informações de clientes e é lido e convertido para um DataFrame, com colunas correspondentes ao modelo `Cliente`.
    A função também realiza conversões de tipos de dados e formatação de CPF.

    Parâmetros:
    ----------
    dir_arquivo : str
        Caminho para o arquivo de texto contendo os dados a serem convertidos.

    Retorno:
    -------
    pd.DataFrame
        DataFrame contendo os dados do arquivo, com colunas ajustadas conforme o modelo `Cliente`, e com CPF formatado.
        Retorna `None` caso ocorra algum erro durante a conversão.

    Exceções Tratadas:
    -----------------
    - Caso ocorra qualquer exceção durante a conversão, um erro é registrado no log e a função retorna `None`.
    
    Exemplo de Uso:
    --------------
    df = converter_para_dataframe('caminho/para/arquivo.txt')

    Ações Realizadas:
    ----------------
    1. Lê o arquivo de texto e mapeia as colunas de acordo com o modelo `Cliente`.
    2. Converte valores monetários ('ticket_medio', 'ticket_medio_ultima_compra') de string para float.
    3. Formata o campo de CPF para incluir a máscara caso o CPF esteja sem formatação.
    4. Registra logs das etapas da conversão, incluindo o número total de registros convertidos.
    '''
    
    # Pego aqui os nomes das colunas para igualar com a base de dados na extracao do arquivo txt
    colunas_cliente_model = [ coluna for coluna in Cliente.__dict__.keys() if not '__' in coluna and not '_sa_class_manager' in coluna]
    cpf = CPF()

    logger.info('Iniciando conversão do arquivo para dataframe')

    try:
        df = pd.read_csv(dir_arquivo, sep=r'\s{2,}', names=colunas_cliente_model, header=None, skiprows=1, engine='python')

        # Converto os campos de valores em float
        df['ticket_medio'] = df['ticket_medio'].str.replace(',', '.').astype(float)
        df['ticket_medio_ultima_compra'] = df['ticket_medio_ultima_compra'].str.replace(',', '.').astype(float)

        # Padronizando a mascara de cpf para os valores que não vieram formatados
        df['cpf'] = df.apply(lambda c: cpf.mask(str(c['cpf'])) if '.' not in c['cpf'] else c['cpf'], axis=1)
        
        logger.info(f'Total de {df.shape[0]} convertidos.')

        return df
    except Exception as err:
        logger.error(f'Erro não esperado: {err=}, {type(err)=}')
        return None
    finally:
        logger.info('Conversão finalizada')





    
