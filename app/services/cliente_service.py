import pandas as pd
import logging
from pandas import DataFrame
from utils import conversor_arquivo
from database import clientes_db as db
from validate_docbr import CPF, CNPJ

logger = logging.getLogger(__name__)
pd.options.mode.chained_assignment = None

def importar_clientes_txt(dir_arquivo: str) -> int:
    '''
    Importa um arquivo de clientes no formato de texto para o banco de dados.

    Esta função realiza a conversão de um arquivo de clientes em um DataFrame, valida os dados
    e persiste as informações no banco de dados se os dados forem válidos.

    Parâmetros:
    -----------
    dir_arquivo : str
        Caminho para o arquivo de texto contendo os dados dos clientes.

    Retorno:
    --------
    None
        A função não retorna nenhum valor, mas registra logs de todas as etapas.
        Se ocorrerem erros durante o processo de conversão ou validação, o fluxo é interrompido e a função retorna `None`.

    Ações Realizadas:
    -----------------
    1. Verifica se o caminho do arquivo foi fornecido.
    2. Converte o arquivo para um DataFrame utilizando a função `converter_para_dataframe`.
    3. Valida os clientes utilizando a função `validar_clientes`.
    4. Salva os dados validados no banco de dados.
    5. Registra logs detalhados durante o processo.

    Exceções Tratadas:
    -----------------
    - Arquivo inválido ou vazio: A função retorna `None` e registra um log.
    - Erros durante a conversão ou validação dos dados: A função retorna `None` e registra um log.

    Exemplo de Uso:
    ---------------
    importar_clientes_txt('caminho/para/arquivo_clientes.txt')
    '''

    logger.info('Iniciando importação do arquivo de clientes')

    if dir_arquivo is None:
        logger.info('É necessario passar um arquivo valido para a importação dos dados.')
        return None

    # Conversão do arquivo para um dataframe pandas
    clientes_dataframe = conversor_arquivo.converter_para_dataframe(dir_arquivo)

    if clientes_dataframe is None or clientes_dataframe.shape[0] == 0:  
        logger.info('Arquivo vazio ou ocorreu algum erro na conversão, verificar o arquivo txt') 
        return None

    clientes_validados = validar_clientes(clientes_dataframe)

    if clientes_validados is None or clientes_validados.shape[0] == 0:  
        logger.info('Apos a validação dos dados não foram encontrados cliente para salvar no banco de dados, finalizando importação.') 
        return None

    # Persistir as informações na base de dados e retorna a quantidade de linhas salvas
    linhas_salvas =  db.salvar_clientes(clientes_validados)
    logger.info('Importação do arquivo de clientes finalizada')

    return linhas_salvas

def validar_clientes(clientes: DataFrame):
    '''
    Valida os dados de clientes contidos em um DataFrame.

    A função valida os CPFs e CNPJs dos clientes, ajustando as entradas e aplicando
    regras de filtragem e formatação.

    Parâmetros:
    -----------
    clientes : pandas.DataFrame
        DataFrame contendo os dados dos clientes para validação.

    Retorno:
    --------
    pandas.DataFrame
        DataFrame com a coluna 'valido' indicando se os clientes passaram na validação ('s' para sim, 'n' para não).
        Retorna `None` em caso de erro durante a validação.

    Ações Realizadas:
    -----------------
    1. Filtra clientes cujo CPF tenha menos de 19 caracteres.
    2. Aplica a validação do CPF e do CNPJ, marcando na coluna 'valido' se o cliente passou na validação.
    3. Se um erro ocorrer durante o processo, registra um log e retorna `None`.

    Exceções Tratadas:
    -----------------
    - Qualquer exceção durante o processo de validação será capturada e registrada, retornando `None`.

    Exemplo de Uso:
    ---------------
    df_validado = validar_clientes(clientes_dataframe)
    '''
    
    logger.info('Iniciando validação dos clientes')

    cpf = CPF()
    cnpj = CNPJ()

    try:
        # Aqui eu filtro para os cpfs com caracteres menor que 19
        clientes = clientes[clientes.apply(lambda c: len(c['cpf']) <= 18, axis=1)]
        
        # Aplico a validação para cpf e cnpj
        clientes['valido'] = clientes.apply(lambda c: 's' if cpf.validate(str(c['cpf'])) else 'n', axis=1, )
        clientes['valido'] = clientes.apply(lambda c: 's' if pd.isnull(c['loja_mais_frequente']) else 's' if cnpj.validate(c['loja_mais_frequente']) else 'n', axis=1)
        clientes['valido'] = clientes.apply(lambda c: 's' if pd.isnull(c['loja_da_ultima_compra']) else 's' if cnpj.validate(c['loja_da_ultima_compra']) else 'n', axis=1)
        return clientes
    except Exception as err:
        logger.error(f'Unexpected {err=}, {type(err)=}')
        return None
    finally:
        logger.info('Finalizado validação dos clientes')


    



