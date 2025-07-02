# .coveragerc

```
[run]
source = .
omit = 
    */.venv/*
    */tests/*
    */test_*
    setup.py
    main.py
    */migrations/*
    */venv/*
    */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstract

[html]
directory = htmlcov
```

# .gitignore

```
.venv
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/

```

# .pytest_cache\.gitignore

```
# Created by pytest automatically.
*

```

# .pytest_cache\CACHEDIR.TAG

```TAG
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html

```

# .pytest_cache\README.md

```md
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

```

# .pytest_cache\v\cache\lastfailed

```
{
  "tests/test_usuario_repo.py": true
}
```

# .vscode\settings.json

```json
{
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```

# model\contrato_model.py

```py
from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Contrato:
    id: int
    valor: float 

    
```

# model\produto_model.py

```py
from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Produto:
    id: int
    nome: str
    preco: float
    quantidade: int
    descricao: str    
    
    
```

# model\servico_model.py

```py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Servico:
    id: int
    nome: str
    preco: float
    descricao: str    

    
```

# model\usuario_model.py

```py
from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome: str
    telefone: str
    email: str    
    senha_hash: Optional[str] = None
    tipo: str
    
```

# pytest.ini

```ini
[tool:pytest]
# Diretórios onde o pytest deve procurar por testes
testpaths = tests

# Padrões de arquivos de teste
python_files = test_*.py *_test.py

# Padrões de classes de teste
python_classes = Test*

# Padrões de funções de teste
python_functions = test_*

# Marcadores personalizados
markers =
    slow: marca testes que demoram para executar
    integration: marca testes de integração
    unit: marca testes unitários

# Opções padrão do pytest COM coverage
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --color=yes
    --tb=short
    --maxfail=1
    --strict-config
    --cov=.
    --cov-report=html
    --cov-report=term-missing:skip-covered
    --cov-config=.coveragerc

# Filtros de warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning

# Configuração de log
log_cli = false
log_cli_level = INFO

# Formato de saída mais limpo
console_output_style = progress
```

# repo\contrato_repo.py

```py
from typing import Optional
from util.database import obter_conexao
from sql.contrato_sql import *
from model.contrato_model import Contrato

def criar_tabela_contratos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de contratos
            cursor.execute(CRIAR_TABELA_CONTRATO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de contratos: {e}")
        # Retorna False indicando falha
        return False

def inserir_contrato(contrato: Contrato) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir contrato com todos os campos
        cursor.execute(INSERIR_CONTRATO, 
            (contrato.valor,))
        # Retorna o ID do contrato inserido
        return cursor.lastrowid

def atualizar_contrato(contrato: Contrato) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do contrato pelo ID
        cursor.execute(ATUALIZAR_CONTRATO, 
            (contrato.valor, contrato.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_tipo_contrato(id: int, tipo: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar tipo do contrato (0=serviço, 1=produto)
        cursor.execute(ATUALIZAR_TIPO_CONTRATO, (tipo, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)


def excluir_contrato(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar contrato pelo ID
        cursor.execute(EXCLUIR_CONTRATO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_contrato_por_id(id: int) -> Optional[Contrato]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar contrato pelo ID
        cursor.execute(OBTER_CONTRATO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Contrato com dados do banco
            return Contrato(
                id=resultado["id"],
                valor=resultado["valor"]
    # Retorna None se não encontrou usuário
    return None
            )
```

# repo\produto_repo.py

```py
from typing import Optional
from util.database import obter_conexao
from sql.produto_sql import *
from model.produto_model import Produto

def criar_tabela_produtos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de produtos
            cursor.execute(CRIAR_TABELA_PRODUTO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de produtos: {e}")
        # Retorna False indicando falha
        return False

def inserir_produto(produto: Produto) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir produto com todos os campos
        cursor.execute(INSERIR_PRODUTO, 
            (produto.nome, produto.preco, produto.quantidade, produto.descricao))
        # Retorna o ID do produto inserido
        return cursor.lastrowid        

def atualizar_produto(produto: Produto) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do produto pelo ID
        cursor.execute(ATUALIZAR_PRODUTO, 
            (produto.nome, produto.preco, produto.quantidade, produto.descricao, produto.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    

def excluir_produto(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar produto pelo ID
        cursor.execute(EXCLUIR_PRODUTO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_produto_por_id(id: int) -> Optional[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produto pelo ID
        cursor.execute(OBTER_PRODUTO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Produto com dados do banco
            return Produto(
                id=resultado["id"],
                nome=resultado["nome"],
                preco=resultado["preco"],
                quantidade=resultado["quantidade"],
                descricao=resultado["descricao"])
    # Retorna None se não encontrou produto
    return None

def obter_produto_por_nome(nome: str) -> Optional[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produto pelo nome
        cursor.execute(OBTER_PRODUTO_POR_NOME, (nome,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Produto com dados do banco
            return Produto(
                id=resultado["id"],
                nome=resultado["nome"],
                preco=resultado["preco"],
                quantidade=resultado["quantidade"],
                descricao=resultado["descricao"])
    # Retorna None se não encontrou produto
    return None

def obter_produtos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produtos com paginação
        cursor.execute(OBTER_PRODUTOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Produto a partir dos resultados
        return [Produtoo(
            id=resultado["id"],
            nome=resultado["nome"],
            preco=resultado["preco"],
            quantidade=resultado["quantidade"],
            descricao=resultado["descricao"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou produtos
    return []
```

# repo\servico_repo.py

```py
from typing import Optional
from util.database import obter_conexao
from sql.servico_sql import *
from model.servico_model import Servico

def criar_tabela_servicos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(criar_tabela_servicos)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de serviços: {e}")
        # Retorna False indicando falha
        return False

def inserir_servico(servico: Servico) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir serviço com todos os campos
        cursor.execute(INSERIR_SERVICO, 
            (servico.nome, servico.preco, servico.descricao))
        # Retorna o ID do serviço inserido
        return cursor.lastrowid        

def atualizar_servico(servico: Servico) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do serviço pelo ID
        cursor.execute(ATUALIZAR_SERVICO, 
            (servico.nome, servico.preco, servico.descricao, servico.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def atualizar_tipo_servico(id: int, tipo: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar tipo do usuário (0=comum, 1=admin)
        cursor.execute(ATUALIZAR_TIPO_SERVICO, (tipo, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_servico(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(EXCLUIR_SERVICO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_servico_por_id(id: int) -> Optional[Servico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar serviço pelo ID
        cursor.execute(OBTER_SERVICO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Servico com dados do banco
            return Servico(
                id=resultado["id"],
                nome=resultado["nome"],
                preco=resultado["preco"],
                descricao=resultado["descricao"]
            )
    # Retorna None se não encontrou serviço
    return None


    # Retorna None se não encontrou usuário
    return None

def obter_servicos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Servico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar serviços com paginação
        cursor.execute(obter_servicos_por_pagina, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Servico a partir dos resultados
        return [Servico(
            id=resultado["id"],
            nome=resultado["nome"],
            preco=resultado["preco"],
            descricao=resultado["descricao"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou serviços
    return []
```

# repo\usuario_repo.py

```py
from typing import Optional
from util.database import obter_conexao
from sql.usuario_sql import *
from model.usuario_model import Usuario

def criar_tabela_usuarios() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(CRIAR_TABELA_USUARIO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de usuários: {e}")
        # Retorna False indicando falha
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir usuário com todos os campos
        cursor.execute(INSERIR_USUARIO, 
            (usuario.nome, usuario.telefone, usuario.email, usuario.senha_hash, usuario.tipo))
        # Retorna o ID do usuário inserido
        return cursor.lastrowid        

def atualizar_usuario(usuario: Usuario) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(ATUALIZAR_USUARIO, 
            (usuario.nome, usuario.telefone, usuario.email, usuario.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def atualizar_senha_usuario(id: int, senha_hash: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar senha hash do usuário
        cursor.execute(ATUALIZAR_SENHA_USUARIO, (senha_hash, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_usuario(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(EXCLUIR_USUARIO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_usuario_por_id(id: int) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo ID
        cursor.execute(OBTER_USUARIO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    # Retorna None se não encontrou usuário
    return None

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo email
        cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    # Retorna None se não encontrou usuário
    return None

def obter_usuarios_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários com paginação
        cursor.execute(OBTER_USUARIOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            tipo=resultado["tipo"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []
```

# requirements.txt

```txt
fastapi[standard]
uvicorn[standard]
jinja2
Babel
python-multipart
itsdangerous

# Dependências de teste
pytest
pytest-asyncio
pytest-cov
```

# sql\contrato_sql.py

```py
CRIAR_TABELA_CONTRATO = """
CREATE TABLE IF NOT EXISTS servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,

"""

INSERIR_CONTRATO = """
INSERT INTO servico (valor)
VALUES (?);
"""

ATUALIZAR_CONTRATO= """
UPDATE servico
SET valor = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_CONTRATO = """
UPDATE servico
SET tipo = ?
WHERE id = ?;
"""



EXCLUIR_CONTRATO = """
DELETE FROM servico
WHERE id = ?;
"""

OBTER_CONTRATO_POR_ID = """
SELECT id, valor
FROM Contrato
WHERE id = ?;
"""




OBTER_CONTRATOS_POR_PAGINA = """
SELECT id, valor
FROM Contrato
ORDER BY id ASC
LIMIT ? OFFSET ?;
"""
```

# sql\prestador_sql.py

```py
CRIAR_TABELA_PRESTADOR = """
CREATE TABLE IF NOT EXISTS Prestador (
    id_prestador INTEGER PRIMARY,
    tipo_pessoa TEXT NOT NULL CHECK(tipo_pessoa IN ('FISICA', 'JURIDICA')),
    documento TEXT NOT NULL UNIQUE,
    FOREIGN KEY (id_prestador) REFERENCES Usuario(id);
"""

INSERIR_PRESTADOR = """
INSERT INTO Prestador(id_prestador, tipo_pessoa, documento)
VALUES (?, ?, ?);
"""

ATUALIZAR_PRESTADOR = """
UPDATE Prestador
SET tipo_pessoa = ?, documento = ?
WHERE id_prestador = ?;
"""

EXCLUIR_PRESTADOR = """
DELETE FROM Prestador
WHERE id_prestador = ?;
"""

OBTER_PRESTADOR_POR_ID = """
SELECT p.id_prestador, u.nome, u.telefone, u.email, u.senha_hash, p.tipo, p.tipo_pessoa, p.documento
FROM Prestador p
JOIN Usuario u ON p.id_prestador = u.id
WHERE p.id_prestador = ?;
"""

OBTER_PRESTADOR_POR_EMAIL = """
SELECT p.id_prestador, u.nome, u.telefone, u.email, u.senha_hash, p.tipo, p.tipo_pessoa, p.documento
FROM Prestador p
JOIN Usuario u ON p.id_prestador = u.id
WHERE u.email = ?;
"""

OBTER_PRESTADORES_POR_PAGINA = """
SELECT p.id_prestador, u.nome, u.telefone, u.email, u.senha_hash, p.tipo, p.tipo_pessoa, p.documento
FROM Prestador p
JOIN Usuario u ON p.id_prestador = u.id
ORDER BY u.nome ASC
LIMIT ? OFFSET ?;
"""
```

# sql\produto_sql.py

```py
CRIAR_TABELA_PRODUTO = """
CREATE TABLE IF NOT EXISTS Produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco FLOAT NOT NULL DEFAULT 0,
    quantidade INTEGER NOT NULL DEFAULT 0,
    descricao TEXT NOT NULL);
"""

INSERIR_PRODUTO = """
INSERT INTO Produto (nome, preco, quantidade, descricao)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_PRODUTO = """
UPDATE Produto
SET nome = ?, preco = ?, quantidade = ?, descricao = ?
WHERE id = ?;
"""

EXCLUIR_PRODUTO = """
DELETE FROM Produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_ID = """
SELECT id, nome, preco, quantidade, descricao
FROM Produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_NOME = """
SELECT id, nome, preco, quantidade, descricao
FROM Produto
WHERE email = ?;
"""

OBTER_PRODUTOS_POR_PAGINA = """
SELECT id, nome, preco, quantidade, descricao
FROM Produto
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""
```

# sql\servico_sql.py

```py
CRIAR_TABELA_SERVICO = """
CREATE TABLE IF NOT EXISTS servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL UNIQUE,

"""

INSERIR_SERVICO = """
INSERT INTO servico (nome, preco, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR_SERVICO= """
UPDATE servico
SET nome = ?, preco = ?, descricao = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_SERVICO = """
UPDATE servico
SET tipo = ?
WHERE id = ?;
"""



EXCLUIR_SERVICO = """
DELETE FROM servico
WHERE id = ?;
"""

OBTER_SERVICO_POR_ID = """
SELECT id, nome, preco, descricao
FROM Usuario
WHERE id = ?;
"""




OBTER_SERVICOS_POR_PAGINA = """
SELECT id, nome, preco, descricao
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""
```

# sql\usuario_sql.py

```py
CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('ADMIN', 'NOIVO', 'PRESTADOR', 'FORNECEDOR'));
"""

INSERIR_USUARIO = """
INSERT INTO Usuario (nome, telefone, email, senha_hash, tipo)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE Usuario
SET nome = ?, telefone = ?, email = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_USUARIO = """
UPDATE Usuario
SET tipo = ?
WHERE id = ?;
"""

ATUALIZAR_SENHA_USUARIO = """
UPDATE Usuario
SET senha_hash = ?
WHERE id = ?;
"""

EXCLUIR_USUARIO = """
DELETE FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT id, nome, telefone, email, senha_hash, tipo
FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT id, nome, telefone, email, senha_hash, tipo
FROM Usuario
WHERE email = ?;
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT id, nome, telefone, email, senha_hash, tipo
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""
```

# tests\__init__.py

```py

```

# tests\conftest.py

```py
from datetime import datetime
import pytest
import os
import sys
import tempfile

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def usuario_exemplo():
    # Cria um usuário de exemplo para os testes
    from model.usuario_model import Usuario
    usuario = Usuario(0, "Usuário Teste", "(28) 99999-0000", "usuario@email.com", "123456", "ADMIN")
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    # Cria uma lista de 10 usuários de exemplo para os testes
    tipos = ["ADMIN", "NOIVO", "PRESTADOR", "FORNECEDOR"]
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Usuário {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", tipos[i % 4])
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def servicos_exemplo():
    # Cria um serviço de exemplo para os testes
    from model.servico_model import Servico
    servico = Servico(0, "Serviço Teste", "Descrição do serviço", 100.0)
    return servico

@pytest.fixture
def lista_servicos_exemplo():
    # Cria uma lista de 10 serviços de exemplo para os testes
    from model.servico_model import Servico
    servicos = []
    for i in range(1, 11):
        servico = Servico(0, f"Serviço {i:02d}", f"Descrição do serviço {i:02d}", 100.0 * i)
        servicos.append(servico)
    return servicos

@pytest.fixture
def produto_exemplo():
    # Cria um produto de exemplo para os testes
    from model.produto_model import Produto
    produto = Produto(0, "Produto Teste", 19.99, 10, "Descrição do produto teste")
    return produto

@pytest.fixture
def lista_produtos_exemplo():  
    # Cria uma lista de 10 produtos de exemplo para os testes
    from model.produto_model import Produto
    produtos = []
    for i in range(1, 11):
        produto = Produto(0, f"Produto {i:02d}", 19.99 + i, 10 + i, f"Descrição do produto {i:02d}")
        produtos.append(produto)
    return produtos    
```

# tests\test_produto_repo.py

```py
from model.produto_model import Produto
from repo import produto_repo

class TestProdutoRepo:
    def test_criar_tabela_produtos(self, test_db):
        # Arrange
        # Act
        resultado = produto_repo.criar_tabela_produtos()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_produto(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Assert
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_db is not None, "O produto inserido não deveria ser None"
        assert produto_db.id == 1, "O produto inserido deveria ter um ID igual a 1"
        assert produto_db.nome == "Produto Teste", "O nome do produto inserido não confere"
        assert produto_db.preco == "19.99", "O preço do produto inserido não confere"
        assert produto_db.quantidade == "10", "A quantidade do produto inserido não confere"
        assert produto_db.descricao == "Descrição do produto teste", "A descrição do produto inserido não confere"

    def test_obter_produto_por_id_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()        
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        # Assert
        assert produto_db is not None, "O produto retornado deveria ser diferente de None"
        assert produto_db.id == id_produto_inserido, "O id do produto buscado deveria ser igual ao id do produto inserido"
        assert produto_db.nome == produto_exemplo.nome, "O nome do produto buscado deveria ser igual ao nome do produto inserido"
        assert produto_db.preco == produto_exemplo.preco, "O preço do produto buscado deveria ser igual ao preço do produto inserido"
        assert produto_db.quantidade == produto_exemplo.quantidade, "A quantidade do produto buscado deveria ser igual à quantidade do produto inserida"
        assert produto_db.descricao == produto_exemplo.descricao, "A descrição do produto buscado deveria ser igual à descrição do produto inserido"

    def test_obter_produto_por_id_inexistente(self, test_db):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        produto_db = produto_repo.obter_produto_por_id(999)
        # Assert
        assert produto_db is None, "O produto buscado com ID inexistente deveria retornar None"

    def test_obter_produto_por_nome_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        produto_db = produto_repo.obter_produto_por_nome(produto_exemplo.nome)
        # Assert
        assert produto_db is not None, "O produto buscado por nome deveria ser diferente de None"
        assert produto_db.id == id_produto_inserido, "O id do produto buscado por nome deveria ser igual ao id do produto inserido"
        assert produto_db.nome == produto_exemplo.nome, "O nome do produto buscado deveria ser igual ao nome do produto inserido"

    def test_obter_produto_por_nome_inexistente(self, test_db):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        produto_db = produto_repo.obter_produto_por_nome("Produto Inexistente")
        # Assert
        assert produto_db is None, "O produto buscado por nome inexistente deveria retornar None"

    def test_atualizar_produto_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        produto_inserido = produto_repo.obter_produto_por_id(id_produto_inserido)
        # Act
        produto_inserido.nome = "Produto Atualizado"
        produto_inserido.preco = "20.99"
        produto_inserido.quantidade = "15"
        produto_inserido.descricao = "Descrição do produto atualizado"
        resultado = produto_repo.atualizar_produto(produto_inserido)
        # Assert
        assert resultado == True, "A atualização do produto deveria retornar True"
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_db.nome == "Produto Atualizado", "O nome do produto atualizado não confere"
        assert produto_db.preco == "20.99", "O preço do produto atualizado não confere"
        assert produto_db.quantidade == "15", "A quantidade do produto atualizado não confere"
        assert produto_db.descricao == "Descrição do produto atualizado", "A descrição atualizada não confere"

    def test_atualizar_produto_inexistente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        produto_exemplo.id = 999  # ID que não existe
        # Act
        resultado = produto_repo.atualizar_produto(produto_exemplo)
        # Assert
        assert resultado == False, "A atualização de um produto inexistente deveria retornar False"

    def test_excluir_produto_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()        
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        resultado = produto_repo.excluir_produto(id_produto_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        produto_excluido = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_excluido is None, "O produto excluído deveria ser None"

    def test_excluir_produto_inexistente(self, test_db):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        resultado = produto_repo.excluir_produto(999)
        # Assert
        assert resultado == False, "A exclusão de um produto inexistente deveria retornar False"

    def test_atualizar_tipo_produto(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        resultado = produto_repo.atualizar_tipo_produto(id_produto_inserido, 1)
        # Assert
        assert resultado == True, "A atualização do tipo de produto deveria retornar True"
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_db.tipo == 1, "O tipo do produto atualizado não confere"

    def test_obter_produtos_por_pagina_primeira_pagina(self, test_db, lista_produtos_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        for produto in lista_produtos_exemplo:
            produto_repo.inserir_produto(produto)
        # Act
        pagina_produtos = produto_repo.obter_produtos_por_pagina(1, 4)
        # Assert
        assert len(pagina_produtos) == 4, "Deveria retornar 4 produtos na primeira página"
        assert all(isinstance(u, Produto) for u in pagina_produtos), "Todos os itens da página devem ser do tipo Produto"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id for u in pagina_produtos]
        assert ids_esperados == ids_retornados, "Os IDs dos produtos na primeira página não estão corretos"
    
    def test_obter_produtos_por_pagina_terceira_pagina(self, test_db, lista_produtos_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        for produto in lista_produtos_exemplo:
            produto_repo.inserir_produto(produto)
        # Act: busca a terceira página com 4 produtos por página
        pagina_produtos = produto_repo.obter_produtos_por_pagina(3, 4)
        # Assert: verifica se retornou a quantidade correta (2 produtos na terceira página)
        assert len(pagina_produtos) == 2, "Deveria retornar 2 produtos na terceira página"
        assert (isinstance(u, Produto) for u in pagina_produtos), "Todos os itens da página devem ser do tipo Produto"
```

# tests\test_servicos_repo.py

```py
from model.servico_model import Servico
from repo import servico_repo

class TestServicoRepo:
    def test_criar_tabela_servicos(self, test_db):
        # Arrange
        # Act
        resultado = servico_repo.criar_tabela_servicos()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_servico(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Assert
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_db is not None, "O serviço inserido não deveria ser None"
        assert servico_db.id == id_servico_inserido, "O serviço inserido deveria ter um ID igual ao retornado pela inserção"
        assert servico_db.nome == "Serviço Teste", "O nome do serviço inserido não confere"
        assert servico_db.descricao == "Descrição do serviço", "A descrição do serviço inserido não confere"
        assert servico_db.preco == 100.0, "O preço do serviço inserido não confere"
        assert servico_db.tipo == 0, "O tipo do serviço inserido não confere"

    def test_obter_servico_por_id_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        # Assert
        assert servico_db is not None, "O serviço retornado deveria ser diferente de None"
        assert servico_db.id == id_servico_inserido, "O id do serviço buscado deveria ser igual ao id do serviço inserido"
        assert servico_db.nome == servico_exemplo.nome, "O nome do serviço buscado deveria ser igual ao nome do serviço inserido"
        assert servico_db.descricao == servico_exemplo.descricao, "A descrição do serviço buscado deveria ser igual à descrição do serviço inserido"
        assert servico_db.preco == servico_exemplo.preco, "O preço do serviço buscado deveria ser igual ao preço do serviço inserido"
        assert servico_db.tipo == servico_exemplo.tipo, "O tipo do serviço buscado deveria ser igual ao tipo do serviço inserido"
        assert servico_db.tipo == servico_exemplo.tipo, "O tipo do serviço buscado deveria ser igual ao tipo do serviço inserido"

    def test_obter_servico_por_id_inexistente(self, test_db):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        servico_db = servico_repo.obter_servico_por_id(999)
        # Assert
        assert servico_db is None, "O serviço buscado com ID inexistente deveria retornar None"

    

    def test_atualizar_servico_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        servico_db.nome = "Serviço Atualizado"
        servico_db.descricao = "Descrição Atualizada"
        servico_db.preco = 150.0
        servico_db.tipo = 1
        resultado = servico_repo.atualizar_servico(servico_db)
        # Assert
        assert resultado == True, "A atualização do serviço deveria retornar True"
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_db.nome == "Serviço Atualizado", "O nome do serviço atualizado não confere"
        assert servico_db.descricao == "Descrição Atualizada", "A descrição do serviço atualizado não confere"
        assert servico_db.preco == 150.0, "O preço do serviço atualizado não confere"
        assert servico_db.tipo == 1, "O tipo do serviço atualizado não confere"

    def test_atualizar_servico_inexistente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        servico_exemplo.id = 999  # ID que não existe
        # Act
        resultado = servico_repo.atualizar_servico(servico_exemplo)
        # Assert
        assert resultado == False, "A atualização de um serviço inexistente deveria retornar False"

    def test_excluir_servico_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        resultado = servico_repo.excluir_servico(id_servico_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        servico_excluido = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_excluido is None, "O serviço excluído deveria ser None"

    def test_excluir_servico_inexistente(self, test_db):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        resultado = servico_repo.excluir_servico(999)
        # Assert
        assert resultado == False, "A exclusão de um serviço inexistente deveria retornar False"

    def test_atualizar_tipo_servico(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        resultado = servico_repo.atualizar_tipo_servico(id_servico_inserido, 1)
        # Assert
        assert resultado == True, "A atualização do tipo de serviço deveria retornar True"
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_db.tipo == 1, "O tipo do serviço atualizado não confere"

   
    def test_obter_servicos_por_pagina_primeira_pagina(self, test_db, lista_servicos_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        for servico in lista_servicos_exemplo:
            servico_repo.inserir_servico(servico)
        # Act
        pagina_servicos = servico_repo.obter_servicos_por_pagina(1, 4)
        # Assert
        assert len(pagina_servicos) == 4, "Deveria retornar 4 serviços na primeira página"
        assert all(isinstance(s, Servico) for s in pagina_servicos), "Todos os itens da página devem ser do tipo Servico"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id for u in pagina_servicos]
        assert ids_esperados == ids_retornados, "Os IDs dos serviços na primeira página não estão corretos"

    def test_obter_servicos_por_pagina_terceira_pagina(self, test_db, lista_servicos_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        for servico in lista_servicos_exemplo:
            servico_repo.inserir_servico(servico)
        # Act: busca a terceira página com 4 serviços por página
        pagina_servicos = servico_repo.obter_servicos_por_pagina(3, 4)
        # Assert: verifica se retornou a quantidade correta (2 serviços na terceira página)
        assert len(pagina_servicos) == 2, "Deveria retornar 2 serviços na terceira página"
        assert (isinstance(s, Servico) for s in pagina_servicos), "Todos os itens da página devem ser do tipo Servico"
```

# tests\test_usuario_repo.py

```py
#from model.usuario_model import Usuario
from model.usuario_model import Usuario
from repo import usuario_repo

class TestUsuarioRepo:
    def test_criar_tabela_usuarios(self, test_db):
        # Arrange
        # Act
        resultado = usuario_repo.criar_tabela_usuarios()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"
        assert True

    def test_inserir_usuario(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        # Act
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        # Assert
        usuario_db = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None, "O usuário inserido não deveria ser None"
        assert usuario_db.id == 1, "O usuário inserido deveria ter um ID igual a 1"
        assert usuario_db.nome == "Usuário Teste", "O nome do usuário inserido não confere"
        assert usuario_db.telefone == "(28) 99999-0000", "O telefone do usuário inserido não confere"
        assert usuario_db.email == "usuario@email.com", "O email do usuário inserido não confere"
        assert usuario_db.senha_hash == "123456", "A senha hash do usuário inserido não confere"
        assert usuario_db.tipo == "ADMIN", "O tipo do usuário inserido não confere"

    def test_obter_usuario_por_id_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()        
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        # Act
        usuario_db = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        # Assert
        assert usuario_db is not None, "O usuário retornado deveria ser diferente de None"
        assert usuario_db.id == id_usuario_inserido, "O id do usuário buscado deveria ser igual ao id do usuário inserido"
        assert usuario_db.nome == usuario_exemplo.nome, "O nome do usuário buscado deveria ser igual ao nome do usuário inserido"
        assert usuario_db.telefone == usuario_exemplo.telefone, "O telefone do usuário buscado deveria ser igual ao telefone do usuário inserido"
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário buscado deveria ser igual ao email do usuário inserido"
        assert usuario_db.senha_hash == usuario_exemplo.senha_hash, "A senha hash do usuário buscado deveria ser igual à senha hash do usuário inserido"
        assert usuario_db.tipo == usuario_exemplo.tipo, "O tipo do usuário buscado deveria ser igual ao tipo do usuário inserido"

    def test_obter_usuario_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        # Act
        usuario_db = usuario_repo.obter_usuario_por_id(999)
        # Assert
        assert usuario_db is None, "O usuário buscado com ID inexistente deveria retornar None"

    def test_obter_usuario_por_email_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        # Act
        usuario_db = usuario_repo.obter_usuario_por_email(usuario_exemplo.email)
        # Assert
        assert usuario_db is not None, "O usuário buscado por email deveria ser diferente de None"
        assert usuario_db.id == id_usuario_inserido, "O id do usuário buscado por email deveria ser igual ao id do usuário inserido"
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário buscado deveria ser igual ao email do usuário inserido"

    def test_obter_usuario_por_email_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        # Act
        usuario_db = usuario_repo.obter_usuario_por_email("inexistente@email.com")
        # Assert
        assert usuario_db is None, "O usuário buscado por email inexistente deveria retornar None"

    def test_atualizar_usuario_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        usuario_inserido = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        # Act
        usuario_inserido.nome = "Usuário Atualizado"
        usuario_inserido.telefone = "(28) 88888-0000"
        usuario_inserido.email = "usuario_atualizado@email.com"
        resultado = usuario_repo.atualizar_usuario(usuario_inserido)
        # Assert
        assert resultado == True, "A atualização do usuário deveria retornar True"
        usuario_db = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.nome == "Usuário Atualizado", "O nome do usuário atualizado não confere"
        assert usuario_db.telefone == "(28) 88888-0000", "O telefone do usuário atualizado não confere"
        assert usuario_db.email == "usuario_atualizado@email.com", "O email do usuário atualizado não confere"
        assert usuario_db.senha_hash == "123456", "A senha hash do usuário atualizado não confere"
        assert usuario_db.tipo == 0, "O tipo do usuário atualizado não confere"

    def test_atualizar_usuario_inexistente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuario_exemplo.id = 999  # ID que não existe
        # Act
        resultado = usuario_repo.atualizar_usuario(usuario_exemplo)
        # Assert
        assert resultado == False, "A atualização de um usuário inexistente deveria retornar False"

    def test_excluir_usuario_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()        
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        # Act
        resultado = usuario_repo.excluir_usuario(id_usuario_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        usuario_excluido = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_excluido is None, "O usuário excluído deveria ser None"

    def test_excluir_usuario_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        # Act
        resultado = usuario_repo.excluir_usuario(999)
        # Assert
        assert resultado == False, "A exclusão de um usuário inexistente deveria retornar False"

    def test_atualizar_tipo_usuario(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        # Act
        resultado = usuario_repo.atualizar_tipo_usuario(id_usuario_inserido, 1)
        # Assert
        assert resultado == True, "A atualização do tipo de usuário deveria retornar True"
        usuario_db = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.tipo == 1, "O tipo do usuário atualizado não confere"

    def test_atualizar_senha_usuario(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        # Act
        resultado = usuario_repo.atualizar_senha_usuario(id_usuario_inserido, "nova_senha_hash")
        # Assert
        assert resultado == True, "A atualização da senha do usuário deveria retornar True"
        usuario_db = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.senha_hash == "nova_senha_hash", "A senha do usuário atualizado não confere"

    def test_atualizar_senha_usuario_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        # Act
        resultado = usuario_repo.atualizar_senha_usuario(999, "nova_senha_hash")
        # Assert
        assert resultado == False, "A atualização da senha de um usuário inexistente deveria retornar False"

    def test_obter_usuarios_por_pagina_primeira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir_usuario(usuario)
        # Act
        pagina_usuarios = usuario_repo.obter_usuarios_por_pagina(1, 4)
        # Assert
        assert len(pagina_usuarios) == 4, "Deveria retornar 4 usuários na primeira página"
        assert all(isinstance(u, Usuario) for u in pagina_usuarios), "Todos os itens da página devem ser do tipo Usuario"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id for u in pagina_usuarios]
        assert ids_esperados == ids_retornados, "Os IDs dos usuários na primeira página não estão corretos"
    
    def test_obter_usuarios_por_pagina_terceira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir_usuario(usuario)
        # Act: busca a terceira página com 4 usuários por página
        pagina_usuarios = usuario_repo.obter_usuarios_por_pagina(3, 4)
        # Assert: verifica se retornou a quantidade correta (2 usuários na terceira página)
        assert len(pagina_usuarios) == 2, "Deveria retornar 2 usuários na terceira página"
        assert (isinstance(u, Usuario) for u in pagina_usuarios), "Todos os itens da página devem ser do tipo Usuario"
```

# util\database.py

```py
import sqlite3
import os

def obter_conexao():
    # Obtém o caminho do banco de dados a partir da variável de ambiente de testes ou usa o padrão
    database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
    # Conecta ao banco de dados SQLite
    conexao = sqlite3.connect(database_path)
    # Ativa as chaves estrangeiras
    conexao.execute("PRAGMA foreign_keys = ON")
    # Define a fábrica de linhas para retornar dicionários
    conexao.row_factory = sqlite3.Row
    # Retorna a conexão com o banco de dados
    return conexao
```

