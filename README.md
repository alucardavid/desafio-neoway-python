# Desafio Neoway Python

Este projeto é um exemplo de aplicação Python que utiliza SQLAlchemy para interagir com um banco de dados PostgreSQL. Ele inclui testes automatizados usando `pytest` e um pipeline de CI/CD configurado com GitHub Actions para executar testes e construir uma imagem Docker.

## Requisitos

- Python 3.13 ou superior
- Docker Desktop
- Docker Compose 
- Git

## Configuração do Ambiente

### 1. Instalar Docker Desktop

Baixe e instale o Docker Desktop para sua plataforma (Windows ou macOS) a partir do site oficial:

- [Docker Desktop para Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module&_gl=1*1k2fn5m*_gcl_au*NDc5MDI2NDMwLjE3NDIzMzY4MTQ.*_ga*Mzk1MzUwMzY5LjE3NDIzMjk2MDg.*_ga_XJWPQMJYHQ*MTc0MjMzNjgxNC4yLjEuMTc0MjMzNjg2OS41LjAuMA..)
- [Docker Desktop para macOS](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module&_gl=1*17basq4*_gcl_au*NDc5MDI2NDMwLjE3NDIzMzY4MTQ.*_ga*Mzk1MzUwMzY5LjE3NDIzMjk2MDg.*_ga_XJWPQMJYHQ*MTc0MjMzNjgxNC4yLjEuMTc0MjMzNjg2OS41LjAuMA..)
- [Docker Desktop para Linux](https://docs.docker.com/desktop/setup/install/linux/)

Após a instalação, inicie o Docker Desktop e certifique-se de que ele está em execução.

### 2. Clonar o Repositório

Clone o repositório para sua máquina local:

```sh
git clone https://github.com/alucardavid/desafio-neoway-python.git
cd desafio-neoway-python

```

### 3. Executar a Aplicação com Docker Compose

Para iniciar a aplicação com Docker Compose, use o seguinte comando:

```sh
docker-compose up -d
```

Isso irá baixar a imagem mais recente do Docker Hub e iniciar a aplicação.

## Documentação do Projeto

### Arquitetura do Projeto

A arquitetura do projeto segue uma estrutura modular, dividida em camadas para facilitar a manutenção e a escalabilidade. As principais camadas são:

1. **Camada de Modelos**: Contém as definições dos modelos de dados usados pelo SQLAlchemy.
2. **Camada de Banco de Dados**: Contém a lógica de interação com o banco de dados, incluindo a criação de tabelas e a persistência de dados.
3. **Camada de Serviços**: Contém a lógica de negócios e as operações de validação.
4. **Camada de Utilitários**: Contém funções auxiliares, como a conversão de arquivos para DataFrames.

### Estrutura do Projeto

```sh
.
├── app
│   ├── data
│   │   ├── base_pyteste.txt
│   │   └── base_teste.txt
│   ├── database
│   │   ├── base.py
│   │   └── clientes_db.py
│   ├── models
│   │   └── cliente.py
│   ├── services
│   │   └── cliente_service.py
│   ├── utils
│   │   └── conversor_arquivo.py
│   └── main.py
├── tests
│   ├── test_clientes.py
│   ├── conftest.py
│   └── test_conversao.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

```

### Principais Funcionalidades

#### 1. clientes_db.py

- `criar_tabelas`: Cria as tabelas necessárias no banco de dados se ainda não existirem.
- `salvar_clientes`: Salva os dados de clientes no banco de dados a partir de um DataFrame.

#### 2. cliente.py

- Define o modelo `Cliente` usado pelo SQLAlchemy para mapear a tabela clientes.

#### 3. cliente_service.py

- `validar_clientes`: Valida os dados dos clientes.

#### 4. conversor_arquivo.py

- `converter_para_dataframe`: Converte um arquivo de texto em um DataFrame do pandas.

### Exemplos de Uso

#### 1. Criar Tabelas

```python
from app.database.clientes_db import criar_tabelas
criar_tabelas()
```

#### 2. Salvar Clientes

```python
from app.database.clientes_db import salvar_clientes
from app.utils.conversor_arquivo import converter_para_dataframe

df_clientes = converter_para_dataframe('data/base_pyteste.txt')
clientes_validados = validar_clientes(df_clientes)
salvar_clientes(clientes_validados)
```

#### 3. Validar Clientes

```python
from app.services.cliente_service import validar_clientes
from app.utils.conversor_arquivo import converter_para_dataframe

df_clientes = converter_para_dataframe('data/base_pyteste.txt')
clientes_validados = validar_clientes(df_clientes)
```

### Base de Dados

#### Criação da Tabela `Clientes` via SQLAlchemy

Este documento descreve como a tabela `Clientes` é criada usando SQLAlchemy, incluindo a definição do modelo e os tipos de dados utilizados.

#### Definição do Modelo `Cliente`

A tabela `Clientes` é definida no arquivo `cliente.py` dentro do diretório `models`. Aqui está a definição do modelo:

```python
from database.base import Base
from sqlalchemy import Column, String, Integer, Date, Numeric

class Cliente(Base):
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
```

#### Tipos de Dados

- **`cpf`**: Tipo `String(18)`. Este campo é a chave primária da tabela e é usado para identificar unicamente cada cliente. O tamanho máximo é 18 caracteres.
- **`private`**: Tipo `Integer`. Este campo armazena um valor inteiro que indica se o cliente é privado.
- **`incompleto`**: Tipo `Integer`. Este campo armazena um valor inteiro que indica se os dados do cliente estão incompletos.
- **`data_ultima_compra`**: Tipo `Date`. Este campo armazena a data da última compra do cliente.
- **`ticket_medio`**: Tipo `Numeric(16, 2)`. Este campo armazena o valor médio das compras do cliente, com até 16 dígitos no total e 2 casas decimais.
- **`ticket_medio_ultima_compra`**: Tipo `Numeric(16, 2)`. Este campo armazena o valor médio da última compra do cliente, com até 16 dígitos no total e 2 casas decimais.
- **`loja_mais_frequente`**: Tipo `String(18)`. Este campo armazena o identificador da loja onde o cliente mais frequentemente realiza compras. O tamanho máximo é 18 caracteres.
- **`loja_da_ultima_compra`**: Tipo `String(18)`. Este campo armazena o identificador da loja onde o cliente realizou a última compra. O tamanho máximo é 18 caracteres.
- **`valido`**: Tipo `String(1)`. Este campo armazena um valor que indica se os dados do cliente são válidos. O tamanho máximo é 1 caractere.

#### Criação das Tabelas

A criação das tabelas é gerenciada pela função `criar_tabelas` no arquivo `clientes_db.py`. Esta função utiliza o SQLAlchemy para criar todas as tabelas mapeadas pelo ORM a partir do modelo `Base`.

```python
from sqlalchemy import create_engine
from database.base import Base
import os

engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")

def criar_tabelas():
    Base.metadata.create_all(engine, checkfirst=True)
```

#### Explicação da Função `criar_tabelas`

- **`create_engine`**: Cria uma conexão com o banco de dados PostgreSQL usando as variáveis de ambiente para obter as credenciais e o endereço do banco de dados.
- **`Base.metadata.create_all`**: Cria todas as tabelas definidas no modelo `Base` se elas ainda não existirem no banco de dados. O parametro `checkfirst=True` garante que as tabelas só serão criadas se ainda não existirem.

#### Executando a Criação das Tabelas

Para criar as tabelas no banco de dados, você pode chamar a função `criar_tabelas` diretamente na aplicação:

```python
from app.database.clientes_db import criar_tabelas

criar_tabelas()
```

Isso garantirá que todas as tabelas definidas no modelo `Base` sejam criadas no banco de dados.

#### DDL

```sql
-- public.clientes definição

-- Drop table

-- DROP TABLE public.clientes;

CREATE TABLE public.clientes (
	cpf varchar(18) NOT NULL,
	private int4 NULL,
	incompleto int4 NULL,
	data_ultima_compra date NULL,
	ticket_medio numeric(16, 2) NULL,
	ticket_medio_ultima_compra numeric(16, 2) NULL,
	loja_mais_frequente varchar(18) NULL,
	loja_da_ultima_compra varchar(18) NULL,
	valido varchar(1) NULL,
	CONSTRAINT clientes_pkey PRIMARY KEY (cpf)
);

```


