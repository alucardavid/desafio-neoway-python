import pytest
from app.database.clientes_db import salvar_clientes
from app.utils.conversor_arquivo import converter_para_dataframe
from app.services.cliente_service import validar_clientes

@pytest.fixture
def mock_engine(mocker):
    return mocker.patch('app.database.clientes_db.engine')

@pytest.fixture
def mock_criar_tabelas(mocker):
    return mocker.patch('app.database.clientes_db.criar_tabelas')

def test_validar_clientes():
    # Converte o arquivo em dataframe
    df_clientes = converter_para_dataframe('app/data/base_pyteste.txt')

    # Chamado o metodo para validar os clientes
    clientes_validados = validar_clientes(df_clientes)

    # Verifica se 
    assert len(clientes_validados) == len(df_clientes)


def test_salvar_clientes(mock_engine, mock_criar_tabelas, mocker):
    # Aqui crio um dataframe com o arquivo para teste
    clientes = converter_para_dataframe('app/data/base_pyteste.txt')

    # Mock do método to_sql
    mock_to_sql = mocker.patch.object(clientes, 'to_sql', return_value=len(clientes))

    # Chama a função a ser testada
    linhas_salvas = salvar_clientes(clientes)

    # Verifica se as tabelas foram criadas
    mock_criar_tabelas.assert_called_once()

    # Verifica se os dados foram salvos no banco de dados
    mock_to_sql.assert_called_once_with('clientes', mock_engine, if_exists='append', index=False)

    # Verifica se o número de linhas salvas está correto
    assert linhas_salvas == len(clientes)
