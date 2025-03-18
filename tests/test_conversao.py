from app.utils.conversor_arquivo import converter_para_dataframe

def test_converter_arquivo():
    df = converter_para_dataframe('app/data/base_pyteste.txt')
    assert len(df) > 0

