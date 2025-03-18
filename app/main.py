from dotenv import load_dotenv
load_dotenv()
from services import cliente_service 
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logger.info('Processamento Iniciado')

    dir_arquivo = "app/data/base_teste.txt"
    
    linhas_importadas = cliente_service.importar_clientes_txt(dir_arquivo)
    
    logger.info(f'Processamento finalizado - {linhas_importadas} foram importadas.')


if __name__ == '__main__':
    main();