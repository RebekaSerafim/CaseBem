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
CLAUDE.md
.claude

```

# .vscode/launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}

```

# .vscode/settings.json

```json
{
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python-envs.pythonProjects": []
}
```

# Dockerfile

```
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip git

WORKDIR /app

RUN git clone https://github.com/RebekaSerafim/CaseBem.git .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

# docs/AtualizacoesMaroquio.pdf

This is a binary file of the type: PDF

# docs/MAROQUIO.md

```md
# Relatório de Modificações - CaseBem

## Resumo das Alterações desde o Commit da Otávia (0ae31f6)

Este documento detalha todas as modificações realizadas no projeto CaseBem desde o último commit da Otávia ("correcoes do maroquio; usuario e casal com todos os testes passando") até o estado atual.

## Histórico de Commits

1. **0ae31f6** - Otávia - "correcoes do maroquio; usuario e casal com todos os testes passando" (ponto de partida)
2. **5946663** - Ricardo Maroquio - "início da simplificacao"
3. **898eddf** - Ricardo Maroquio - "atualizacoes nos itens de demanda"
4. **1d6f5ed** - Ricardo Maroquio - "renomeacoes e acertos de bugs"
5. **b2ebd3c** - Ricardo Maroquio - "refafotarcao completa"
6. **f5157da** - Ricardo Maroquio - "projeto atualizado com novo esquema de classes e com testes funcionando totalmente"

## Principais Mudanças Estruturais

### 1. Simplificação do Modelo de Usuários
- **Removido**: Modelos separados para `Noivo`, `Administrador`, `Fornecedor` e `Prestador`
- **Mantido**: Apenas o modelo `Usuario` com campo `tipo` para diferenciar os papéis
- **Impacto**: Simplificação significativa da estrutura, eliminando herança desnecessária

### 2. Reestruturação de Itens de Contrato
- **Renomeado**: `ItemContrato` → `ItemDemanda`
- **Criado**: Separação entre `ItemDemandaProduto` e `ItemDemandaServico`
- **Motivo**: Melhor representação do domínio onde demandas precedem contratos

### 3. Implementação Completa de Orçamentos
- **Criado**: Sistema completo de orçamentos com estrutura similar a demandas
- **Componentes**:
  - `model/orcamento_model.py`
  - `model/item_orcamento_produto_model.py`
  - `model/item_orcamento_servico_model.py`
  - Repositórios e SQLs correspondentes
  - Testes completos para todas as funcionalidades

## Detalhamento das Modificações

### Models (`/model/`)

#### Removidos:
- `administrador_model.py`
- `fornecedor_model.py`
- `prestador_model.py`
- `noivo_model.py` (nunca existiu como arquivo separado)

#### Modificados:
- **`usuario_model.py`**: 
  - Adicionado campo `tipo` (ENUM: ADMIN, NOIVO, FORNECEDOR, PRESTADOR)
  - Centralização de todos os tipos de usuário em uma única entidade

- **`casal_model.py`**:
  - Simplificado para referenciar IDs de usuários do tipo NOIVO
  - Removida herança complexa

- **`demanda_model.py`**:
  - Renomeado conceito de "contrato" para "demanda"
  - Representa lista de desejos do casal

#### Novos:
- **`item_demanda_produto_model.py`**: Item de demanda para produtos
- **`item_demanda_servico_model.py`**: Item de demanda para serviços
- **`orcamento_model.py`**: Orçamento principal com status (PENDENTE, ACEITO, REJEITADO)
- **`item_orcamento_produto_model.py`**: Item de orçamento para produtos com preço
- **`item_orcamento_servico_model.py`**: Item de orçamento para serviços com preço

### SQL (`/sql/`)

#### Modificações Principais:
- **Tabelas de usuário unificadas**: Removidas tabelas específicas por tipo
- **Foreign Keys**: Todas apontam para tabela `usuario`
- **Novos comandos SQL para orçamentos**:
  - Query especial `ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS`
  - Cálculo de totais por orçamento

### Repositórios (`/repo/`)

#### Removidos:
- `administrador_repo.py`
- `fornecedor_repo.py`
- `prestador_repo.py`

#### Modificados:
- **`usuario_repo.py`**: Centraliza todas operações de usuário
- **`casal_repo.py`**: Adicionado método `obter_casal_por_noivo`

#### Novos:
- **`orcamento_repo.py`**: 
  - Método especial `aceitar_orcamento_e_rejeitar_outros`
  - Métodos de busca por status, demanda, fornecedor/prestador
- **`item_orcamento_produto_repo.py`**: 
  - Inclui `calcular_total_itens_produto_orcamento`
- **`item_orcamento_servico_repo.py`**: 
  - Inclui `calcular_total_itens_servico_orcamento`

### Testes (`/tests/`)

#### Estrutura de Fixtures (`conftest.py`):
- **Problema corrigido**: Conflito de emails e telefones únicos entre diferentes tipos de usuários
- **Solução**: 
  - Noivos: emails `usuario{i}@email.com`, telefones `(28) 99999-00{i}`
  - Prestadores: emails `prestador{i}@email.com`, telefones `(28) 99999-20{i}`
  - Fornecedores: emails `fornecedor{i}@email.com`, telefones `(28) 99999-30{i}`
  - Administradores: emails `admin{i}@email.com`, telefones `(28) 99999-40{i}`

#### Novos Testes:
- `test_orcamento_repo.py`: 12 testes cobrindo todas funcionalidades
- `test_item_orcamento_produto_repo.py`: 9 testes incluindo cálculo de totais
- `test_item_orcamento_servico_repo.py`: 9 testes incluindo cálculo de totais

## Correções de Bugs

### 1. Foreign Key Constraints
- **Problema**: Ordem incorreta de criação de tabelas
- **Solução**: Sempre criar tabelas de dependência antes (usuario → casal → demanda → itens)

### 2. Unique Constraints
- **Problema**: Emails e telefones duplicados entre fixtures
- **Solução**: Namespaces diferentes para cada tipo de usuário

### 3. Nomenclatura Inconsistente
- **Problema**: Mistura entre "ItemContrato" e "ItemDemanda"
- **Solução**: Padronização completa para "ItemDemanda"

## Estado Final do Projeto

### Estatísticas:
- **Total de testes**: 122 (todos passando)
- **Cobertura**: Todos os repositórios com testes completos
- **Warnings**: Apenas deprecation warnings do datetime adapter do SQLite

### Arquitetura:
\`\`\`
CaseBem/
├── model/          # Modelos de dados (dataclasses)
├── sql/            # Comandos SQL
├── repo/           # Repositórios (camada de acesso a dados)
├── tests/          # Testes unitários
│   └── conftest.py # Fixtures compartilhadas
└── util/           # Utilitários (conexão com BD)
\`\`\`

### Fluxo de Negócio:
1. **Usuários** se cadastram com tipos específicos
2. **Casais** são formados por dois noivos
3. **Demandas** são criadas pelos casais com itens desejados
4. **Fornecedores/Prestadores** enviam orçamentos para as demandas
5. **Casais** podem aceitar orçamentos (rejeitando automaticamente os demais)

Modificado
```

# main.py

```py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import secrets

import uvicorn

from routes import locador_routes
from routes import usuario_routes
from routes import prestador_routes
from routes import fornecedor_routes
from routes import noivo_routes
from routes import public_routes

app = FastAPI()
SECRET_KEY = secrets.token_urlsafe(32)

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600,  # Sessão expira em 1 hora
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public_routes.router)
app.include_router(usuario_routes.router)
app.include_router(locador_routes.router)
app.include_router(noivo_routes.router)
app.include_router(prestador_routes.router)
app.include_router(fornecedor_routes.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

```

# model/casal_model.py

```py
from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Casal:
    id: int
    id_noivo1: int
    id_noivo2: int
    orcamento: float
    noivo1: Optional[Usuario] = None
    noivo2: Optional[Usuario] = None
```

# model/chat_model.py

```py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from model.usuario_model import Usuario

@dataclass
class Chat:    
    id_remetente: int
    id_destinatario: int
    data_hora_envio: datetime
    mensagem: str
    data_hora_leitura: Optional[datetime] = None
    remetente: Optional[Usuario] = None
    destinatario: Optional[Usuario] = None

```

# model/demanda_model.py

```py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Demanda:
    id: int
    id_casal: int
    data_hora_cadastro: datetime    
    
```

# model/fornecedor_produto_model.py

```py
from dataclasses import dataclass
from typing import Optional

from model.produto_model import Produto
from model.usuario_model import Usuario

@dataclass
class FornecedorProduto:
    id_fornecedor: int
    id_produto: int
    observacoes: Optional[str]
    preco: Optional[float]
    fornecedor: Optional[Usuario] = None
    produto: Optional[Produto] = None

```

# model/item_demanda_produto_model.py

```py
from dataclasses import dataclass
from typing import Optional

from model.demanda_model import Demanda
from model.produto_model import Produto

@dataclass
class ItemDemandaProduto:
    id_demanda: int
    id_produto: int    
    quantidade: int
    observacoes: Optional[str] = None
    demanda: Optional[Demanda] = None
    produto: Optional[Produto] = None

```

# model/item_demanda_servico_model.py

```py
from dataclasses import dataclass
from typing import Optional

from model.demanda_model import Demanda
from model.servico_model import Servico

@dataclass
class ItemDemandaServico:
    id_demanda: int
    id_servico: int
    quantidade: int
    observacoes: Optional[str] = None
    demanda: Optional[Demanda] = None
    servico: Optional[Servico] = None
```

# model/item_orcamento_produto_model.py

```py
from dataclasses import dataclass
from typing import Optional
from model.orcamento_model import Orcamento
from model.produto_model import Produto

@dataclass
class ItemOrcamentoProduto:
    id_orcamento: int
    id_produto: int
    preco_unitario: float
    quantidade: int
    observacoes: Optional[str] = None
    orcamento: Optional[Orcamento] = None
    produto: Optional[Produto] = None
```

# model/item_orcamento_servico_model.py

```py
from dataclasses import dataclass
from typing import Optional
from model.orcamento_model import Orcamento
from model.servico_model import Servico

@dataclass
class ItemOrcamentoServico:
    id_orcamento: int
    id_servico: int
    preco_unitario: float
    quantidade: int
    observacoes: Optional[str] = None
    orcamento: Optional[Orcamento] = None
    servico: Optional[Servico] = None
```

# model/orcamento_model.py

```py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from model.demanda_model import Demanda
from model.usuario_model import Usuario

@dataclass
class Orcamento:
    id: int
    id_demanda: int
    id_fornecedor_prestador: int
    data_hora_cadastro: datetime
    data_hora_validade: Optional[datetime] = None
    status: str = "PENDENTE"  # PENDENTE, ACEITO, REJEITADO
    observacoes: Optional[str] = None
    valor_total: Optional[float] = None
    demanda: Optional[Demanda] = None
    fornecedor_prestador: Optional[Usuario] = None
```

# model/prestador_servico_model.py

```py
from dataclasses import dataclass
from typing import Optional

from model.servico_model import Servico
from model.usuario_model import Usuario

@dataclass
class PrestadorServico:
    id_prestador: int
    id_servico: int
    observacoes: str
    preco: Optional[float] = None
    prestador: Optional[Usuario] = None
    servico: Optional[Servico] = None

```

# model/produto_model.py

```py
from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Produto:
    id: int
    nome: str
    preco: float    
    descricao: str
    
    
```

# model/servico_model.py

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

# model/usuario_model.py

```py
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TipoUsuario(Enum):
    ADMIN = "ADMIN"
    NOIVO = "NOIVO"        
    FORNECEDOR = "FORNECEDOR"
    PRESTADOR = "PRESTADOR"
    LOCADOR = "LOCADOR"

@dataclass
class Usuario:
    id: int
    nome: str
    telefone: str
    email: str
    senha: str
    perfil: TipoUsuario
    foto: Optional[str]
    token_redefinicao: Optional[str]
    data_token: Optional[str]
    data_cadastro: Optional[str]
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

# README.md

```md
# Projeto Case Bem


```

# repo/casal_repo.py

```py
from typing import Optional
from repo import usuario_repo
from util.database import obter_conexao
from sql.casal_sql import *
from model.casal_model import Casal

def criar_tabela_casal() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_CASAL)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de noivos: {e}")
        return False

def inserir_casal(casal: Casal) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_CASAL, (casal.id_noivo1, casal.id_noivo2, casal.orcamento))
        return cursor.lastrowid

def atualizar_casal(casal: Casal) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_CASAL, (casal.orcamento, casal.id))
        return (cursor.rowcount > 0)

def excluir_casal(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXCLUIR_CASAL, (id,))
        return (cursor.rowcount > 0)

def obter_casal_por_id(id: int) -> Optional[Casal]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CASAL_POR_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Casal(      
                id=resultado["id"],          
                id_noivo1=resultado["id_noivo1"],
                id_noivo2=resultado["id_noivo2"],
                orcamento=resultado["orcamento"],
                noivo1=usuario_repo.obter_usuario_por_id(resultado["id_noivo1"]),
                noivo2=usuario_repo.obter_usuario_por_id(resultado["id_noivo2"])
            )
    return None

def obter_casais_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Casal]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.cursor()
        cursor.execute(OBTER_CASAL_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Casal(
            id=resultado["id"],
            id_noivo1=resultado["id_noivo1"],
            id_noivo2=resultado["id_noivo2"],
            orcamento=resultado["orcamento"]
        ) for resultado in resultados]

def obter_casal_por_noivo(id_noivo: int) -> Optional[Casal]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CASAL_POR_NOIVO, (id_noivo, id_noivo))
        resultado = cursor.fetchone()
        if resultado:
            return Casal(
                id=resultado["id"],
                id_noivo1=resultado["id_noivo1"],
                id_noivo2=resultado["id_noivo2"],
                orcamento=resultado["orcamento"]
            )
    return None

```

# repo/chat_repo.py

```py
from typing import List
from datetime import datetime
from util.database import obter_conexao
from sql.chat_sql import *
from model.chat_model import Chat

def criar_tabela_chat() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_CHAT)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela Chat: {e}")
        return False

def inserir_chat(chat: Chat) -> bool:
    with obter_conexao() as conexao:
        conexao.execute(
            INSERIR_CHAT,
            (chat.id_remetente, chat.id_destinatario, chat.data_hora_envio, chat.mensagem)
        )
        return True

def obter_mensagens_por_usuario(id_usuario: int, pagina: int, tamanho: int) -> List[Chat]:
    offset = (pagina - 1) * tamanho
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_MENSAGENS_POR_USUARIO, (id_usuario, id_usuario, tamanho, offset))
        resultados = cursor.fetchall()
        return [Chat(
            id_remetente=r["id_remetente"],
            id_destinatario=r["id_destinatario"],
            mensagem=r["mensagem"],
            data_hora_envio=r["data_hora_envio"],
            data_hora_leitura=r["data_hora_leitura"]
        ) for r in resultados]

def atualizar_data_leitura(id_remetente: int, id_destinatario: int, data_envio: datetime, data_leitura: datetime) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_DATA_LEITURA,
            (data_leitura, id_remetente, id_destinatario, data_envio)
        )
        return cursor.rowcount > 0

```

# repo/demanda_repo.py

```py
from typing import Optional, List
from datetime import datetime
from util.database import obter_conexao
from sql.demanda_sql import *
from model.demanda_model import Demanda

def criar_tabela_demandas() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de demandas
            cursor.execute(CRIAR_TABELA_DEMANDA)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de demandas: {e}")
        # Retorna False indicando falha
        return False

def inserir_demanda(demanda: Demanda) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir demanda com todos os campos
        cursor.execute(INSERIR_DEMANDA, 
            (demanda.id_casal, demanda.data_hora_cadastro))
        # Retorna o ID da demanda inserida
        return cursor.lastrowid

def atualizar_demanda(demanda: Demanda) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados da demanda pelo ID
        cursor.execute(ATUALIZAR_DEMANDA, 
            (demanda.id_casal, demanda.data_hora_cadastro, demanda.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_demanda(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar demanda pelo ID
        cursor.execute(EXCLUIR_DEMANDA, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_demanda_por_id(id: int) -> Optional[Demanda]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar demanda pelo ID
        cursor.execute(OBTER_DEMANDA_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Demanda com dados do banco
            return Demanda(
                id=resultado["id"],
                id_casal=resultado["id_casal"],
                data_hora_cadastro=resultado["data_hora_cadastro"])
    # Retorna None se não encontrou demanda
    return None

def obter_demandas_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Demanda]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar demandas com paginação
        cursor.execute(OBTER_DEMANDAS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Demanda a partir dos resultados
        return [Demanda(
            id=resultado["id"],
            id_casal=resultado["id_casal"],
            data_hora_cadastro=resultado["data_hora_cadastro"]
        ) for resultado in resultados]

def obter_demandas_por_casal(id_casal: int) -> List[Demanda]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar demandas por casal
        cursor.execute(OBTER_DEMANDAS_POR_CASAL, (id_casal,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Demanda a partir dos resultados
        return [Demanda(
            id=resultado["id"],
            id_casal=resultado["id_casal"],
            data_hora_cadastro=resultado["data_hora_cadastro"]
        ) for resultado in resultados]
```

# repo/fornecedor_produto_repo.py

```py
from typing import Optional, List
from util.database import obter_conexao
from sql.fornecedor_produto_sql import *
from model.fornecedor_model import Fornecedor

def criar_tabela_fornecedor_produto() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_FORNECEDOR_PRODUTO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela FornecedorProduto: {e}")
        return False

def inserir_fornecedor_produto(fp: Fornecedor) -> Optional[tuple]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_FORNECEDOR_PRODUTO,
            (fp.id_fornecedor, fp.id_produto, fp.observacoes, fp.preco)
        )
        return (fp.id_fornecedor, fp.id_produto)

def atualizar_fornecedor_produto(fp: Fornecedor) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_FORNECEDOR_PRODUTO,
            (fp.observacoes, fp.preco, fp.id_fornecedor, fp.id_produto)
        )
        return cursor.rowcount > 0

def excluir_fornecedor_produto(id_fornecedor: int, id_produto: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_FORNECEDOR_PRODUTO, (id_fornecedor, id_produto))
        return cursor.rowcount > 0

def obter_fornecedor_produto_por_id(id_fornecedor: int, id_produto: int) -> Optional[Fornecedor]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_FORNECEDOR_PRODUTO_POR_ID, (id_fornecedor, id_produto))
        resultado = cursor.fetchone()
        if resultado:
            return Fornecedor(
                id_fornecedor=resultado["id_fornecedor"],
                id_produto=resultado["id_produto"],
                observacoes=resultado["observacoes"],
                preco=resultado["preco"]
            )
    return None

def obter_fornecedores_produto_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Fornecedor]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.execute(OBTER_FORNECEDORES_PRODUTO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Fornecedor(
            id_fornecedor=r["id_fornecedor"],
            id_produto=r["id_produto"],
            observacoes=r["observacoes"],
            preco=r["preco"]
        ) for r in resultados]

```

# repo/item_demanda_produto_repo.py

```py
from typing import Optional, List
from util.database import obter_conexao
from sql.item_demanda_produto_sql import *
from model.item_demanda_produto_model import ItemDemandaProduto

def criar_tabela_item_demanda_produto() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_ITEM_DEMANDA_PRODUTO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela ItemDemandaProduto: {e}")
        return False

def inserir_item_demanda_produto(item: ItemDemandaProduto) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_ITEM_DEMANDA_PRODUTO,
            (item.id_demanda, item.id_produto, item.quantidade, item.observacoes)
        )
        return cursor.rowcount > 0

def atualizar_item_demanda_produto(item: ItemDemandaProduto) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_ITEM_DEMANDA_PRODUTO,
            (item.quantidade, item.observacoes, item.id_demanda, item.id_produto)
        )
        return cursor.rowcount > 0

def excluir_item_demanda_produto(id_demanda: int, id_produto: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_ITEM_DEMANDA_PRODUTO, (id_demanda, id_produto))
        return cursor.rowcount > 0

def obter_item_demanda_produto_por_id(id_demanda: int, id_produto: int) -> Optional[ItemDemandaProduto]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITEM_DEMANDA_PRODUTO_POR_ID, (id_demanda, id_produto))
        row = cursor.fetchone()
        if row:
            return ItemDemandaProduto(
                id_demanda=row["id_demanda"],
                id_produto=row["id_produto"],
                quantidade=row["quantidade"],
                observacoes=row["observacoes"]
            )
    return None

def obter_itens_por_demanda(id_demanda: int) -> List[ItemDemandaProduto]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITENS_POR_DEMANDA, (id_demanda,))
        rows = cursor.fetchall()
        return [
            ItemDemandaProduto(
                id_demanda=row["id_demanda"],
                id_produto=row["id_produto"],
                quantidade=row["quantidade"],
                observacoes=row["observacoes"]
            ) for row in rows
        ]

def obter_itens_demanda_produto_por_pagina(pagina: int, tamanho: int) -> List[ItemDemandaProduto]:
    offset = (pagina - 1) * tamanho
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITENS_DEMANDA_PRODUTO_POR_PAGINA, (tamanho, offset))
        rows = cursor.fetchall()
        return [
            ItemDemandaProduto(
                id_demanda=row["id_demanda"],
                id_produto=row["id_produto"],
                quantidade=row["quantidade"],
                observacoes=row["observacoes"]
            ) for row in rows
        ]
```

# repo/item_demanda_servico_repo.py

```py
from typing import Optional, List
from util.database import obter_conexao
from sql.item_demanda_servico_sql import *
from model.item_demanda_servico_model import ItemDemandaServico

def criar_tabela_item_demanda_servico() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_ITEM_DEMANDA_SERVICO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela ItemDemandaServico: {e}")
        return False

def inserir_item_demanda_servico(item: ItemDemandaServico) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_ITEM_DEMANDA_SERVICO,
            (item.id_demanda, item.id_servico, item.quantidade, item.observacoes)
        )
        return cursor.rowcount > 0

def atualizar_item_demanda_servico(item: ItemDemandaServico) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_ITEM_DEMANDA_SERVICO,
            (item.quantidade, item.observacoes, item.id_demanda, item.id_servico)
        )
        return cursor.rowcount > 0

def excluir_item_demanda_servico(id_demanda: int, id_servico: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_ITEM_DEMANDA_SERVICO, (id_demanda, id_servico))
        return cursor.rowcount > 0

def obter_item_demanda_servico_por_id(id_demanda: int, id_servico: int) -> Optional[ItemDemandaServico]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITEM_DEMANDA_SERVICO_POR_ID, (id_demanda, id_servico))
        resultado = cursor.fetchone()
        if resultado:
            return ItemDemandaServico(
                id_demanda=resultado["id_demanda"],
                id_servico=resultado["id_servico"],
                quantidade=resultado["quantidade"],
                observacoes=resultado["observacoes"]
            )
    return None

def obter_itens_por_demanda(id_demanda: int) -> List[ItemDemandaServico]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITENS_POR_DEMANDA, (id_demanda,))
        resultados = cursor.fetchall()
        return [ItemDemandaServico(
            id_demanda=r["id_demanda"],
            id_servico=r["id_servico"],
            quantidade=r["quantidade"],
            observacoes=r["observacoes"]
        ) for r in resultados]

def obter_itens_demanda_servico_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[ItemDemandaServico]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.execute(OBTER_ITENS_DEMANDA_SERVICO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [ItemDemandaServico(
            id_demanda=r["id_demanda"],
            id_servico=r["id_servico"],
            quantidade=r["quantidade"],
            observacoes=r["observacoes"]
        ) for r in resultados]
```

# repo/item_orcamento_produto_repo.py

```py
from typing import Optional, List
from util.database import obter_conexao
from sql.item_orcamento_produto_sql import *
from model.item_orcamento_produto_model import ItemOrcamentoProduto

def criar_tabela_item_orcamento_produto() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de itens de orçamento produto
            cursor.execute(CRIAR_TABELA_ITEM_ORCAMENTO_PRODUTO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de itens de orçamento produto: {e}")
        # Retorna False indicando falha
        return False

def inserir_item_orcamento_produto(item: ItemOrcamentoProduto) -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para inserir item com todos os campos
            cursor.execute(INSERIR_ITEM_ORCAMENTO_PRODUTO, 
                (item.id_orcamento, item.id_produto, 
                 item.preco_unitario, item.quantidade, item.observacoes))
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao inserir item de orçamento produto: {e}")
        # Retorna False indicando falha
        return False

def atualizar_item_orcamento_produto(item: ItemOrcamentoProduto) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do item pela chave composta
        cursor.execute(ATUALIZAR_ITEM_ORCAMENTO_PRODUTO, 
            (item.preco_unitario, item.quantidade, item.observacoes,
             item.id_orcamento, item.id_produto))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_item_orcamento_produto(id_orcamento: int, id_produto: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar item pela chave composta
        cursor.execute(EXCLUIR_ITEM_ORCAMENTO_PRODUTO, (id_orcamento, id_produto))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_item_orcamento_produto_por_id(id_orcamento: int, id_produto: int) -> Optional[ItemOrcamentoProduto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar item pela chave composta
        cursor.execute(OBTER_ITEM_ORCAMENTO_PRODUTO_POR_ID, (id_orcamento, id_produto))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto ItemOrcamentoProduto com dados do banco
            return ItemOrcamentoProduto(
                id_orcamento=resultado["id_orcamento"],
                id_produto=resultado["id_produto"],
                preco_unitario=resultado["preco_unitario"],
                quantidade=resultado["quantidade"],
                observacoes=resultado["observacoes"]
            )
    # Retorna None se não encontrou item
    return None

def obter_itens_por_orcamento(id_orcamento: int) -> List[ItemOrcamentoProduto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar itens por orçamento
        cursor.execute(OBTER_ITENS_POR_ORCAMENTO, (id_orcamento,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos ItemOrcamentoProduto a partir dos resultados
        return [ItemOrcamentoProduto(
            id_orcamento=resultado["id_orcamento"],
            id_produto=resultado["id_produto"],
            preco_unitario=resultado["preco_unitario"],
            quantidade=resultado["quantidade"],
            observacoes=resultado["observacoes"]
        ) for resultado in resultados]

def obter_itens_orcamento_produto_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[ItemOrcamentoProduto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar itens com paginação
        cursor.execute(OBTER_ITENS_ORCAMENTO_PRODUTO_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos ItemOrcamentoProduto a partir dos resultados
        return [ItemOrcamentoProduto(
            id_orcamento=resultado["id_orcamento"],
            id_produto=resultado["id_produto"],
            preco_unitario=resultado["preco_unitario"],
            quantidade=resultado["quantidade"],
            observacoes=resultado["observacoes"]
        ) for resultado in resultados]

def calcular_total_itens_produto_orcamento(id_orcamento: int) -> float:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para calcular total
        cursor.execute(CALCULAR_TOTAL_ITENS_PRODUTO_ORCAMENTO, (id_orcamento,))
        # Obtém resultado
        resultado = cursor.fetchone()
        # Retorna o total ou 0 se não houver itens
        return resultado["total"] if resultado["total"] else 0.0
```

# repo/item_orcamento_servico_repo.py

```py
from typing import Optional, List
from util.database import obter_conexao
from sql.item_orcamento_servico_sql import *
from model.item_orcamento_servico_model import ItemOrcamentoServico

def criar_tabela_item_orcamento_servico() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de itens de orçamento serviço
            cursor.execute(CRIAR_TABELA_ITEM_ORCAMENTO_SERVICO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de itens de orçamento serviço: {e}")
        # Retorna False indicando falha
        return False

def inserir_item_orcamento_servico(item: ItemOrcamentoServico) -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para inserir item com todos os campos
            cursor.execute(INSERIR_ITEM_ORCAMENTO_SERVICO, 
                (item.id_orcamento, item.id_servico, 
                 item.preco_unitario, item.quantidade, item.observacoes))
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao inserir item de orçamento serviço: {e}")
        # Retorna False indicando falha
        return False

def atualizar_item_orcamento_servico(item: ItemOrcamentoServico) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do item pela chave composta
        cursor.execute(ATUALIZAR_ITEM_ORCAMENTO_SERVICO, 
            (item.preco_unitario, item.quantidade, item.observacoes,
             item.id_orcamento, item.id_servico))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_item_orcamento_servico(id_orcamento: int, id_servico: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar item pela chave composta
        cursor.execute(EXCLUIR_ITEM_ORCAMENTO_SERVICO, (id_orcamento, id_servico))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_item_orcamento_servico_por_id(id_orcamento: int, id_servico: int) -> Optional[ItemOrcamentoServico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar item pela chave composta
        cursor.execute(OBTER_ITEM_ORCAMENTO_SERVICO_POR_ID, (id_orcamento, id_servico))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto ItemOrcamentoServico com dados do banco
            return ItemOrcamentoServico(
                id_orcamento=resultado["id_orcamento"],
                id_servico=resultado["id_servico"],
                preco_unitario=resultado["preco_unitario"],
                quantidade=resultado["quantidade"],
                observacoes=resultado["observacoes"]
            )
    # Retorna None se não encontrou item
    return None

def obter_itens_por_orcamento(id_orcamento: int) -> List[ItemOrcamentoServico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar itens por orçamento
        cursor.execute(OBTER_ITENS_POR_ORCAMENTO, (id_orcamento,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos ItemOrcamentoServico a partir dos resultados
        return [ItemOrcamentoServico(
            id_orcamento=resultado["id_orcamento"],
            id_servico=resultado["id_servico"],
            preco_unitario=resultado["preco_unitario"],
            quantidade=resultado["quantidade"],
            observacoes=resultado["observacoes"]
        ) for resultado in resultados]

def obter_itens_orcamento_servico_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[ItemOrcamentoServico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar itens com paginação
        cursor.execute(OBTER_ITENS_ORCAMENTO_SERVICO_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos ItemOrcamentoServico a partir dos resultados
        return [ItemOrcamentoServico(
            id_orcamento=resultado["id_orcamento"],
            id_servico=resultado["id_servico"],
            preco_unitario=resultado["preco_unitario"],
            quantidade=resultado["quantidade"],
            observacoes=resultado["observacoes"]
        ) for resultado in resultados]

def calcular_total_itens_servico_orcamento(id_orcamento: int) -> float:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para calcular total
        cursor.execute(CALCULAR_TOTAL_ITENS_SERVICO_ORCAMENTO, (id_orcamento,))
        # Obtém resultado
        resultado = cursor.fetchone()
        # Retorna o total ou 0 se não houver itens
        return resultado["total"] if resultado["total"] else 0.0
```

# repo/orcamento_repo.py

```py
from typing import Optional, List
from datetime import datetime
from util.database import obter_conexao
from sql.orcamento_sql import *
from model.orcamento_model import Orcamento

def criar_tabela_orcamento() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de orçamentos
            cursor.execute(CRIAR_TABELA_ORCAMENTO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de orçamentos: {e}")
        # Retorna False indicando falha
        return False

def inserir_orcamento(orcamento: Orcamento) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir orçamento com todos os campos
        cursor.execute(INSERIR_ORCAMENTO, 
            (orcamento.id_demanda, orcamento.id_fornecedor_prestador,
             orcamento.data_hora_cadastro, orcamento.data_hora_validade,
             orcamento.status, orcamento.observacoes, orcamento.valor_total))
        # Retorna o ID do orçamento inserido
        return cursor.lastrowid

def atualizar_orcamento(orcamento: Orcamento) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do orçamento pelo ID
        cursor.execute(ATUALIZAR_ORCAMENTO, 
            (orcamento.data_hora_validade, orcamento.status,
             orcamento.observacoes, orcamento.valor_total, orcamento.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar status do orçamento
        cursor.execute(ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_valor_total_orcamento(id_orcamento: int, valor_total: float) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar valor total do orçamento
        cursor.execute(ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id_orcamento))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def aceitar_orcamento_e_rejeitar_outros(id_orcamento: int, id_demanda: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para aceitar orçamento e rejeitar outros
        cursor.execute(ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_orcamento(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar orçamento pelo ID
        cursor.execute(EXCLUIR_ORCAMENTO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_orcamento_por_id(id: int) -> Optional[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamento pelo ID
        cursor.execute(OBTER_ORCAMENTO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Orcamento com dados do banco
            return Orcamento(
                id=resultado["id"],
                id_demanda=resultado["id_demanda"],
                id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
                data_hora_cadastro=resultado["data_hora_cadastro"],
                data_hora_validade=resultado["data_hora_validade"],
                status=resultado["status"],
                observacoes=resultado["observacoes"],
                valor_total=resultado["valor_total"]
            )
    # Retorna None se não encontrou orçamento
    return None

def obter_orcamentos_por_demanda(id_demanda: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por demanda
        cursor.execute(OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_fornecedor_prestador(id_fornecedor_prestador: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por fornecedor/prestador
        cursor.execute(OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR, (id_fornecedor_prestador,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_status(status: str) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por status
        cursor.execute(OBTER_ORCAMENTOS_POR_STATUS, (status,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos com paginação
        cursor.execute(OBTER_ORCAMENTOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]
```

# repo/prestador_servico_repo.py

```py
from typing import Optional, List
from util.database import obter_conexao
from sql.prestador_servico_sql import *
from model.prestador_servico_model import Prestador

def criar_tabela_prestador_servico() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_PRESTADOR_SERVICO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela PrestadorServico: {e}")
        return False

def inserir_prestador_servico(ps: Prestador) -> Optional[tuple]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_PRESTADOR_SERVICO,
            (ps.id_prestador, ps.id_servico, ps.observacoes, ps.preco)
        )
        return (ps.id_prestador, ps.id_servico)

def atualizar_prestador_servico(ps: Prestador) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_PRESTADOR_SERVICO,
            (ps.observacoes, ps.preco, ps.id_prestador, ps.id_servico)
        )
        return cursor.rowcount > 0

def excluir_prestador_servico(id_prestador: int, id_servico: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_PRESTADOR_SERVICO, (id_prestador, id_servico))
        return cursor.rowcount > 0

def obter_prestador_servico_por_id(id_prestador: int, id_servico: int) -> Optional[Prestador]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_PRESTADOR_SERVICO_POR_ID, (id_prestador, id_servico))
        resultado = cursor.fetchone()
        if resultado:
            return Prestador(
                id_prestador=resultado["id_prestador"],
                id_servico=resultado["id_servico"],
                observacoes=resultado["observacoes"],
                preco=resultado["preco"]
            )
    return None

def obter_prestadores_servico_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Prestador]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.execute(OBTER_PRESTADORES_SERVICO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Prestador(
            id_prestador=r["id_prestador"],
            id_servico=r["id_servico"],
            observacoes=r["observacoes"],
            preco=r["preco"]
        ) for r in resultados]
```

# repo/produto_repo.py

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
            (produto.nome, produto.preco, produto.descricao))
        # Retorna o ID do produto inserido
        return cursor.lastrowid        

def atualizar_produto(produto: Produto) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do produto pelo ID
        cursor.execute(ATUALIZAR_PRODUTO, 
            (produto.nome, produto.preco, produto.descricao, produto.id))    
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
        return [Produto(
            id=resultado["id"],
            nome=resultado["nome"],
            preco=resultado["preco"],
            descricao=resultado["descricao"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou produtos
    return []
```

# repo/servico_repo.py

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
            # Executa comando SQL para criar tabela de serviços
            cursor.execute(CRIAR_TABELA_SERVICO)
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
    

def excluir_servico(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar serviço pelo ID
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
        cursor.execute(OBTER_SERVICOS_POR_PAGINA, (limite, offset))
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

def obter_servico_por_nome(nome: str) -> Optional[Servico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar serviço pelo nome
        cursor.execute(OBTER_SERVICO_POR_NOME, (nome,))
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
```

# repo/usuario_repo.py

```py
from typing import Optional
from util.database import obter_conexao
from sql.usuario_sql import *
from model.usuario_model import TipoUsuario, Usuario

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
            (usuario.nome, usuario.telefone, usuario.email, usuario.senha_hash, usuario.tipo, usuario.documento))
        # Retorna o ID do usuário inserido
        return cursor.lastrowid        

def atualizar_usuario(usuario: Usuario) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(ATUALIZAR_USUARIO, 
            (usuario.nome, usuario.telefone, usuario.email, usuario.documento, usuario.id))    
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
                tipo=resultado["tipo"],
                documento=resultado["documento"])
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
                tipo=resultado["tipo"], 
                documento=resultado["documento"])
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
            senha_hash=resultado["senha_hash"],
            tipo=resultado["tipo"],
            documento=resultado["documento"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []


def obter_usuarios_por_tipo_por_pagina(tipo: TipoUsuario, numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários por tipo com paginação
        cursor.execute(OBTER_USUARIOS_POR_TIPO_POR_PAGINA, (tipo, limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            senha_hash=resultado["senha_hash"],
            tipo=resultado["tipo"],
            documento=resultado["documento"]
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
passlib[bcrypt]
python-jose[cryptography]
itsdangerous

# Dependências de teste
pytest
pytest-asyncio
pytest-cov


```

# routes/admin_routes.py

```py
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/dashboard")
async def get_root():
    response = templates.TemplateResponse("administrador/dashboard.html", {"request": {}})
    return response

@router.get("/administrador/administradores")
async def get_root():
    response = templates.TemplateResponse("administrador/administradores.html", {"request": {}})
    return response

@router.get("/administrador/administradores/cadastrar")
async def get_root():
    response = templates.TemplateResponse("administrador/cadastrar_administrador.html", {"request": {}})
    return response

@router.get("/administrador/administradores/alterar/{id_administrador}")
async def get_root(id_administrador: int):
    response = templates.TemplateResponse("administrador/alterar_administrador.html", {"request": {}})
    return response

@router.get("/administrador/administradores/excluir/{id_administrador}")
async def get_root(id_administrador: int):
    response = templates.TemplateResponse("administrador/excluir_administrador.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos")
async def get_root():
    response = templates.TemplateResponse("administrador/categorias_produtos.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos/cadastrar")
async def get_root():
    response = templates.TemplateResponse("administrador/cadastrar_categoria_produto.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos/alterar/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/alterar_categoria_produto.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos/excluir/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/excluir_categoria_produto.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos")
async def get_root():
    response = templates.TemplateResponse("administrador/categorias_servicos.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos/cadastrar")
async def get_root():    
    response = templates.TemplateResponse("administrador/cadastrar_categoria_servico.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos/alterar/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/alterar_categoria_servico.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos/excluir/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/excluir_categoria_servico.html", {"request": {}})
    return response

@router.get("/administrador/cadastros_pendentes")
async def get_root():
    response = templates.TemplateResponse("administrador/cadastros_pendentes.html", {"request": {}})
    return response

@router.get("/administrador/validar_cadastro/{id_usuario}")
async def get_root(id_usuario: int):
    response = templates.TemplateResponse("administrador/validar_cadastro.html", {"request": {}})
    return response

@router.get("/administrador/usuarios")
async def get_root():
    response = templates.TemplateResponse("administrador/usuarios.html", {"request": {}})
    return response
```

# routes/fornecedor_routes.py

```py
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/fornecedor/dashboard")
async def get_root():
    response = templates.TemplateResponse("fornecedor/dashboard.html", {"request": {}})
    return response

@router.get("/fornecedor/cadastar_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/cadastrar_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/alterar_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/alterar_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/excluir_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/excluir_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/detalhes_do_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/detalhes_do_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/dados_do_perfil")
async def get_root():
    response = templates.TemplateResponse("fornecedor/dados_do_perfil.html", {"request": {}})
    return response





```

# routes/locador_routes.py

```py
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/locador/dashboard")
async def get_root():
    response = templates.TemplateResponse("locador/dashboard.html", {"request": {}})
    return response

@router.get("/locador/locadores")
async def get_root():
    response = templates.TemplateResponse("locador/locadores.html", {"request": {}})
    return response

@router.get("/locador/locadores/cadastrar")
async def get_root():
    response = templates.TemplateResponse("locador/cadastrar_locador.html", {"request": {}})
    return response

@router.get("/locador/locadores/alterar/{id_locador}")
async def get_root(id_locador: int):
    response = templates.TemplateResponse("locador/alterar_locador.html", {"request": {}})
    return response

@router.get("/locador/locadores/excluir/{id_locador}")
async def get_root(id_locador: int):
    response = templates.TemplateResponse("locador/excluir_locador.html", {"request": {}})
    return response

@router.get("/locador/detalhes_local/{id_locador}")
async def get_root(id_locador: int):
    response = templates.TemplateResponse("locador/detalhes_local.html", {"request": {}, "id_locador": id_locador})
    return response

@router.get("/locador/dados_perfil/cadastrar")
async def get_root():
    response = templates.TemplateResponse("locador/cadastrar_dados_perfil.html", {"request": {}})
    return response


```

# routes/noivo_routes.py

```py
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/noivo/dashboard")
async def get_root():
    response = templates.TemplateResponse("noivo/dashboard.html", {"request": {}})
    return response

@router.get("/noivo/noivos")
async def get_root():
    response = templates.TemplateResponse("noivo/noivos.html", {"request": {}})
    return response

@router.get("/noivo/noivos/cadastrar")
async def get_root():
    response = templates.TemplateResponse("noivo/cadastrar_noivo.html", {"request": {}})
    return response

@router.get("/noivo/noivos/alterar/{id_noivo}")
async def get_root(id_noivo: int):
    response = templates.TemplateResponse("noivo/alterar_noivo.html", {"request": {}})
    return response

@router.get("/noivo/noivos/excluir/{id_noivo}")
async def get_root(id_noivo: int):
    response = templates.TemplateResponse("noivo/excluir_noivo.html", {"request": {}})
    return response

@router.get("/noivo/compras_e_contratacoes/{id_noivo}")
async def get_root(id_noivo: int):
    response = templates.TemplateResponse("noivo/compras_e_contratacoes.html", {"request": {}, "id_noivo": id_noivo})
    return response

@router.get("/noivo/dados_usuario/cadastrar")
async def get_root():
    response = templates.TemplateResponse("noivo/cadastrar_dados_usuario.html", {"request": {}})
    return response


```

# routes/prestador_routes.py

```py
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/prestador/dashboard")
async def get_root():
    response = templates.TemplateResponse("prestador/dashboard.html", {"request": {}})
    return response

@router.get("/prestador/cadastar_servico")
async def get_root():
    response = templates.TemplateResponse("prestador/cadastrar_servico.html", {"request": {}})
    return response

@router.get("/prestador/alterar_servico")
async def get_root():
    response = templates.TemplateResponse("prestador/alterar_servico.html", {"request": {}})
    return response

@router.get("/prestador/excluir_servico")
async def get_root():
    response = templates.TemplateResponse("prestador/excluir_servico.html", {"request": {}})
    return response

@router.get("/prestador/detalhes_do_servico")
async def get_root():
    response = templates.TemplateResponse("prestador/detalhes_do_servico.html", {"request": {}})
    return response

@router.get("/prestador/dados_do_perfil")
async def get_root():
    response = templates.TemplateResponse("prestador/dados_do_perfil.html", {"request": {}})
    return response





```

# routes/public_routes.py

```py
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.usuario_model import TipoUsuario, Usuario
from repo import usuario_repo
from util.auth_decorator import criar_sessao
from util.security import criar_hash_senha, verificar_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root():
    response = templates.TemplateResponse("publico/home.html", {"request": {}})
    return response


@router.get("/cadastro")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro.html", {"request": {}})
    return response


@router.get("/cadastro_noivos")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_noivos.html", {"request": {}})
    return response


@router.post("/cadastro_noivos")
async def post_root(request: Request,
    nome_noivo: str = Form(...),
    telefone_noivo: str = Form(None),
    email_noivo: str = Form(...),
    senha_noivo: str = Form(...),
    nome_noiva: str = Form(...),
    telefone_noiva: str = Form(None),
    email_noiva: str = Form(...),
    senha_noiva: str = Form(...)
):
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email_noivo):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "E-mail do noivo já cadastrado"}
        )
    if usuario_repo.obter_por_email(email_noiva):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "E-mail do noiva já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash_noivo = criar_hash_senha(senha_noivo)
    senha_hash_noiva = criar_hash_senha(senha_noiva)
    
    # Criar usuário
    usuario_noivo = Usuario(
        id=0,
        nome=nome_noivo,
        telefone=telefone_noivo,
        email=email_noivo,
        senha=senha_hash_noivo,
        perfil=TipoUsuario.NOIVO
    )
    usuario_noivo_id = usuario_repo.inserir(usuario_noivo)

    usuario_noiva = Usuario(
        id=0,
        nome=nome_noiva,
        telefone=telefone_noiva,
        email=email_noiva,
        senha=senha_hash_noiva,
        perfil=TipoUsuario.NOIVO
    )    
    usuario_noiva_id = usuario_repo.inserir(usuario_noiva)
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_geral")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_fornecedor.html", {"request": {}})
    return response


@router.post("/cadastro_geral")
async def post_root(request: Request,
    nome: str = Form(...),
    telefone: str = Form(None),
    email: str = Form(...),
    senha: str = Form(...),
    tipo: str = Form(...)
):
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "E-mail do noivo já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash_noivo = criar_hash_senha(senha)  
    perfil = None
    match (tipo):
        case "F":
            perfil = TipoUsuario.FORNECEDOR            
        case  "P":
            perfil = TipoUsuario.PRESTADOR
        case "L":
            perfil = TipoUsuario.LOCADOR

    # Criar usuário
    usuario_fornecedor = Usuario(
        id=0,
        nome=nome,
        telefone=telefone,
        email=email,
        senha=senha_hash_noivo,
        perfil=perfil
    )
    usuario_id = usuario_repo.inserir(usuario_fornecedor)
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_confirmacao")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_confirmacao.html", {"request": {}})
    return response

@router.get("/login")
async def get_root():
    response = templates.TemplateResponse("publico/login.html", {"request": {}})
    return response


@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_por_email(email)
    
    if not usuario or not verificar_senha(senha, usuario.senha):
       return templates.TemplateResponse(
    "publico/login.html",
    {"request": request, "erro": "Email ou senha inválidos"}
)


    
    # Criar sessão
    usuario_dict = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)
    
    # Redirecionar
    if redirect:
        return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)
    
    if usuario.perfil == "admin":
        return RedirectResponse("/admin", status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

@router.get("/contato")
async def get_root():
    response = templates.TemplateResponse("publico/contato.html", {"request": {}})
    return response

@router.get("/sobre")
async def get_root():
    response = templates.TemplateResponse("publico/sobre.html", {"request": {}})
    return response

@router.get("/produtos")
async def get_root():
    response = templates.TemplateResponse("publico/produtos.html", {"request": {}})
    return response

@router.get("/servicos")
async def get_root():
    response = templates.TemplateResponse("publico/servicos.html", {"request": {}})
    return response

@router.get("/locais")
async def get_root():
    response = templates.TemplateResponse("publico/locais.html", {"request": {}})
    return response

@router.get("/fornecedores")
async def get_root():
    response = templates.TemplateResponse("publico/fornecedores.html", {"request": {}})
    return response

@router.get("/prestadores")
async def get_root():
    response = templates.TemplateResponse("publico/prestadores.html", {"request": {}})
    return response

@router.get("/locais/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_local.html", {"request": {}, "id": id})
    return response

@router.get("/fornecedores/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_fornecedor.html", {"request": {}, "id": id})
    return response

@router.get("/prestadores/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_prestador.html", {"request": {}, "id": id})
    return response

@router.get("/produtos/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_produto.html", {"request": {}, "id": id})
    return response

@router.get("/servicos/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_servico.html", {"request": {}, "id": id})
    return response


```

# routes/usuario_routes.py

```py
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuario/alterar_senha")
async def get_root():
    response = templates.TemplateResponse("usuario/alterar_senha.html", {"request": {}})
    return response

@router.get("/usuario/conversas")
async def get_root():
    response = templates.TemplateResponse("usuario/conversas.html", {"request": {}})
    return response

@router.get("/usuario/conversas/{id_conversa}")
async def get_root(id_conversa: int):    
    response = templates.TemplateResponse("usuario/chat.html", {"request": {}})
    return response
```

# sql/casal_sql.py

```py
CRIAR_TABELA_CASAL = """
CREATE TABLE IF NOT EXISTS casal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_noivo1 INTEGER NOT NULL,
    id_noivo2 INTEGER NOT NULL,
    orcamento REAL NOT NULL,
    FOREIGN KEY (id_noivo1) REFERENCES usuario(id),
    FOREIGN KEY (id_noivo2) REFERENCES usuario(id)
);
"""

INSERIR_CASAL = """
INSERT INTO casal (id_noivo1, id_noivo2, orcamento)
VALUES (?, ?, ?);
"""

ATUALIZAR_CASAL = """
UPDATE casal
SET orcamento = ?
WHERE id = ?;
"""

EXCLUIR_CASAL = """
DELETE FROM casal
WHERE id = ?;
"""

OBTER_CASAL_POR_ID = """
SELECT id, id_noivo1, id_noivo2, orcamento
FROM casal
WHERE id = ?;
"""

OBTER_CASAL_POR_NOIVO = """
SELECT id, id_noivo1, id_noivo2, orcamento
FROM casal
WHERE (id_noivo1 = ? OR id_noivo2 = ?)
ORDER BY id DESC;
"""

OBTER_CASAL_POR_PAGINA = """
SELECT id, id_noivo1, id_noivo2, orcamento
FROM casal
LIMIT ? OFFSET ?;
"""

```

# sql/chat_sql.py

```py
CRIAR_TABELA_CHAT = """
CREATE TABLE IF NOT EXISTS chat (
    id_remetente INTEGER NOT NULL,
    id_destinatario INTEGER NOT NULL,
    data_hora_envio TIMESTAMP NOT NULL,
    mensagem TEXT NOT NULL,
    data_hora_leitura TIMESTAMP,
    PRIMARY KEY (id_remetente, id_destinatario, data_hora_envio),
    FOREIGN KEY (id_remetente) REFERENCES usuario(id),
    FOREIGN KEY (id_destinatario) REFERENCES usuario(id)
);
"""

INSERIR_CHAT = """
INSERT INTO chat (id_remetente, id_destinatario, data_hora_envio, mensagem)
VALUES (?, ?, ?, ?);
"""

OBTER_MENSAGENS_POR_USUARIO = """
SELECT id_remetente, id_destinatario, data_hora_envio, mensagem, data_hora_leitura
FROM chat
WHERE id_remetente = ? OR id_destinatario = ?
ORDER BY data_hora_envio DESC
LIMIT ? OFFSET ?;
"""

ATUALIZAR_DATA_LEITURA = """
UPDATE chat
SET data_hora_leitura = ?
WHERE id_remetente = ? AND id_destinatario = ? AND data_hora_envio = ?;
"""

```

# sql/demanda_sql.py

```py
CRIAR_TABELA_DEMANDA = """
CREATE TABLE IF NOT EXISTS demanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_casal INTEGER NOT NULL,
    data_hora_cadastro TIMESTAMP NOT NULL,
    FOREIGN KEY (id_casal) REFERENCES casal(id) ON DELETE CASCADE
);
"""

INSERIR_DEMANDA = """
INSERT INTO demanda (id_casal, data_hora_cadastro)
VALUES (?, ?);
"""

ATUALIZAR_DEMANDA = """
UPDATE demanda
SET id_casal = ?, data_hora_cadastro = ?
WHERE id = ?;
"""

EXCLUIR_DEMANDA = """
DELETE FROM demanda
WHERE id = ?;
"""

OBTER_DEMANDA_POR_ID = """
SELECT id, id_casal, data_hora_cadastro
FROM demanda
WHERE id = ?;
"""

OBTER_DEMANDAS_POR_PAGINA = """
SELECT id, id_casal, data_hora_cadastro
FROM demanda
ORDER BY data_hora_cadastro DESC
LIMIT ? OFFSET ?;
"""

OBTER_DEMANDAS_POR_CASAL = """
SELECT id, id_casal, data_hora_cadastro
FROM demanda
WHERE id_casal = ?
ORDER BY data_hora_cadastro DESC;
"""
```

# sql/fornecedor_produto_sql.py

```py
CRIAR_TABELA_FORNECEDOR_PRODUTO = """
CREATE TABLE IF NOT EXISTS fornecedor_produto (
    id_fornecedor INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    observacoes TEXT,
    preco REAL,
    PRIMARY KEY (id_fornecedor, id_produto),
    FOREIGN KEY (id_fornecedor) REFERENCES usuario(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);
"""

INSERIR_FORNECEDOR_PRODUTO = """
INSERT INTO fornecedor_produto (id_fornecedor, id_produto, observacoes, preco)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_FORNECEDOR_PRODUTO = """
UPDATE fornecedor_produto
SET observacoes = ?, preco = ?
WHERE id_fornecedor = ? AND id_produto = ?;
"""

EXCLUIR_FORNECEDOR_PRODUTO = """
DELETE FROM fornecedor_produto
WHERE id_fornecedor = ? AND id_produto = ?;
"""

OBTER_FORNECEDOR_PRODUTO_POR_ID = """
SELECT id_fornecedor, id_produto, observacoes, preco
FROM fornecedor_produto
WHERE id_fornecedor = ? AND id_produto = ?;
"""

OBTER_FORNECEDORES_PRODUTO_POR_PAGINA = """
SELECT id_fornecedor, id_produto, observacoes, preco
FROM fornecedor_produto
ORDER BY id_fornecedor ASC
LIMIT ? OFFSET ?;
"""

```

# sql/item_demanda_produto_sql.py

```py
CRIAR_TABELA_ITEM_DEMANDA_PRODUTO = """
CREATE TABLE IF NOT EXISTS item_demanda_produto (
    id_demanda INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_demanda, id_produto),
    FOREIGN KEY (id_demanda) REFERENCES demanda(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);
"""

INSERIR_ITEM_DEMANDA_PRODUTO = """
INSERT INTO item_demanda_produto (id_demanda, id_produto, quantidade, observacoes)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_ITEM_DEMANDA_PRODUTO = """
UPDATE item_demanda_produto
SET quantidade = ?, observacoes = ?
WHERE id_demanda = ? AND id_produto = ?;
"""

EXCLUIR_ITEM_DEMANDA_PRODUTO = """
DELETE FROM item_demanda_produto
WHERE id_demanda = ? AND id_produto = ?;
"""

OBTER_ITEM_DEMANDA_PRODUTO_POR_ID = """
SELECT id_demanda, id_produto, quantidade, observacoes
FROM item_demanda_produto
WHERE id_demanda = ? AND id_produto = ?;
"""

OBTER_ITENS_POR_DEMANDA = """
SELECT id_demanda, id_produto, quantidade, observacoes
FROM item_demanda_produto
WHERE id_demanda = ?
ORDER BY id_produto ASC;
"""

OBTER_ITENS_DEMANDA_PRODUTO_POR_PAGINA = """
SELECT id_demanda, id_produto, quantidade, observacoes
FROM item_demanda_produto
ORDER BY id_demanda ASC, id_produto ASC
LIMIT ? OFFSET ?;
"""
```

# sql/item_demanda_servico_sql.py

```py
CRIAR_TABELA_ITEM_DEMANDA_SERVICO = """
CREATE TABLE IF NOT EXISTS item_demanda_servico (
    id_demanda INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_demanda, id_servico),
    FOREIGN KEY (id_demanda) REFERENCES demanda(id),
    FOREIGN KEY (id_servico) REFERENCES servico(id)
);
"""

INSERIR_ITEM_DEMANDA_SERVICO = """
INSERT INTO item_demanda_servico (id_demanda, id_servico, quantidade, observacoes)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_ITEM_DEMANDA_SERVICO = """
UPDATE item_demanda_servico
SET quantidade = ?, observacoes = ?
WHERE id_demanda = ? AND id_servico = ?;
"""

EXCLUIR_ITEM_DEMANDA_SERVICO = """
DELETE FROM item_demanda_servico
WHERE id_demanda = ? AND id_servico = ?;
"""

OBTER_ITEM_DEMANDA_SERVICO_POR_ID = """
SELECT id_demanda, id_servico, quantidade, observacoes
FROM item_demanda_servico
WHERE id_demanda = ? AND id_servico = ?;
"""

OBTER_ITENS_POR_DEMANDA = """
SELECT id_demanda, id_servico, quantidade, observacoes
FROM item_demanda_servico
WHERE id_demanda = ?
ORDER BY id_servico ASC;
"""

OBTER_ITENS_DEMANDA_SERVICO_POR_PAGINA = """
SELECT id_demanda, id_servico, quantidade, observacoes
FROM item_demanda_servico
ORDER BY id_demanda ASC, id_servico ASC
LIMIT ? OFFSET ?;
"""
```

# sql/item_orcamento_produto_sql.py

```py
CRIAR_TABELA_ITEM_ORCAMENTO_PRODUTO = """
CREATE TABLE IF NOT EXISTS item_orcamento_produto (
    id_orcamento INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_orcamento, id_produto),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id) ON DELETE CASCADE
);
"""

INSERIR_ITEM_ORCAMENTO_PRODUTO = """
INSERT INTO item_orcamento_produto (id_orcamento, id_produto, preco_unitario, quantidade, observacoes)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR_ITEM_ORCAMENTO_PRODUTO = """
UPDATE item_orcamento_produto
SET preco_unitario = ?, quantidade = ?, observacoes = ?
WHERE id_orcamento = ? AND id_produto = ?;
"""

EXCLUIR_ITEM_ORCAMENTO_PRODUTO = """
DELETE FROM item_orcamento_produto
WHERE id_orcamento = ? AND id_produto = ?;
"""

OBTER_ITEM_ORCAMENTO_PRODUTO_POR_ID = """
SELECT id_orcamento, id_produto, preco_unitario, quantidade, observacoes
FROM item_orcamento_produto
WHERE id_orcamento = ? AND id_produto = ?;
"""

OBTER_ITENS_POR_ORCAMENTO = """
SELECT id_orcamento, id_produto, preco_unitario, quantidade, observacoes
FROM item_orcamento_produto
WHERE id_orcamento = ?
ORDER BY id_produto;
"""

OBTER_ITENS_ORCAMENTO_PRODUTO_POR_PAGINA = """
SELECT id_orcamento, id_produto, preco_unitario, quantidade, observacoes
FROM item_orcamento_produto
ORDER BY id_orcamento, id_produto
LIMIT ? OFFSET ?;
"""

CALCULAR_TOTAL_ITENS_PRODUTO_ORCAMENTO = """
SELECT SUM(preco_unitario * quantidade) as total
FROM item_orcamento_produto
WHERE id_orcamento = ?;
"""
```

# sql/item_orcamento_servico_sql.py

```py
CRIAR_TABELA_ITEM_ORCAMENTO_SERVICO = """
CREATE TABLE IF NOT EXISTS item_orcamento_servico (
    id_orcamento INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_orcamento, id_servico),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servico(id) ON DELETE CASCADE
);
"""

INSERIR_ITEM_ORCAMENTO_SERVICO = """
INSERT INTO item_orcamento_servico (id_orcamento, id_servico, preco_unitario, quantidade, observacoes)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR_ITEM_ORCAMENTO_SERVICO = """
UPDATE item_orcamento_servico
SET preco_unitario = ?, quantidade = ?, observacoes = ?
WHERE id_orcamento = ? AND id_servico = ?;
"""

EXCLUIR_ITEM_ORCAMENTO_SERVICO = """
DELETE FROM item_orcamento_servico
WHERE id_orcamento = ? AND id_servico = ?;
"""

OBTER_ITEM_ORCAMENTO_SERVICO_POR_ID = """
SELECT id_orcamento, id_servico, preco_unitario, quantidade, observacoes
FROM item_orcamento_servico
WHERE id_orcamento = ? AND id_servico = ?;
"""

OBTER_ITENS_POR_ORCAMENTO = """
SELECT id_orcamento, id_servico, preco_unitario, quantidade, observacoes
FROM item_orcamento_servico
WHERE id_orcamento = ?
ORDER BY id_servico;
"""

OBTER_ITENS_ORCAMENTO_SERVICO_POR_PAGINA = """
SELECT id_orcamento, id_servico, preco_unitario, quantidade, observacoes
FROM item_orcamento_servico
ORDER BY id_orcamento, id_servico
LIMIT ? OFFSET ?;
"""

CALCULAR_TOTAL_ITENS_SERVICO_ORCAMENTO = """
SELECT SUM(preco_unitario * quantidade) as total
FROM item_orcamento_servico
WHERE id_orcamento = ?;
"""
```

# sql/orcamento_sql.py

```py
CRIAR_TABELA_ORCAMENTO = """
CREATE TABLE IF NOT EXISTS orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_demanda INTEGER NOT NULL,
    id_fornecedor_prestador INTEGER NOT NULL,
    data_hora_cadastro TIMESTAMP NOT NULL,
    data_hora_validade TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'PENDENTE',
    observacoes TEXT,
    valor_total REAL,
    FOREIGN KEY (id_demanda) REFERENCES demanda(id) ON DELETE CASCADE,
    FOREIGN KEY (id_fornecedor_prestador) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

INSERIR_ORCAMENTO = """
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
                      data_hora_validade, status, observacoes, valor_total)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_ORCAMENTO = """
UPDATE orcamento
SET data_hora_validade = ?, status = ?, observacoes = ?, valor_total = ?
WHERE id = ?;
"""

ATUALIZAR_STATUS_ORCAMENTO = """
UPDATE orcamento
SET status = ?
WHERE id = ?;
"""

ATUALIZAR_VALOR_TOTAL_ORCAMENTO = """
UPDATE orcamento
SET valor_total = ?
WHERE id = ?;
"""

EXCLUIR_ORCAMENTO = """
DELETE FROM orcamento
WHERE id = ?;
"""

OBTER_ORCAMENTO_POR_ID = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE id = ?;
"""

OBTER_ORCAMENTOS_POR_DEMANDA = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE id_demanda = ?
ORDER BY data_hora_cadastro DESC;
"""

OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE id_fornecedor_prestador = ?
ORDER BY data_hora_cadastro DESC;
"""

OBTER_ORCAMENTOS_POR_STATUS = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE status = ?
ORDER BY data_hora_cadastro DESC;
"""

OBTER_ORCAMENTOS_POR_PAGINA = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
ORDER BY data_hora_cadastro DESC
LIMIT ? OFFSET ?;
"""

# Query específica para aceitar um orçamento e rejeitar outros da mesma demanda
ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS = """
UPDATE orcamento
SET status = CASE
    WHEN id = ? THEN 'ACEITO'
    ELSE 'REJEITADO'
END
WHERE id_demanda = ? AND status = 'PENDENTE';
"""
```

# sql/prestador_servico_sql.py

```py
CRIAR_TABELA_PRESTADOR_SERVICO = """
CREATE TABLE IF NOT EXISTS prestador_servico (
    id_prestador INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    observacoes TEXT NOT NULL,
    preco REAL,
    PRIMARY KEY (id_prestador, id_servico),
    FOREIGN KEY (id_prestador) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servico(id) ON DELETE CASCADE
);
"""

INSERIR_PRESTADOR_SERVICO = """
INSERT INTO prestador_servico (id_prestador, id_servico, observacoes, preco)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_PRESTADOR_SERVICO = """
UPDATE prestador_servico
SET observacoes = ?, preco = ?
WHERE id_prestador = ? AND id_servico = ?;
"""

EXCLUIR_PRESTADOR_SERVICO = """
DELETE FROM prestador_servico
WHERE id_prestador = ? AND id_servico = ?;
"""

OBTER_PRESTADOR_SERVICO_POR_ID = """
SELECT id_prestador, id_servico, observacoes, preco
FROM prestador_servico
WHERE id_prestador = ? AND id_servico = ?;
"""

OBTER_PRESTADORES_SERVICO_POR_PAGINA = """
SELECT id_prestador, id_servico, observacoes, preco
FROM prestador_servico
ORDER BY id_prestador ASC
LIMIT ? OFFSET ?;
"""
```

# sql/produto_sql.py

```py
CRIAR_TABELA_PRODUTO = """
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT NOT NULL
);
"""

INSERIR_PRODUTO = """
INSERT INTO produto (nome, preco, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR_PRODUTO = """
UPDATE produto
SET nome = ?, preco = ?, descricao = ?
WHERE id = ?;
"""

EXCLUIR_PRODUTO = """
DELETE FROM produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_ID = """
SELECT id, nome, preco, descricao
FROM produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_NOME = """
SELECT id, nome, preco, descricao
FROM produto
WHERE nome = ?;
"""

OBTER_PRODUTOS_POR_PAGINA = """
SELECT id, nome, preco, descricao
FROM produto
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""
```

# sql/servico_sql.py

```py
CRIAR_TABELA_SERVICO = """
CREATE TABLE IF NOT EXISTS servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT NOT NULL
);
"""

INSERIR_SERVICO = """
INSERT INTO servico (nome, preco, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR_SERVICO = """
UPDATE servico
SET nome = ?, preco = ?, descricao = ?
WHERE id = ?;
"""

EXCLUIR_SERVICO = """
DELETE FROM servico
WHERE id = ?;
"""

OBTER_SERVICO_POR_ID = """
SELECT id, nome, preco, descricao
FROM servico
WHERE id = ?;
"""

OBTER_SERVICO_POR_NOME = """
SELECT id, nome, preco, descricao
FROM servico
WHERE nome = ?;
"""

OBTER_SERVICOS_POR_PAGINA = """
SELECT id, nome, preco, descricao
FROM servico
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""
```

# sql/usuario_sql.py

```py
CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'cliente',
    foto TEXT,
    token_redefinicao TEXT,
    data_token TIMESTAMP,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERIR_USUARIO = """
INSERT INTO Usuario (nome, telefone, email, senha_hash, tipo, documento)
VALUES (?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE Usuario
SET nome = ?, telefone = ?, email = ?, documento = ?
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
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
WHERE email = ?;
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

OBTER_USUARIOS_POR_TIPO_POR_PAGINA = """
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
WHERE tipo = ?
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""
```

# static/css/login.css

```css
form {
  border: 3px solid #f1f1f1;
}

/* Full-width inputs */
input[type=text], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Set a style for all buttons */
button {
  background-color: #04AA6D;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}

/* Add a hover effect for buttons */
button:hover {
  opacity: 0.8;
}

/* Extra style for the cancel button (red) */
.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;
}

/* Center the avatar image inside this container */
.imgcontainer {
  text-align: center;
  margin: 24px 0 12px 0;
}

/* Avatar image */
img.avatar {
  width: 40%;
  border-radius: 50%;
}

/* Add padding to containers */
.container {
  padding: 16px;
}

/* The "Forgot password" text */
span.psw {
  float: right;
  padding-top: 16px;
}

/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
  span.psw {
    display: block;
    float: none;
  }
  .cancelbtn {
    width: 100%;
  }
}
```

# static/css/styles.css

```css
.tittle {
    background-color: #f8f4f2;
}

body {
    margin: 0;
    font-family: "Lora", serif;
    background-color: #fefefe;
}

.cor_texto_rosa_empoeirado {
    color: #f8b4c2 !important;
}

.cor_fundo_rosa_empoeirado {
    background-color: #f8b4c2 !important;
}


.navbar-custom {
    background-color: #f8f4f2;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    position: relative;
}

.navbar-brand {
    font-family: "Playfair Display", serif;
    font-size: 1.8rem;
    font-weight: 600;
    margin: auto;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    color: #4e3b31;
}

.menu-icon {
    font-size: 1.5rem;
    color: #4e3b31;
    cursor: pointer;
}

.grid-image {
    position: relative;
    overflow: hidden;
    height: 100%;
    cursor: pointer;
}

.grid-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.grid-image:hover img {
    transform: scale(1.05);
}

.grid-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    color: white;
    padding: 1rem;
    transition: background 0.4s;
}

.grid-image:hover .grid-overlay {
    background: rgba(0, 0, 0, 0.5);
}

.grid-overlay h5 {
    font-size: 1.5rem;
    font-weight: 500;
}

.grid-overlay small {
    font-size: 0.9rem;
    opacity: 0.8;
}

.card-img-top {
    height: 350px;
    width: 100%;
    object-fit: cover;
}

.btn-custom {
    background-color: #4e3b31;
    color: white;
    border: none;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    transition: background-color 0.3s ease;
}

.btn-custom:hover {
    background-color: #3b2e26;
}

@media (max-width: 768px) {
    .navbar-brand {
        font-size: 1.4rem;
    }

    .grid-overlay h5 {
        font-size: 1.2rem;
    }

    .card-img-top {
        height: 280px;
    }
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.titulo {
    font-size: 2.5rem;
    font-weight: 600;
}

.descricao {
    font-size: 1.1rem;
    color: #444;
}

.preco {
    font-weight: bold;
    color: #111;
}

.parcelado {
    font-size: 0.9rem;
    color: #777;
}

.produto-hover {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.produto-hover:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    z-index: 2;
}

/*menu */

.menu-topo {
    position: sticky;
    top: 0;
    background-color: #fff;
    z-index: 1000;
    padding: 0.5rem 1rem;
}

.menu-title {
    font-size: 1rem;
    text-transform: uppercase;
}

.menu-topo .nav-link {
    color: #000;
    font-size: 0.9rem;
    padding: 0.5rem 0.75rem;
}

.menu-topo .nav-link.active,
.menu-topo .nav-link:hover {
    font-weight: bold;
    color: #000;
}

/*vermais vestido */

/* Reset e configurações gerais */
* {
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
    color: #333;
    line-height: 1.6;
}

/* Container principal */
.container-fluid {
    padding: 0;
}

/* Seção da imagem do produto */
.product-image-container {
    max-width: 500px;
    width: 100%;
}

.product-image {
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.product-image:hover {
    transform: scale(1.02);
}

/* Seção de informações do produto */
.product-info {
    max-width: 600px;
}

/* Título do produto */
.product-title {
    font-size: 2rem;
    font-weight: 400;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    line-height: 1.3;
}

/* Marca e referência */
.product-brand {
    font-size: 1.1rem;
    color: #6c757d;
    margin-bottom: 0.25rem;
}

.product-reference {
    font-size: 0.9rem;
    color: #adb5bd;
    margin-bottom: 1.5rem;
}

/* Seção de disponibilidade */
.availability-section {
    margin-bottom: 2rem;
}

.availability-box {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.availability-box p {
    color: #6c757d;
    font-size: 0.95rem;
    margin: 0;
}

/* Botão de contato */
.btn-contact {
    background-color: #495057;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1.1rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.btn-contact:hover {
    background-color: #343a40;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-contact:focus {
    box-shadow: 0 0 0 3px rgba(73, 80, 87, 0.25);
}

/* Abas personalizadas */
.nav-tabs {
    border-bottom: 1px solid #dee2e6;
    margin-bottom: 1rem;
}

.custom-tab {
    border: none;
    background: none;
    color: #6c757d;
    font-size: 0.95rem;
    padding: 0.75rem 1rem;
    margin-right: 2rem;
    border-bottom: 2px solid transparent;
    transition: all 0.3s ease;
}

.custom-tab:hover {
    color: #495057;
    border-bottom-color: #dee2e6;
}

.custom-tab.active {
    color: #495057;
    border-bottom-color: #495057;
    font-weight: 500;
}

.custom-tab:focus {
    box-shadow: none;
}

/* Conteúdo das abas */
.tab-content {
    padding-top: 1rem;
}

.tab-text {
    color: #6c757d;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
}

/* Responsividade */
@media (max-width: 991.98px) {
    .product-title {
        font-size: 1.75rem;
    }
    
    .product-info {
        padding: 2rem !important;
    }
    
    .custom-tab {
        margin-right: 1rem;
        font-size: 0.9rem;
    }
}

@media (max-width: 767.98px) {
    .product-title {
        font-size: 1.5rem;
    }
    
    .product-info {
        padding: 1.5rem !important;
    }
    
    .custom-tab {
        margin-right: 0.5rem;
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
    }
    
    .btn-contact {
        font-size: 1rem;
    }
}

/* Animações suaves */
.product-info > * {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Melhorias de acessibilidade */
.btn-contact:focus,
.custom-tab:focus {
    outline: 2px solid #495057;
    outline-offset: 2px;
}

/* Hover states para melhor UX */
.availability-box:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
}

```

# static/img/img_home/card1.jpg

This is a binary file of the type: Image

# static/img/img_home/card2.jpg

This is a binary file of the type: Image

# static/img/img_home/card3.jpg

This is a binary file of the type: Image

# static/img/img_home/casamento1.jpg

This is a binary file of the type: Image

# static/img/img_home/primeiracol.jpg

This is a binary file of the type: Image

# static/img/img_home/segundacol.jpg

This is a binary file of the type: Image

# static/img/img_home/terceiracol.jpg

This is a binary file of the type: Image

# static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido1.jpg

This is a binary file of the type: Image

# static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido2.jpg

This is a binary file of the type: Image

# static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido3.jpg

This is a binary file of the type: Image

# static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido4.jpg

This is a binary file of the type: Image

# static/img/img_produtoseservicos/img_produtoseservicos_vestidos/produtoseserviços_fotoprincipal_vestido.jpg

This is a binary file of the type: Image

# static/img/img_produtoseservicos/img_produtoseservicos_vestidos/vermais_card_vestido1.jpg

This is a binary file of the type: Image

# static/img/logo_preto.svg

This is a file of the type: SVG Image

# static/img/Logotipos Case Bem Figma.svg

This is a file of the type: SVG Image

# static/img/Logotipos Case Bem.png

This is a binary file of the type: Image

# static/img/produtos/casamento_decoracao.png

This is a binary file of the type: Image

# static/img/produtos/decoracaocasamento.png

This is a binary file of the type: Image

# static/img/produtos/espacocasamento.png

This is a binary file of the type: Image

# static/img/produtos/fotografia.jpg

This is a binary file of the type: Image

# static/img/produtos/joias.jpg

This is a binary file of the type: Image

# static/img/produtos/lembrancinha-biscoitos.jpg

This is a binary file of the type: Image

# static/img/produtos/musica.jpg

This is a binary file of the type: Image

# static/img/produtos/transportenoivos.png

This is a binary file of the type: Image

# static/img/produtos/vestido_terno.png

This is a binary file of the type: Image

# static/img/produtos/vestido-noiva.png

This is a binary file of the type: Image

# static/img/produtos/vintage-convite.jpg

This is a binary file of the type: Image

# static/img/svg/svgexport-1.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-3.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-4.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-5.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-6.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-7.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-8.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-16.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-18.svg

This is a file of the type: SVG Image

# static/img/svg/svgexport-21.svg

This is a file of the type: SVG Image

# static/js/scripts.js

```js

```

# templates/fornecedor/vestidos/card_vestido1.html

```html
{% extends "base.html" %}
{% block conteudo %}

<!-- ESSA É A PÁGINA DE VER MAIS-->

<div class="container-fluid bg-light min-vh-100">
        <div class="row h-100">
            <!-- Seção da Imagem -->
            <div class="col-lg-6 d-flex align-items-center justify-content-center p-5">
                <div class="product-image-container">
                    <img src="/static/img/img_produtoseservicos/img_produtoseservicos_vestidos/vermais_card_vestido1.jpg" 
                         alt="" 
                         class="img-fluid product-image">
                </div>
            </div>

            <!-- Seção das Informações do Produto -->
            <div class="col-lg-6 d-flex align-items-center">
                <div class="product-info w-100 p-5">
                    <!-- Título e Marca -->
                    <div class="mb-4">
                        <h1 class="product-title mb-2">Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim, illo!</h1>
                        <p class="product-brand text-muted mb-1">Lorem ipsum dolor sit amet.</p>
                    </div>

                    <!-- Disponibilidade -->
                    <div class="availability-section mb-4">
                        <div class="availability-box p-3 rounded">
                            <p class="mb-0 text-center">Lorem, ipsum dolor.</p>
                        </div>
                    </div>

                    <!-- Botão de Contato -->
                    <div class="contact-section mb-4">
                        <button class="btn btn-contact w-100 py-3">
                            <a href="/contato_vestido1"> Contato</a>
                        </button>
                    </div>

                    <!-- Abas de Informações -->
                    <div class="product-tabs">
                        <ul class="nav nav-tabs border-0" id="productTabs" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active custom-tab" id="description-tab" data-bs-toggle="tab" 
                                        data-bs-target="#description" type="button" role="tab">
                                    Descrição
                                </button>
                            </li>
                        </ul>
                        
                        <div class="tab-content mt-3" id="productTabsContent">
                            <div class="tab-pane fade show active" id="description" role="tabpanel">
                                <p class="tab-text">Lorem ipsum dolor sit amet consectetur adipisicing elit. In sit quas sed quam accusamus error ratione eos! Ex, nostrum! Magni distinctio officia dolorem reprehenderit excepturi iure temporibus maxime veniam corrupti nesciunt ipsam quidem dolores quasi odit praesentium numquam nemo obcaecati eius velit exercitationem, rem sit adipisci. Repudiandae dolor sunt itaque!</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>




{% endblock conteudo %}

```

# templates/fornecedor/vestidos/contato_vestido1.html

```html
{% extends "base.html" %}
{% block conteudo %}


{% endblock conteudo %}

```

# templates/fornecedor/vestidos/produtoseservicos_vestidos.html

```html
{% extends "base.html" %}
{% block conteudo %}

<body>

    <!-- Menu Flutuante -->

    <nav class="menu-topo shadow-sm">
        <div class="container-fluid d-flex align-items-center">
            <span class="menu-title fw-bold">Encontre o que você precisa</span>
            <ul class="nav ms-4">
                <li class="nav-item"><a href="#" class="nav-link">Acessórios</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Alianças</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Bolos</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Bridal Day</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Buffet</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Cenografia e Sonoplastia</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Convites</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Floristas</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Fotógrafos</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Lembranças</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Locais</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Ternos</a></li>
                <li class="nav-item"><a href="#" class="nav-link active">Vestidos</a></li>
            </ul>
        </div>
    </nav>


    <!-- VESTIDOS -->

    <section class="container-fluid py-5">
        <div class="row align-items-center">
            <div class="col-md-6 text-center text-md-start px-5">
                <h2 class="titulo">Vestidos</h2>
                <p class="descricao">
                    Lorem ipsum dolor, sit amet consectetur adipisicing elit. Perferendis sapiente earum, ea, dolorem
                    veritatis
                    laboriosam labore, laborum aspernatur fuga at ut? Sunt odio aut pariatur optio ut? Officia esse
                    incidunt
                    tempora ex iusto sunt illum nulla. Aliquam mollitia iste, quos laborum vitae pariatur nemo impedit
                    possimus
                    eos! Perspiciatis, alias dolores.
                </p>
            </div>
            <div class="col-md-6 text-center">
                <img src="/static/img/img_produtoseservicos/img_produtoseservicos_vestidos/produtoseserviços_fotoprincipal_vestido.jpg" alt=""
                    class="img-fluid rounded">
            </div>
        </div>
    </section>
    <section class="container my-5">
        <div class="row text-center">
            <h3 class="mb-4">Coleção</h3>
            <div class="col-md-3 mb-4">
                <div class="card h-100 produto-hover">
                    <img src="/static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido1.jpg" class="card-img-top" alt="">
                    <div class="card-body">
                        <h6 class="card-title">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ut, facilis.
                        </h6>
                        <p class="preco">R$ 44.800,00</p>
                        <p class="parcelado">Ou em até 10x de R$ 4.480,00</p>
                        <a href="/card_vestido1"
                            class="btn btn-outline-dark btn-sm mt-2">Ver Detalhes</a>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="card h-100 produto-hover">
                    <img src="/static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido2.jpg" class="card-img-top"
                        alt="Anel Ouro Amarelo">
                    <div class="card-body">
                        <h6 class="card-title">
                            Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illum, quia?
                        </h6>
                        <p class="preco">R$ 44.800,00</p>
                        <p class="parcelado">Ou em até 10x de R$ 4.480,00</p>
                        <a href="#" class="btn btn-outline-dark btn-sm mt-2">Ver Detalhes</a>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="card h-100 produto-hover">
                    <img src="/static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido3.jpg" class="card-img-top"
                        alt="Anel Ouro Amarelo">
                    <div class="card-body">
                        <h6 class="card-title">
                            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Debitis, ad.
                        </h6>
                        <p class="preco">R$ 44.800,00</p>
                        <p class="parcelado">Ou em até 10x de R$ 4.480,00</p>
                        <a href="#" class="btn btn-outline-dark btn-sm mt-2">Ver Detalhes</a>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="card h-100 produto-hover">
                    <img src="/static/img/img_produtoseservicos/img_produtoseservicos_vestidos/card_vestido4.jpg" class="card-img-top"
                        alt="Anel Ouro Amarelo">
                    <div class="card-body">
                        <h6 class="card-title">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. A, illum.
                        </h6>
                        <p class="preco">R$ 44.800,00</p>
                        <p class="parcelado">Ou em até 10x de R$ 4.480,00</p>
                        <a href="#" class="btn btn-outline-dark btn-sm mt-2">Ver Detalhes</a>
                    </div>
                </div>
            </div>
    </section>
    {% endblock conteudo %}
```

# templates/publico/base.html

```html
<!DOCTYPE html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="/static/css/styles.css">
        <title>Case Bem</title>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Case Bem</a>
                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/produtos">Produtos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/servicos">Serviços</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/locais">Locais</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/login">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/cadastro">Cadastro</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/sobre">Sobre</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/contato">Contato</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <main>
            {% block conteudo %}
            {% endblock %}
        </main>
        <footer class="mt-5 text-center text-muted py-4 bg-white">
            <div class="container">
                <p class="mb-1">
                    <img src="/static/img/logo_preto.svg" alt="Logotipo Case Bem" width="128">
                </p>
                <p class="mb-1">Inspiração e organização para o seu grande dia.</p>
                <div class="d-flex justify-content-center gap-3 mt-2">
                    <a href="/sobre" class="text-muted text-decoration-none">Sobre</a>
                    <a href="/contato" class="text-muted text-decoration-none">Contato</a>
                </div>
                <small class="d-block mt-3">&copy; 2025 Case Bem. Todos os direitos reservados.</small>
            </div>
        </footer>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
        <script src="/static/js/scripts.js"></script>
    </body>
</html>

```

# templates/publico/cadastro.html

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background:url('casamento2.jpg');
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            border-radius: 15px;
            padding: 20px;
            width: 100%;
            max-width: 400px;
        }
        .btn-custom {
            background-color: #6f42c1;
            color: white;
            border-radius: 25px;
            padding: 10px;
            width: 100%;
        }
        #senhaForca {
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="card shadow">
    <div class="text-center mb-3">
        <i class="fas fa-user-plus fa-2x text-primary"></i>
        <h3 class="mt-2">Criar Conta</h3>
        <small>Preencha os dados abaixo para se cadastrar</small>
    </div>

    <form id="formCadastro">
        <div class="mb-3">
            <label class="form-label">Nome Completo</label>
            <input type="text" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">E-mail</label>
            <input type="email" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Telefone</label>
            <input type="tel" class="form-control" placeholder="(XX) XXXXX-XXXX" required>
        </div>

        <div class="mb-3">
            <label class="form-label">CPF</label>
            <input type="text" id="cpf" class="form-control" placeholder="000.000.000-00" required>
            <div class="invalid-feedback">CPF inválido.</div>
        </div>

        <div class="mb-3">
            <label class="form-label">Data de Nascimento</label>
            <input type="date" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Gênero</label>
            <div>
                <input type="radio" name="genero" required> Masculino
                <input type="radio" name="genero" class="ms-3"> Feminino
                <input type="radio" name="genero" class="ms-3"> Outro
            </div>
        </div>

        <div class="mb-3">
            <label class="form-label">Senha</label>
            <input type="password" id="senha" class="form-control" required>
            <small id="senhaForca" class="text-muted">A senha deve ter pelo menos 8 caracteres.</small>
        </div>

        <div class="mb-3">
            <label class="form-label">Confirmar Senha</label>
            <input type="password" id="confirmarSenha" class="form-control" required>
            <div class="invalid-feedback">As senhas não coincidem.</div>
        </div>

        <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" required>
            <label class="form-check-label">
                Eu concordo com os <a href="#">Termos de Uso</a> e <a href="#">Política de Privacidade</a>
            </label>
        </div>

        <div class="form-check mb-4">
            <input class="form-check-input" type="checkbox">
            <label class="form-check-label">
                Desejo receber novidades e promoções por e-mail
            </label>
        </div>
        
        <button type="submit" class="btn btn-custom">Entrar</button>
        <div class="text-center mb-3">
            <small>Já tem uma conta? <a href="login.html">Faça login</a></small>
    </form>
</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<script>
    // Validação de CPF
    function validarCPF(cpf) {
        cpf = cpf.replace(/[^\d]+/g, '');
        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;

        let soma = 0;
        for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
        let resto = 11 - (soma % 11);
        if (resto === 10 || resto === 11) resto = 0;
        if (resto !== parseInt(cpf.charAt(9))) return false;

        soma = 0;
        for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
        resto = 11 - (soma % 11);
        if (resto === 10 || resto === 11) resto = 0;
        return resto === parseInt(cpf.charAt(10));
    }

    document.getElementById("cpf").addEventListener("input", function() {
        if (!validarCPF(this.value)) {
            this.classList.add("is-invalid");
            this.classList.remove("is-valid");
        } else {
            this.classList.remove("is-invalid");
            this.classList.add("is-valid");
        }
    });

    // Medidor de força de senha
    document.getElementById("senha").addEventListener("input", function() {
        let senha = this.value;
        let forcaTexto = document.getElementById("senhaForca");

        let forca = 0;
        if (senha.length >= 8) forca++;
        if (/[A-Z]/.test(senha)) forca++;
        if (/[0-9]/.test(senha)) forca++;
        if (/[^A-Za-z0-9]/.test(senha)) forca++;

        if (forca <= 1) {
            forcaTexto.textContent = "Senha fraca";
            forcaTexto.className = "text-danger";
        } else if (forca === 2) {
            forcaTexto.textContent = "Senha média";
            forcaTexto.className = "text-warning";
        } else if (forca >= 3) {
            forcaTexto.textContent = "Senha forte";
            forcaTexto.className = "text-success";
        }
    });

    // Validação de confirmação de senha
    document.getElementById("formCadastro").addEventListener("submit", function(e) {
        let senha = document.getElementById("senha");
        let confirmarSenha = document.getElementById("confirmarSenha");

        if (senha.value !== confirmarSenha.value) {
            confirmarSenha.classList.add("is-invalid");
            e.preventDefault();
        } else {
            confirmarSenha.classList.remove("is-invalid");
        }
    });
</script>

</body>
</html>
```

# templates/publico/detalhes_do_fornecedor_x.html

```html
<h1>Página com detalhes do fornecedor, mostrando os produtos dele daquela categoria</h1>
<h1>Quando clica no produto leva pra página detalhes_do_produto_x.html</h1>
```

# templates/publico/detalhes_do_local_x.html

```html
<h1>Página que mostra os detalhes do local escolhido e leva pro chat</h1>
```

# templates/publico/detalhes_do_prestador.html

```html
{% extends "base.html" %}
{% block conteudo %}


<h1>Página com detalhes do prestador, mostrando os servicos dele daquela categoria</h1>
<h1>Quando clica no servico leva pra página detalhes_do_servico_x.html</h1>






{% endblock conteudo %}
```

# templates/publico/detalhes_do_produto_x.html

```html
<h1>Página com detalhes do produto escolhido, tem um botão pra levar ao chat</h1>
```

# templates/publico/detalhes_do_servico.html

```html
<h1>Página com detalhes do servico escolhido, tem um botão pra levar ao chat</h1>
```

# templates/publico/fornecedores_x.html

```html
{% extends "base.html" %}
{% block conteudo %}


<h1>PÁGINA MOSTRANDO OS FORNECEDORES DO PRODUTO X</h1>
<h1>QUANDO CLICAR EM UM DELES, VAI LEVAR PRA UMA PÁGINA IDENTICA A ESSA, COM OS PRODUTOS X DAQUELE FORNECEDOR ESCOLHIDO (detalhes_do_fornecedor_x.html) </h1>






{% endblock conteudo %}
```

# templates/publico/home.html

```html
{% extends "publico/base.html" %}
{% block conteudo %}
<div class="container-fluid px-0">
    <div class="row g-0 row-cols-1 row-cols-md-3">
        <div class="col">
            <a href="#pret-a-porter" class="text-decoration-none">
                <div class="grid-image">
                    <img src="/static/img/img_home/terceiracol.jpg" alt="Prêt-à-porter">
                    <div class="grid-overlay">
                        <h5>Vestimentas</h5>
                        <small>Descubra os melhores looks</small>
                    </div>
                </div>
            </a>
        </div>
        <div class="col">
            <a href="#novidades" class="text-decoration-none">
                <div class="grid-image">
                    <img src="/static/img/img_home/segundacol.jpg" alt="Novidades">
                    <div class="grid-overlay">
                        <h5>Locais</h5>
                        <small>Explore novos horizontes</small>
                    </div>
                </div>
            </a>
        </div>
        <div class="col">
            <a href="/produtos" class="text-decoration-none">
                <div class="grid-image">
                    <img src="/static/img/img_home/primeiracol.jpg" alt="Óculos">
                    <div class="grid-overlay">
                        <h5>Produtos e serviços</h5>
                        <small>Contate os melhores profissionais</small>
                    </div>
                </div>
            </a>
        </div>
    </div>
</div>
<div class="container py-5">
    <h3 class="mb-4 text-center" style="font-family: 'Playfair Display', serif">
        Destaques da Temporada
    </h3>
    <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="col">
            <div class="card h-100 shadow-sm border-0">
                <img src="/static/img/img_home/card2.jpg" class="card-img-top" alt="Vestido de Noiva">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">Tendências em Vestidos</h5>
                    <p class="card-text">Conheça os estilos mais desejados do ano para vestidos de noiva.</p>
                    <div class="mt-auto d-flex justify-content-center">
                        <a href="#pret-a-porter" class="btn btn-custom">Ver mais</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col">
            <div class="card h-100 shadow-sm border-0">
                <img src="/static/img/img_home/card1.jpg" class="card-img-top" alt="Local para Casamento">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">Espaços Inesquecíveis</h5>
                    <p class="card-text">Locações encantadoras para cerimônias ao ar livre e clássicas.</p>
                    <div class="mt-auto d-flex justify-content-center">
                        <a href="#novidades" class="btn btn-custom">Ver mais</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col">
            <div class="card h-100 shadow-sm border-0">
                <img src="/static/img/img_home/card3.jpg" class="card-img-top" alt="Detalhes do Evento">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">Detalhes que Encantam</h5>
                    <p class="card-text">Ideias criativas para lembrancinhas, decoração e papelaria personalizada.</p>
                    <div class="mt-auto d-flex justify-content-center">
                        <a href="#oculos" class="btn btn-custom">Ver mais</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock conteudo %}

```

# templates/publico/locais.html

```html
<h1>Página que mostra os locais disponíveis</h1>
```

# templates/publico/login.html

```html
{% extends "publico/base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <center><h2>Login</h2></center>
            
            {% if erro %}
            <div class="alert alert-danger">{{ erro }}</div>
            {% endif %}
            
            <form method="post" action="/login">
                {% if redirect %}
                <input type="hidden" name="redirect" value="{{ redirect }}">
                {% endif %}
                
                <div class="mb-3">
                    <label for="email" class="form-label">E-mail</label>
                    <input type="email" class="form-control" id="email" 
                           name="email" required>
                </div>
                
                <div class="mb-3">
                    <label for="senha" class="form-label">Senha</label>
                    <input type="password" class="form-control" id="senha" 
                           name="senha" required>
                </div>
                
               <center><button type="submit" class="btn btn-primary">Entrar</button></center> 
                <center><a href="/esqueci-senha" class="btn btn-link">Esqueci minha senha</a><center>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

# templates/publico/prestadores_x.html

```html
{% extends "base.html" %}
{% block conteudo %}


<h1>PÁGINA MOSTRANDO OS PRESTADORES DO SERVICO X</h1>
<h1>QUANDO CLICAR EM UM DELES, VAI LEVAR PRA UMA PÁGINA IDENTICA A ESSA, COM OS SERVIOS X DAQUELE PRESTADOR ESCOLHIDO (detalhes_do_prestador_x.html) </h1>






{% endblock conteudo %}
```

# templates/publico/produtos.html

```html
{% extends "base.html" %}
{% block conteudo %}


<h1>PÁGINA MOSTRANDO AS CATEGORIAS DE PRODUTOS</h1>
<h1>QUANDO CLICAR NA CATEGORIA X, VAI LEVAR PRA UMA PÁGINA MOSTRANDO OS FORNECEDORES DO PRODUTO X (FORNECEDORES_X.HTML)</h1>






{% endblock conteudo %}

```

# templates/publico/servicos.html

```html
{% extends "base.html" %}
{% block conteudo %}

<h1>PÁGINA MOSTRANDO AS CATEGORIAS DE PRODUTOS</h1>
<h1>QUANDO CLICAR NA CATEGORIA X, VAI LEVAR PRA UMA PÁGINA MOSTRANDO OS FORNECEDORES DO PRODUTO X (FORNECEDORES_X.HTML)</h1>






{% endblock conteudo %}

```

# templates/publico/sobre.html

```html
{% extends "publico/base.html" %}
{% block conteudo %}
<!-- Seção Sobre -->
<section class="about-section py-5">
    <div class="container">
        <div class="row align-items-center">
            <!-- Texto -->
            <div class="col-md-6 mb-4 mb-md-0">
                <h2 class="section-title">Sobre Nós</h2>
                <p class="lead">
                    Somos uma marca dedicada a trazer elegância e sofisticação para momentos únicos. 
            Nossa coleção é pensada para unir tradição, modernidade e cuidado em cada detalhe.
                </p>
                <p>
                    Do primeiro esboço ao acabamento final, cada peça é feita para celebrar histórias especiais. 
            Valorizamos a exclusividade, o conforto e a qualidade, oferecendo uma experiência completa 
            para quem busca mais que um produto: busca memórias inesquecíveis.
                </p>
                <button class="btn btn-dark mt-3">Saiba Mais</button>
            </div>
            <!-- Imagem -->
            <div class="col-md-6 text-center">
                <img src="img/about.jpg" alt="Sobre nós" class="img-fluid rounded shadow">
            </div>
        </div>
    </div>
</section>
{% endblock conteudo %}

```

# templates/publico/teste.html

```html
{% extends "base.html" %}
{% block conteudo %}

<!-- Menu Flutuante -->

<nav class="menu-topo shadow-sm">
    <div class="container-fluid d-flex align-items-center">
        <span class="menu-title fw-bold">Encontre o que você precisa</span>
        <ul class="nav ms-4">
            <li class="nav-item"><a href="#" class="nav-link">Acessórios</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Alianças</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Bolos</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Bridal Day</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Buffet</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Cenografia e Sonoplastia</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Convites</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Floristas</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Fotógrafos</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Lembranças</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Locais</a></li>
            <li class="nav-item"><a href="#" class="nav-link">Ternos</a></li>
            <li class="nav-item"><a href="/produtoseservicos_vestidos" class="nav-link">Vestidos</a></li>
        </ul>
    </div>
</nav>

<h1>PÁGINA MOSTRANDO AS CATEGORIAS DE PRODUTOS</h1>
<h1>QUANDO CLICAR NA CATEGORIA X, VAI LEVAR PRA UMA PÁGINA MOSTRANDO OS FORNECEDORES DO PRODUTO X (FORNECEDORES_X.HTML)</h1>






{% endblock conteudo %}






```

# templates/usuario/alterar_senha.html

```html
{% extends "base.html" %}
{% block conteudo %}
<h1>Alteração de Senha</h1>
<hr>
{% endblock conteudo %}
```

# templates/usuario/chat.html

```html
{% extends "base.html" %}
{% block conteudo %}
<h1>Detalhes de Conversa</h1>
<hr>
{% endblock conteudo %}
```

# templates/usuario/conversas.html

```html
{% extends "base.html" %}
{% block conteudo %}
<h1>Histórico de Conversas</h1>
<hr>
<a href="/usuario/conversas/1"></a>
{% endblock conteudo %}
```

# tests/__init__.py

```py

```

# tests/conftest.py

```py
from datetime import datetime
import pytest
import os
import sys
import tempfile

from model.usuario_model import Usuario

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
    usuario = Usuario(0, "Usuário Teste", "(28) 99999-0000", "usuario@email.com", "123456", "ADMIN", "123.456.789-00")
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
def noivo_exemplo():
    # Cria um noivo de exemplo para os testes
    from model.usuario_model import Usuario
    noivo = Usuario(0, "Noivo Teste", "(28) 99999-0000", "noivo@email.com", "123456", "NOIVO", "123.456.789-00")
    return noivo

@pytest.fixture
def lista_noivos_exemplo():
    # Cria uma lista de 10 noivos de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Noivo {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", "NOIVO", f"123.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def prestador_exemplo():
    # Cria um prestador de exemplo para os testes
    from model.usuario_model import Usuario
    prestador = Usuario(0, "Prestador Teste", "(28) 99999-2000", "prestador@email.com", "123456", "PRESTADOR", "223.456.789-00")
    return prestador

@pytest.fixture
def lista_prestadores_exemplo():
    # Cria uma lista de 10 prestadores de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Prestador {i:02d}", f"(28) 99999-20{i:02d}", f"prestador{i:02d}@email.com", "123456", "PRESTADOR", f"223.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def fornecedor_exemplo():
    # Cria um fornecedor de exemplo para os testes
    from model.usuario_model import Usuario
    fornecedor = Usuario(0, "Fornecedor Teste", "(28) 99999-3000", "fornecedor@email.com", "123456", "FORNECEDOR", "323.456.789-00")
    return fornecedor

@pytest.fixture
def lista_fornecedores_exemplo():
    # Cria uma lista de 10 fornecedores de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Fornecedor {i:02d}", f"(28) 99999-30{i:02d}", f"fornecedor{i:02d}@email.com", "123456", "FORNECEDOR", f"323.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def administrador_exemplo():
    # Cria um administrador de exemplo para os testes
    from model.usuario_model import Usuario
    administrador = Usuario(0, "Administrador Teste", "(28) 99999-4000", "admin@email.com", "123456", "ADMIN", "423.456.789-00")
    return administrador

@pytest.fixture
def lista_administradores_exemplo():
    # Cria uma lista de 10 administradores de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Administrador {i:02d}", f"(28) 99999-40{i:02d}", f"admin{i:02d}@email.com", "123456", "ADMIN", f"423.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def casal_exemplo():
    # Cria um casal de exemplo para os testes    
    from model.casal_model import Casal
    casal = Casal(0, 1, 2, 10000.0)
    return casal

@pytest.fixture
def lista_casais_exemplo():
    # Cria uma lista de 10 casais de exemplo para os testes    
    from model.casal_model import Casal
    casais = []
    for i in range(1, 11, 2):
        casal = Casal(0, i, i + 1, 10000.0 + (i * 100))
        casais.append(casal)
    return casais

@pytest.fixture
def servico_exemplo():
    # Cria um serviço de exemplo para os testes
    from model.servico_model import Servico
    servico = Servico(0, "Serviço Teste", 100.0, "Descrição do serviço")
    return servico

@pytest.fixture
def lista_servicos_exemplo():
    # Cria uma lista de 10 serviços de exemplo para os testes
    from model.servico_model import Servico
    servicos = []
    for i in range(1, 11):
        servico = Servico(0, f"Serviço {i:02d}", 100.0 * i, f"Descrição do serviço {i:02d}")
        servicos.append(servico)
    return servicos

@pytest.fixture
def produto_exemplo():
    # Cria um produto de exemplo para os testes
    from model.produto_model import Produto
    produto = Produto(0, "Produto Teste", 19.99, "Descrição do produto teste")
    return produto

@pytest.fixture
def lista_produtos_exemplo():  
    # Cria uma lista de 10 produtos de exemplo para os testes
    from model.produto_model import Produto
    produtos = []
    for i in range(1, 11):
        produto = Produto(0, f"Produto {i:02d}", 19.99 + i, f"Descrição do produto {i:02d}")
        produtos.append(produto)
    return produtos    

@pytest.fixture
def demanda_exemplo():
    # Cria um demanda de exemplo para os testes
    from model.demanda_model import Demanda
    demanda = Demanda(0, 1, datetime.now())
    return demanda

@pytest.fixture
def lista_demandas_exemplo():
    # Cria uma lista de 10 demandas de exemplo para os testes
    from model.demanda_model import Demanda
    demandas = []
    for i in range(1, 11):
        demanda = Demanda(0, i, datetime.now())
        demandas.append(demanda)
    return demandas

@pytest.fixture
def chat_exemplo():
    # Cria um chat de exemplo para os testes
    from model.chat_model import Chat
    chat = Chat(1, 2, datetime.now(), "Mensagem de teste", None)
    return chat

@pytest.fixture
def fornecedor_produto_exemplo():
    # Cria uma relação fornecedor-produto de exemplo para os testes
    from model.fornecedor_model import Fornecedor
    fp = Fornecedor(1, 1, "Observações teste", 50.0)
    return fp

@pytest.fixture
def prestador_servico_exemplo():
    # Cria uma relação prestador-serviço de exemplo para os testes
    from model.prestador_servico_model import Prestador
    ps = Prestador(1, 1, "Observações teste", 100.0)
    return ps

@pytest.fixture
def item_demanda_produto_exemplo():
    # Cria um item demanda produto de exemplo para os testes
    from model.item_demanda_produto_model import ItemDemandaProduto
    item = ItemDemandaProduto(1, 1, 2, "Observações do item")
    return item

@pytest.fixture
def item_demanda_servico_exemplo():
    # Cria um item demanda serviço de exemplo para os testes
    from model.item_demanda_servico_model import ItemDemandaServico
    item = ItemDemandaServico(1, 1, 1, "Observações do serviço")
    return item

@pytest.fixture
def orcamento_exemplo():
    # Cria um orçamento de exemplo para os testes
    from model.orcamento_model import Orcamento
    orcamento = Orcamento(
        id=0,
        id_demanda=1,
        id_fornecedor_prestador=1,
        data_hora_cadastro=datetime.now(),
        data_hora_validade=None,
        status="PENDENTE",
        observacoes="Orçamento de teste",
        valor_total=1000.00
    )
    return orcamento

@pytest.fixture
def lista_orcamentos_exemplo():
    # Cria uma lista de 10 orçamentos de exemplo para os testes
    from model.orcamento_model import Orcamento
    orcamentos = []
    for i in range(1, 11):
        orcamento = Orcamento(
            id=0,
            id_demanda=1,
            id_fornecedor_prestador=i,
            data_hora_cadastro=datetime.now(),
            data_hora_validade=None,
            status="PENDENTE",
            observacoes=f"Orçamento {i:02d}",
            valor_total=1000.00 * i
        )
        orcamentos.append(orcamento)
    return orcamentos

@pytest.fixture
def item_orcamento_produto_exemplo():
    # Cria um item orçamento produto de exemplo para os testes
    from model.item_orcamento_produto_model import ItemOrcamentoProduto
    item = ItemOrcamentoProduto(
        id_orcamento=1,
        id_produto=1,
        preco_unitario=50.00,
        quantidade=2,
        observacoes="Item de produto de teste"
    )
    return item

@pytest.fixture
def item_orcamento_servico_exemplo():
    # Cria um item orçamento serviço de exemplo para os testes
    from model.item_orcamento_servico_model import ItemOrcamentoServico
    item = ItemOrcamentoServico(
        id_orcamento=1,
        id_servico=1,
        preco_unitario=200.00,
        quantidade=1,
        observacoes="Item de serviço de teste"
    )
    return item

```

# tests/test_casal_repo.py

```py
from model.casal_model import Casal
from repo import casal_repo, usuario_repo

class TestCasalRepo:
    def test_criar_tabela_casal(self, test_db):
        assert casal_repo.criar_tabela_casal() is True

    def test_inserir_casal(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(0, 1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        # Act
        id_casal = casal_repo.inserir_casal(novo_casal)        
        # Assert
        assert id_casal is not None, "ID do casal inserido não pode ser None"
        casal = casal_repo.obter_casal_por_id(id_casal)
        assert casal is not None, "Casal não encontrado após inserção"
        assert casal.id_noivo1 == 1
        assert casal.id_noivo2 == 2
        assert casal.orcamento == 10000.0

    def test_obter_casal_por_id_inexistente(self, test_db):
        # Arrange        
        casal_repo.criar_tabela_casal()
        # Act        
        casal = casal_repo.obter_casal_por_id(999)
        # Assert
        assert casal is None, "Não deveria encontrar casal com ID inexistente"

    def test_atualizar_casal_existente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(0, 1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        id_casal = casal_repo.inserir_casal(novo_casal)
        # Act
        casal_atualizado = Casal(id_casal, 1, 2, 15000.0)
        sucesso = casal_repo.atualizar_casal(casal_atualizado)
        # Assert
        assert sucesso is True, "Atualização do casal deveria ser bem-sucedida"
        casal = casal_repo.obter_casal_por_id(id_casal)
        assert casal is not None, "Casal não encontrado após atualização"
        assert casal.orcamento == 15000.0, "Orçamento do casal não foi atualizado corretamente"

    def test_atualizar_casal_inexistente(self, test_db):
        # Arrange
        casal_repo.criar_tabela_casal()
        # Act
        casal_inexistente = Casal(999, 1, 2, 10000.0)        
        atualizou = casal_repo.atualizar_casal(casal_inexistente)
        # Assert
        assert atualizou is False, "Atualização de casal inexistente deveria falhar"

    def test_excluir_casal_existente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(0, 1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        id_casal = casal_repo.inserir_casal(novo_casal)
        # Act
        sucesso = casal_repo.excluir_casal(id_casal)
        # Assert
        assert sucesso is True, "Exclusão do casal deveria ser bem-sucedida"
        casal_excluido = casal_repo.obter_casal_por_id(id_casal)
        assert casal_excluido is None, "Casal não foi excluído corretamente"

    def test_excluir_casal_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        assert casal_repo.excluir_casal(999) is False

    def test_obter_casais_por_pagina(self, test_db, lista_usuarios_exemplo, lista_casais_exemplo):
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir_usuario(usuario)
        casal_repo.criar_tabela_casal()
        for casal in lista_casais_exemplo:
            casal_repo.inserir_casal(casal)
        pagina = casal_repo.obter_casais_por_pagina(1, 4)
        assert len(pagina) == 4
        assert all(isinstance(c, Casal) for c in pagina)

    def test_obter_casal_por_noivo(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        casal_repo.criar_tabela_casal()
        casal1 = Casal(0, 1, 2, 10000.0)
        casal2 = Casal(0, 3, 4, 15000.0)
        casal_repo.inserir_casal(casal1)
        casal_repo.inserir_casal(casal2)
        # Act
        casal_encontrado = casal_repo.obter_casal_por_noivo(1)
        # Assert
        assert casal_encontrado is not None
        assert casal_encontrado.id_noivo1 == 1 or casal_encontrado.id_noivo2 == 1
```

# tests/test_chat_repo.py

```py
from datetime import datetime
from model.chat_model import Chat
from repo import chat_repo, usuario_repo

class TestChatRepo:
    def test_criar_tabela_chat(self, test_db):
        assert chat_repo.criar_tabela_chat() is True

    def test_inserir_chat(self, test_db, chat_exemplo, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:2]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        # Act
        sucesso = chat_repo.inserir_chat(chat_exemplo)
        # Assert
        assert sucesso is True

    def test_obter_mensagens_por_usuario(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:3]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        
        # Inserir algumas mensagens
        chat1 = Chat(1, 2, datetime.now(), "Olá!", None)
        chat2 = Chat(2, 1, datetime.now(), "Oi!", None)
        chat3 = Chat(1, 3, datetime.now(), "Tudo bem?", None)
        
        chat_repo.inserir_chat(chat1)
        chat_repo.inserir_chat(chat2)
        chat_repo.inserir_chat(chat3)
        
        # Act
        mensagens = chat_repo.obter_mensagens_por_usuario(1, 1, 10)
        
        # Assert
        assert len(mensagens) == 3
        assert all(isinstance(m, Chat) for m in mensagens)

    def test_atualizar_data_leitura(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:2]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        
        data_envio = datetime.now()
        chat = Chat(1, 2, data_envio, "Mensagem teste", None)
        chat_repo.inserir_chat(chat)
        
        # Act
        data_leitura = datetime.now()
        sucesso = chat_repo.atualizar_data_leitura(1, 2, data_envio, data_leitura)
        
        # Assert
        assert sucesso is True

    def test_obter_mensagens_paginacao(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:3]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        
        # Inserir 10 mensagens
        for i in range(10):
            chat = Chat(1, 2, datetime.now(), f"Mensagem {i}", None)
            chat_repo.inserir_chat(chat)
        
        # Act
        pagina1 = chat_repo.obter_mensagens_por_usuario(1, 1, 5)
        pagina2 = chat_repo.obter_mensagens_por_usuario(1, 2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 5
```

# tests/test_demanda_repo.py

```py
from datetime import datetime
from model.demanda_model import Demanda
from model.casal_model import Casal
from repo import demanda_repo, casal_repo, usuario_repo

class TestDemandaRepo:
    def test_criar_tabela_demandas(self, test_db):
        # Arrange
        # Act
        resultado = demanda_repo.criar_tabela_demandas()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_demanda(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        # Inserir usuários e casal
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Act
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Assert
        demanda_db = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        assert demanda_db is not None, "A demanda inserida não deveria ser None"
        assert demanda_db.id == id_demanda_inserida, "A demanda inserida deveria ter um ID igual ao retornado pela inserção"
        assert demanda_db.id_casal == 1, "O id_casal da demanda inserida não confere"
        assert demanda_db.data_hora_cadastro is not None, "A data_hora_cadastro não deveria ser None"

    def test_obter_demanda_por_id_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Act
        demanda_db = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        
        # Assert
        assert demanda_db is not None, "A demanda retornada deveria ser diferente de None"
        assert demanda_db.id == id_demanda_inserida, "O id da demanda buscada deveria ser igual ao id da demanda inserida"
        assert demanda_db.id_casal == demanda_exemplo.id_casal, "O id_casal da demanda buscada deveria ser igual ao id_casal da demanda inserida"

    def test_obter_demanda_por_id_inexistente(self, test_db):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        # Act
        demanda_db = demanda_repo.obter_demanda_por_id(999)
        # Assert
        assert demanda_db is None, "A demanda buscada com ID inexistente deveria retornar None"

    def test_atualizar_demanda_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Act
        demanda_db = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        # Apenas verificar se a atualização funciona, sem comparar datas
        resultado = demanda_repo.atualizar_demanda(demanda_db)
        
        # Assert
        assert resultado == True, "A atualização da demanda deveria retornar True"

    def test_atualizar_demanda_inexistente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        # Criar usuários e casal necessários para satisfazer foreign key
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(999, 1, datetime.now())
        # Act
        resultado = demanda_repo.atualizar_demanda(demanda)
        # Assert
        assert resultado == False, "A atualização de uma demanda inexistente deveria retornar False"

    def test_excluir_demanda_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Act
        resultado = demanda_repo.excluir_demanda(id_demanda_inserida)
        
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        demanda_excluida = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        assert demanda_excluida is None, "A demanda excluída deveria ser None"

    def test_excluir_demanda_inexistente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        # Criar usuários e casal necessários para satisfazer foreign key
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Act
        resultado = demanda_repo.excluir_demanda(999)
        # Assert
        assert resultado == False, "A exclusão de uma demanda inexistente deveria retornar False"

    def test_obter_demandas_por_pagina(self, test_db, lista_demandas_exemplo, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        # Inserir usuários e casais
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir_usuario(usuario)
        
        from model.casal_model import Casal
        for i in range(1, 11, 2):
            casal = Casal(0, i, i+1, 10000.0)
            casal_repo.inserir_casal(casal)
        
        # Inserir demandas
        for demanda in lista_demandas_exemplo[:5]:
            demanda_repo.inserir_demanda(demanda)
        
        # Act
        pagina_demandas = demanda_repo.obter_demandas_por_pagina(1, 3)
        
        # Assert
        assert len(pagina_demandas) == 3, "Deveria retornar 3 demandas na primeira página"
        assert all(isinstance(d, Demanda) for d in pagina_demandas), "Todos os itens da página devem ser do tipo Demanda"

    def test_obter_demandas_por_casal(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        # Inserir usuários e casal
        for noivo in lista_noivos_exemplo[:4]:
            usuario_repo.inserir_usuario(noivo)
        
        from model.casal_model import Casal
        casal1 = Casal(0, 1, 2, 10000.0)
        casal2 = Casal(0, 3, 4, 15000.0)
        id_casal1 = casal_repo.inserir_casal(casal1)
        id_casal2 = casal_repo.inserir_casal(casal2)
        
        # Inserir demandas para casal1
        demanda1 = Demanda(0, id_casal1, datetime.now())
        demanda2 = Demanda(0, id_casal1, datetime.now())
        demanda3 = Demanda(0, id_casal2, datetime.now())
        
        demanda_repo.inserir_demanda(demanda1)
        demanda_repo.inserir_demanda(demanda2)
        demanda_repo.inserir_demanda(demanda3)
        
        # Act
        demandas_casal1 = demanda_repo.obter_demandas_por_casal(id_casal1)
        
        # Assert
        assert len(demandas_casal1) == 2, "Deveria retornar 2 demandas para o casal1"
        assert all(d.id_casal == id_casal1 for d in demandas_casal1), "Todas as demandas devem pertencer ao casal1"
```

# tests/test_fornecedor_produto_repo.py

```py
from model.fornecedor_model import Fornecedor
from repo import fornecedor_produto_repo, usuario_repo, produto_repo

class TestFornecedorProdutoRepo:
    def test_criar_tabela_fornecedor_produto(self, test_db):
        assert fornecedor_produto_repo.criar_tabela_fornecedor_produto() is True

    def test_inserir_fornecedor_produto(self, test_db, fornecedor_produto_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        
        # Act
        ids = fornecedor_produto_repo.inserir_fornecedor_produto(fornecedor_produto_exemplo)
        
        # Assert
        assert ids == (1, 1)

    def test_atualizar_fornecedor_produto(self, test_db, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        
        fp = Fornecedor(1, 1, "Observações iniciais", 50.0)
        fornecedor_produto_repo.inserir_fornecedor_produto(fp)
        
        # Act
        fp_atualizado = Fornecedor(1, 1, "Observações atualizadas", 75.0)
        sucesso = fornecedor_produto_repo.atualizar_fornecedor_produto(fp_atualizado)
        
        # Assert
        assert sucesso is True
        fp_obtido = fornecedor_produto_repo.obter_fornecedor_produto_por_id(1, 1)
        assert fp_obtido.observacoes == "Observações atualizadas"
        assert fp_obtido.preco == 75.0

    def test_excluir_fornecedor_produto(self, test_db, fornecedor_produto_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        fornecedor_produto_repo.inserir_fornecedor_produto(fornecedor_produto_exemplo)
        
        # Act
        sucesso = fornecedor_produto_repo.excluir_fornecedor_produto(1, 1)
        
        # Assert
        assert sucesso is True
        assert fornecedor_produto_repo.obter_fornecedor_produto_por_id(1, 1) is None

    def test_obter_fornecedor_produto_por_id(self, test_db, fornecedor_produto_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        fornecedor_produto_repo.inserir_fornecedor_produto(fornecedor_produto_exemplo)
        
        # Act
        fp = fornecedor_produto_repo.obter_fornecedor_produto_por_id(1, 1)
        
        # Assert
        assert fp is not None
        assert fp.id_fornecedor == 1
        assert fp.id_produto == 1
        assert fp.observacoes == "Observações teste"
        assert fp.preco == 50.0

    def test_obter_fornecedores_produto_por_pagina(self, test_db, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        for produto in lista_produtos_exemplo[:5]:
            produto_repo.inserir_produto(produto)
        
        # Inserir relações
        for i in range(1, 6):
            fp = Fornecedor(1, i, f"Observações {i}", 50.0 * i)
            fornecedor_produto_repo.inserir_fornecedor_produto(fp)
        
        # Act
        pagina = fornecedor_produto_repo.obter_fornecedores_produto_por_pagina(1, 3)
        
        # Assert
        assert len(pagina) == 3
        assert all(isinstance(fp, Fornecedor) for fp in pagina)
```

# tests/test_item_demanda_produto_repo.py

```py
from datetime import datetime
from model.item_demanda_produto_model import ItemDemandaProduto
from model.demanda_model import Demanda
from model.casal_model import Casal
from repo import item_demanda_produto_repo, demanda_repo, produto_repo, casal_repo, usuario_repo

class TestItemDemandaProdutoRepo:
    def test_criar_tabela_item_demanda_produto(self, test_db):
        assert item_demanda_produto_repo.criar_tabela_item_demanda_produto() is True

    def test_inserir_item_demanda_produto(self, test_db, item_demanda_produto_exemplo, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        # Act
        sucesso = item_demanda_produto_repo.inserir_item_demanda_produto(item_demanda_produto_exemplo)
        
        # Assert
        assert sucesso is True

    def test_obter_item_demanda_produto_por_id(self, test_db, item_demanda_produto_exemplo, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        item_demanda_produto_repo.inserir_item_demanda_produto(item_demanda_produto_exemplo)
        
        # Act
        item = item_demanda_produto_repo.obter_item_demanda_produto_por_id(1, 1)
        
        # Assert
        assert item is not None
        assert item.id_demanda == 1
        assert item.id_produto == 1
        assert item.quantidade == 2
        assert item.observacoes == "Observações do item"

    def test_atualizar_item_demanda_produto(self, test_db, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        item = ItemDemandaProduto(1, 1, 2, "Observações iniciais")
        item_demanda_produto_repo.inserir_item_demanda_produto(item)
        
        # Act
        item_atualizado = ItemDemandaProduto(1, 1, 5, "Observações atualizadas")
        sucesso = item_demanda_produto_repo.atualizar_item_demanda_produto(item_atualizado)
        
        # Assert
        assert sucesso is True
        item_obtido = item_demanda_produto_repo.obter_item_demanda_produto_por_id(1, 1)
        assert item_obtido.quantidade == 5
        assert item_obtido.observacoes == "Observações atualizadas"

    def test_excluir_item_demanda_produto(self, test_db, item_demanda_produto_exemplo, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        item_demanda_produto_repo.inserir_item_demanda_produto(item_demanda_produto_exemplo)
        
        # Act
        sucesso = item_demanda_produto_repo.excluir_item_demanda_produto(1, 1)
        
        # Assert
        assert sucesso is True
        assert item_demanda_produto_repo.obter_item_demanda_produto_por_id(1, 1) is None

    def test_obter_itens_por_demanda(self, test_db, lista_noivos_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        for produto in lista_produtos_exemplo[:3]:
            produto_repo.inserir_produto(produto)
        
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        # Inserir itens
        for i in range(1, 4):
            item = ItemDemandaProduto(1, i, i * 2, f"Observações {i}")
            item_demanda_produto_repo.inserir_item_demanda_produto(item)
        
        # Act
        itens = item_demanda_produto_repo.obter_itens_por_demanda(1)
        
        # Assert
        assert len(itens) == 3
        assert all(isinstance(item, ItemDemandaProduto) for item in itens)
        assert all(item.id_demanda == 1 for item in itens)

    def test_obter_itens_demanda_produto_por_pagina(self, test_db, lista_noivos_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        # Inserir usuários e casais
        for usuario in lista_noivos_exemplo[:4]:
            usuario_repo.inserir_usuario(usuario)
        casal1 = Casal(0, 1, 2, 10000.0)
        casal2 = Casal(0, 3, 4, 15000.0)
        casal_repo.inserir_casal(casal1)
        casal_repo.inserir_casal(casal2)
        
        # Inserir produtos
        for produto in lista_produtos_exemplo[:5]:
            produto_repo.inserir_produto(produto)
        
        # Inserir demandas
        demanda1 = Demanda(0, 1, datetime.now())
        demanda2 = Demanda(0, 2, datetime.now())
        demanda_repo.inserir_demanda(demanda1)
        demanda_repo.inserir_demanda(demanda2)
        
        # Inserir itens
        for d in range(1, 3):
            for p in range(1, 4):
                item = ItemDemandaProduto(d, p, p, f"Obs {d}-{p}")
                item_demanda_produto_repo.inserir_item_demanda_produto(item)
        
        # Act
        pagina = item_demanda_produto_repo.obter_itens_demanda_produto_por_pagina(1, 4)
        
        # Assert
        assert len(pagina) == 4
        assert all(isinstance(item, ItemDemandaProduto) for item in pagina)
```

# tests/test_item_demanda_servico_repo.py

```py
from datetime import datetime
from model.item_demanda_servico_model import ItemDemandaServico
from model.demanda_model import Demanda
from model.casal_model import Casal
from repo import item_demanda_servico_repo, demanda_repo, servico_repo, casal_repo, usuario_repo

class TestItemDemandaServicoRepo:
    def test_criar_tabela_item_demanda_servico(self, test_db):
        assert item_demanda_servico_repo.criar_tabela_item_demanda_servico() is True

    def test_inserir_item_demanda_servico(self, test_db, item_demanda_servico_exemplo, lista_noivos_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        servico_repo.criar_tabela_servicos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_servico_repo.criar_tabela_item_demanda_servico()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        servico_repo.inserir_servico(servico_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        # Act
        sucesso = item_demanda_servico_repo.inserir_item_demanda_servico(item_demanda_servico_exemplo)
        
        # Assert
        assert sucesso is True

    def test_obter_item_demanda_servico_por_id(self, test_db, item_demanda_servico_exemplo, lista_noivos_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        servico_repo.criar_tabela_servicos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_servico_repo.criar_tabela_item_demanda_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        servico_repo.inserir_servico(servico_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        item_demanda_servico_repo.inserir_item_demanda_servico(item_demanda_servico_exemplo)
        
        # Act
        item = item_demanda_servico_repo.obter_item_demanda_servico_por_id(1, 1)
        
        # Assert
        assert item is not None
        assert item.id_demanda == 1
        assert item.id_servico == 1
        assert item.quantidade == 1
        assert item.observacoes == "Observações do serviço"

    def test_atualizar_item_demanda_servico(self, test_db, lista_noivos_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        servico_repo.criar_tabela_servicos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_servico_repo.criar_tabela_item_demanda_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        servico_repo.inserir_servico(servico_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        item = ItemDemandaServico(1, 1, 1, "Observações iniciais")
        item_demanda_servico_repo.inserir_item_demanda_servico(item)
        
        # Act
        item_atualizado = ItemDemandaServico(1, 1, 3, "Observações atualizadas")
        sucesso = item_demanda_servico_repo.atualizar_item_demanda_servico(item_atualizado)
        
        # Assert
        assert sucesso is True
        item_obtido = item_demanda_servico_repo.obter_item_demanda_servico_por_id(1, 1)
        assert item_obtido.quantidade == 3
        assert item_obtido.observacoes == "Observações atualizadas"

    def test_excluir_item_demanda_servico(self, test_db, item_demanda_servico_exemplo, lista_noivos_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        servico_repo.criar_tabela_servicos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_servico_repo.criar_tabela_item_demanda_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        servico_repo.inserir_servico(servico_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        item_demanda_servico_repo.inserir_item_demanda_servico(item_demanda_servico_exemplo)
        
        # Act
        sucesso = item_demanda_servico_repo.excluir_item_demanda_servico(1, 1)
        
        # Assert
        assert sucesso is True
        assert item_demanda_servico_repo.obter_item_demanda_servico_por_id(1, 1) is None

    def test_obter_itens_por_demanda(self, test_db, lista_noivos_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        servico_repo.criar_tabela_servicos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_servico_repo.criar_tabela_item_demanda_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        for servico in lista_servicos_exemplo[:3]:
            servico_repo.inserir_servico(servico)
        
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        # Inserir itens
        for i in range(1, 4):
            item = ItemDemandaServico(1, i, 1, f"Observações {i}")
            item_demanda_servico_repo.inserir_item_demanda_servico(item)
        
        # Act
        itens = item_demanda_servico_repo.obter_itens_por_demanda(1)
        
        # Assert
        assert len(itens) == 3
        assert all(isinstance(item, ItemDemandaServico) for item in itens)
        assert all(item.id_demanda == 1 for item in itens)

    def test_obter_itens_demanda_servico_por_pagina(self, test_db, lista_noivos_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        servico_repo.criar_tabela_servicos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_servico_repo.criar_tabela_item_demanda_servico()
        
        # Inserir usuários e casais
        for usuario in lista_noivos_exemplo[:4]:
            usuario_repo.inserir_usuario(usuario)
        casal1 = Casal(0, 1, 2, 10000.0)
        casal2 = Casal(0, 3, 4, 15000.0)
        casal_repo.inserir_casal(casal1)
        casal_repo.inserir_casal(casal2)
        
        # Inserir serviços
        for servico in lista_servicos_exemplo[:5]:
            servico_repo.inserir_servico(servico)
        
        # Inserir demandas
        demanda1 = Demanda(0, 1, datetime.now())
        demanda2 = Demanda(0, 2, datetime.now())
        demanda_repo.inserir_demanda(demanda1)
        demanda_repo.inserir_demanda(demanda2)
        
        # Inserir itens
        for d in range(1, 3):
            for s in range(1, 4):
                item = ItemDemandaServico(d, s, 1, f"Obs {d}-{s}")
                item_demanda_servico_repo.inserir_item_demanda_servico(item)
        
        # Act
        pagina = item_demanda_servico_repo.obter_itens_demanda_servico_por_pagina(1, 4)
        
        # Assert
        assert len(pagina) == 4
        assert all(isinstance(item, ItemDemandaServico) for item in pagina)
```

# tests/test_item_orcamento_produto_repo.py

```py
from datetime import datetime
from model.orcamento_model import Orcamento
from model.demanda_model import Demanda
from model.casal_model import Casal
from model.item_orcamento_produto_model import ItemOrcamentoProduto
from repo import item_orcamento_produto_repo, orcamento_repo, demanda_repo, casal_repo, usuario_repo, produto_repo

class TestItemOrcamentoProdutoRepo:
    def test_criar_tabela_item_orcamento_produto(self, test_db):
        # Criar tabelas dependentes primeiro
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        # Agora criar tabela item_orcamento_produto
        assert item_orcamento_produto_repo.criar_tabela_item_orcamento_produto() is True

    def test_inserir_item_orcamento_produto(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_produto = produto_repo.inserir_produto(produto_exemplo)
        
        # Criar item
        item = ItemOrcamentoProduto(
            id_orcamento=id_orcamento,
            id_produto=id_produto,
            preco_unitario=25.50,
            quantidade=3,
            observacoes="Item de teste"
        )
        
        # Act
        sucesso = item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Assert
        assert sucesso is True
        item_salvo = item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(id_orcamento, id_produto)
        assert item_salvo is not None
        assert item_salvo.preco_unitario == 25.50
        assert item_salvo.quantidade == 3
        assert item_salvo.observacoes == "Item de teste"

    def test_atualizar_item_orcamento_produto(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_produto = produto_repo.inserir_produto(produto_exemplo)
        
        item = ItemOrcamentoProduto(id_orcamento, id_produto, 25.50, 3, "Item inicial")
        item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        item.preco_unitario = 30.00
        item.quantidade = 5
        item.observacoes = "Item atualizado"
        sucesso = item_orcamento_produto_repo.atualizar_item_orcamento_produto(item)
        
        # Assert
        assert sucesso is True
        item_verificado = item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(id_orcamento, id_produto)
        assert item_verificado.preco_unitario == 30.00
        assert item_verificado.quantidade == 5
        assert item_verificado.observacoes == "Item atualizado"

    def test_excluir_item_orcamento_produto(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_produto = produto_repo.inserir_produto(produto_exemplo)
        
        item = ItemOrcamentoProduto(id_orcamento, id_produto, 25.50, 3, None)
        item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        sucesso = item_orcamento_produto_repo.excluir_item_orcamento_produto(id_orcamento, id_produto)
        
        # Assert
        assert sucesso is True
        assert item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(id_orcamento, id_produto) is None

    def test_obter_item_orcamento_produto_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        # Act
        item = item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(999, 999)
        
        # Assert
        assert item is None

    def test_obter_itens_por_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir produtos e itens
        for i, produto in enumerate(lista_produtos_exemplo[:3]):
            id_produto = produto_repo.inserir_produto(produto)
            item = ItemOrcamentoProduto(id_orcamento, id_produto, 10.0 * (i+1), i+1, f"Item {i+1}")
            item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        itens = item_orcamento_produto_repo.obter_itens_por_orcamento(id_orcamento)
        
        # Assert
        assert len(itens) == 3
        assert all(item.id_orcamento == id_orcamento for item in itens)
        assert itens[0].preco_unitario == 10.0
        assert itens[1].preco_unitario == 20.0
        assert itens[2].preco_unitario == 30.0

    def test_obter_itens_orcamento_produto_por_pagina(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Criar múltiplos orçamentos e itens
        ids_orcamentos = []
        for i in range(3):
            demanda = Demanda(0, 1, datetime.now())
            id_demanda = demanda_repo.inserir_demanda(demanda)
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
            ids_orcamentos.append(orcamento_repo.inserir_orcamento(orcamento))
        
        # Inserir produtos e itens
        for produto in lista_produtos_exemplo[:3]:
            id_produto = produto_repo.inserir_produto(produto)
            for id_orcamento in ids_orcamentos:
                item = ItemOrcamentoProduto(id_orcamento, id_produto, 10.0, 1, None)
                item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act - Total de 9 itens (3 orçamentos x 3 produtos)
        pagina1 = item_orcamento_produto_repo.obter_itens_orcamento_produto_por_pagina(1, 5)
        pagina2 = item_orcamento_produto_repo.obter_itens_orcamento_produto_por_pagina(2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 4
        assert all(isinstance(item, ItemOrcamentoProduto) for item in pagina1)
        assert all(isinstance(item, ItemOrcamentoProduto) for item in pagina2)

    def test_calcular_total_itens_produto_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir produtos e itens com valores conhecidos
        produtos_precos = [(10.0, 2), (25.0, 3), (100.0, 1)]  # (preco_unitario, quantidade)
        for i, (produto, (preco, qtd)) in enumerate(zip(lista_produtos_exemplo[:3], produtos_precos)):
            id_produto = produto_repo.inserir_produto(produto)
            item = ItemOrcamentoProduto(id_orcamento, id_produto, preco, qtd, None)
            item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        total = item_orcamento_produto_repo.calcular_total_itens_produto_orcamento(id_orcamento)
        
        # Assert
        # Total = (10*2) + (25*3) + (100*1) = 20 + 75 + 100 = 195
        assert total == 195.0

    def test_calcular_total_itens_produto_orcamento_vazio(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act - Orçamento sem itens
        total = item_orcamento_produto_repo.calcular_total_itens_produto_orcamento(id_orcamento)
        
        # Assert
        assert total == 0.0
```

# tests/test_item_orcamento_servico_repo.py

```py
from datetime import datetime
from model.orcamento_model import Orcamento
from model.demanda_model import Demanda
from model.casal_model import Casal
from model.item_orcamento_servico_model import ItemOrcamentoServico
from repo import item_orcamento_servico_repo, orcamento_repo, demanda_repo, casal_repo, usuario_repo, servico_repo

class TestItemOrcamentoServicoRepo:
    def test_criar_tabela_item_orcamento_servico(self, test_db):
        # Criar tabelas dependentes primeiro
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        # Agora criar tabela item_orcamento_servico
        assert item_orcamento_servico_repo.criar_tabela_item_orcamento_servico() is True

    def test_inserir_item_orcamento_servico(self, test_db, lista_noivos_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_servico = servico_repo.inserir_servico(servico_exemplo)
        
        # Criar item
        item = ItemOrcamentoServico(
            id_orcamento=id_orcamento,
            id_servico=id_servico,
            preco_unitario=150.00,
            quantidade=2,
            observacoes="Serviço de teste"
        )
        
        # Act
        sucesso = item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Assert
        assert sucesso is True
        item_salvo = item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(id_orcamento, id_servico)
        assert item_salvo is not None
        assert item_salvo.preco_unitario == 150.00
        assert item_salvo.quantidade == 2
        assert item_salvo.observacoes == "Serviço de teste"

    def test_atualizar_item_orcamento_servico(self, test_db, lista_noivos_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_servico = servico_repo.inserir_servico(servico_exemplo)
        
        item = ItemOrcamentoServico(id_orcamento, id_servico, 150.00, 2, "Serviço inicial")
        item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        item.preco_unitario = 200.00
        item.quantidade = 3
        item.observacoes = "Serviço atualizado"
        sucesso = item_orcamento_servico_repo.atualizar_item_orcamento_servico(item)
        
        # Assert
        assert sucesso is True
        item_verificado = item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(id_orcamento, id_servico)
        assert item_verificado.preco_unitario == 200.00
        assert item_verificado.quantidade == 3
        assert item_verificado.observacoes == "Serviço atualizado"

    def test_excluir_item_orcamento_servico(self, test_db, lista_noivos_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_servico = servico_repo.inserir_servico(servico_exemplo)
        
        item = ItemOrcamentoServico(id_orcamento, id_servico, 150.00, 2, None)
        item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        sucesso = item_orcamento_servico_repo.excluir_item_orcamento_servico(id_orcamento, id_servico)
        
        # Assert
        assert sucesso is True
        assert item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(id_orcamento, id_servico) is None

    def test_obter_item_orcamento_servico_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        # Act
        item = item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(999, 999)
        
        # Assert
        assert item is None

    def test_obter_itens_por_orcamento(self, test_db, lista_noivos_exemplo, prestador_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir serviços e itens
        for i, servico in enumerate(lista_servicos_exemplo[:3]):
            id_servico = servico_repo.inserir_servico(servico)
            item = ItemOrcamentoServico(id_orcamento, id_servico, 100.0 * (i+1), i+1, f"Serviço {i+1}")
            item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        itens = item_orcamento_servico_repo.obter_itens_por_orcamento(id_orcamento)
        
        # Assert
        assert len(itens) == 3
        assert all(item.id_orcamento == id_orcamento for item in itens)
        assert itens[0].preco_unitario == 100.0
        assert itens[1].preco_unitario == 200.0
        assert itens[2].preco_unitario == 300.0

    def test_obter_itens_orcamento_servico_por_pagina(self, test_db, lista_noivos_exemplo, prestador_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Criar múltiplos orçamentos e itens
        ids_orcamentos = []
        for i in range(3):
            demanda = Demanda(0, 1, datetime.now())
            id_demanda = demanda_repo.inserir_demanda(demanda)
            orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
            ids_orcamentos.append(orcamento_repo.inserir_orcamento(orcamento))
        
        # Inserir serviços e itens
        for servico in lista_servicos_exemplo[:3]:
            id_servico = servico_repo.inserir_servico(servico)
            for id_orcamento in ids_orcamentos:
                item = ItemOrcamentoServico(id_orcamento, id_servico, 100.0, 1, None)
                item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act - Total de 9 itens (3 orçamentos x 3 serviços)
        pagina1 = item_orcamento_servico_repo.obter_itens_orcamento_servico_por_pagina(1, 5)
        pagina2 = item_orcamento_servico_repo.obter_itens_orcamento_servico_por_pagina(2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 4
        assert all(isinstance(item, ItemOrcamentoServico) for item in pagina1)
        assert all(isinstance(item, ItemOrcamentoServico) for item in pagina2)

    def test_calcular_total_itens_servico_orcamento(self, test_db, lista_noivos_exemplo, prestador_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir serviços e itens com valores conhecidos
        servicos_precos = [(100.0, 2), (250.0, 1), (500.0, 1)]  # (preco_unitario, quantidade)
        for i, (servico, (preco, qtd)) in enumerate(zip(lista_servicos_exemplo[:3], servicos_precos)):
            id_servico = servico_repo.inserir_servico(servico)
            item = ItemOrcamentoServico(id_orcamento, id_servico, preco, qtd, None)
            item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        total = item_orcamento_servico_repo.calcular_total_itens_servico_orcamento(id_orcamento)
        
        # Assert
        # Total = (100*2) + (250*1) + (500*1) = 200 + 250 + 500 = 950
        assert total == 950.0

    def test_calcular_total_itens_servico_orcamento_vazio(self, test_db, lista_noivos_exemplo, prestador_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act - Orçamento sem itens
        total = item_orcamento_servico_repo.calcular_total_itens_servico_orcamento(id_orcamento)
        
        # Assert
        assert total == 0.0
```

# tests/test_orcamento_repo.py

```py
from datetime import datetime, timedelta
from model.orcamento_model import Orcamento
from model.demanda_model import Demanda
from model.casal_model import Casal
from repo import orcamento_repo, demanda_repo, casal_repo, usuario_repo

class TestOrcamentoRepo:
    def test_criar_tabela_orcamento(self, test_db):
        # Criar tabelas dependentes primeiro
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        # Agora criar tabela orcamento
        assert orcamento_repo.criar_tabela_orcamento() is True

    def test_inserir_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Criar orçamento
        orcamento = Orcamento(
            id=0,
            id_demanda=id_demanda,
            id_fornecedor_prestador=id_fornecedor,
            data_hora_cadastro=datetime.now(),
            data_hora_validade=datetime.now() + timedelta(days=30),
            status="PENDENTE",
            observacoes="Orçamento de teste",
            valor_total=1500.00
        )
        
        # Act
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Assert
        assert id_orcamento is not None
        orcamento_salvo = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_salvo is not None
        assert orcamento_salvo.id_demanda == id_demanda
        assert orcamento_salvo.id_fornecedor_prestador == id_fornecedor
        assert orcamento_salvo.status == "PENDENTE"
        assert orcamento_salvo.valor_total == 1500.00

    def test_atualizar_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), 
                            datetime.now() + timedelta(days=30), "PENDENTE", 
                            "Orçamento inicial", 1500.00)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamento_atualizado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        orcamento_atualizado.status = "ACEITO"
        orcamento_atualizado.valor_total = 2000.00
        orcamento_atualizado.observacoes = "Orçamento atualizado"
        sucesso = orcamento_repo.atualizar_orcamento(orcamento_atualizado)
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_verificado.status == "ACEITO"
        assert orcamento_verificado.valor_total == 2000.00
        assert orcamento_verificado.observacoes == "Orçamento atualizado"

    def test_atualizar_status_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        sucesso = orcamento_repo.atualizar_status_orcamento(id_orcamento, "ACEITO")
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_verificado.status == "ACEITO"

    def test_atualizar_valor_total_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 100.00)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        sucesso = orcamento_repo.atualizar_valor_total_orcamento(id_orcamento, 250.00)
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_verificado.valor_total == 250.00

    def test_aceitar_orcamento_e_rejeitar_outros(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir múltiplos orçamentos
        ids_orcamentos = []
        for i, id_fornecedor in enumerate(ids_fornecedores):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            ids_orcamentos.append(orcamento_repo.inserir_orcamento(orcamento))
        
        # Act - Aceitar o segundo orçamento
        sucesso = orcamento_repo.aceitar_orcamento_e_rejeitar_outros(ids_orcamentos[1], id_demanda)
        
        # Assert
        assert sucesso is True
        # Verificar que o segundo foi aceito
        orcamento_aceito = orcamento_repo.obter_orcamento_por_id(ids_orcamentos[1])
        assert orcamento_aceito.status == "ACEITO"
        
        # Verificar que os outros foram rejeitados
        orcamento_rejeitado1 = orcamento_repo.obter_orcamento_por_id(ids_orcamentos[0])
        assert orcamento_rejeitado1.status == "REJEITADO"
        
        orcamento_rejeitado2 = orcamento_repo.obter_orcamento_por_id(ids_orcamentos[2])
        assert orcamento_rejeitado2.status == "REJEITADO"

    def test_excluir_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        sucesso = orcamento_repo.excluir_orcamento(id_orcamento)
        
        # Assert
        assert sucesso is True
        assert orcamento_repo.obter_orcamento_por_id(id_orcamento) is None

    def test_obter_orcamento_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        # Act
        orcamento = orcamento_repo.obter_orcamento_por_id(999)
        
        # Assert
        assert orcamento is None

    def test_obter_orcamentos_por_demanda(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir orçamentos
        for i, id_fornecedor in enumerate(ids_fornecedores):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamentos = orcamento_repo.obter_orcamentos_por_demanda(id_demanda)
        
        # Assert
        assert len(orcamentos) == 3
        assert all(o.id_demanda == id_demanda for o in orcamentos)

    def test_obter_orcamentos_por_fornecedor_prestador(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Criar múltiplas demandas
        ids_demandas = []
        for i in range(3):
            demanda = Demanda(0, 1, datetime.now())
            ids_demandas.append(demanda_repo.inserir_demanda(demanda))
        
        # Inserir orçamentos do mesmo fornecedor
        for id_demanda in ids_demandas:
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", None, 100.00)
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamentos = orcamento_repo.obter_orcamentos_por_fornecedor_prestador(id_fornecedor)
        
        # Assert
        assert len(orcamentos) == 3
        assert all(o.id_fornecedor_prestador == id_fornecedor for o in orcamentos)

    def test_obter_orcamentos_por_status(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir orçamentos com status diferentes
        status_list = ["PENDENTE", "ACEITO", "PENDENTE"]
        for i, (id_fornecedor, status) in enumerate(zip(ids_fornecedores, status_list)):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                status, None, 100.00)
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamentos_pendentes = orcamento_repo.obter_orcamentos_por_status("PENDENTE")
        orcamentos_aceitos = orcamento_repo.obter_orcamentos_por_status("ACEITO")
        
        # Assert
        assert len(orcamentos_pendentes) == 2
        assert all(o.status == "PENDENTE" for o in orcamentos_pendentes)
        assert len(orcamentos_aceitos) == 1
        assert all(o.status == "ACEITO" for o in orcamentos_aceitos)

    def test_obter_orcamentos_por_pagina(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:5]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir 10 orçamentos
        for i in range(10):
            orcamento = Orcamento(0, id_demanda, ids_fornecedores[i % 5], datetime.now(), 
                                None, "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        pagina1 = orcamento_repo.obter_orcamentos_por_pagina(1, 5)
        pagina2 = orcamento_repo.obter_orcamentos_por_pagina(2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 5
        assert all(isinstance(o, Orcamento) for o in pagina1)
        assert all(isinstance(o, Orcamento) for o in pagina2)
```

# tests/test_prestador_servico_repo.py

```py
from model.prestador_servico_model import Prestador
from repo import prestador_servico_repo, usuario_repo, servico_repo

class TestPrestadorServicoRepo:
    def test_criar_tabela_prestador_servico(self, test_db):
        assert prestador_servico_repo.criar_tabela_prestador_servico() is True

    def test_inserir_prestador_servico(self, test_db, prestador_servico_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        usuario_repo.inserir_usuario(prestador_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        
        # Act
        ids = prestador_servico_repo.inserir_prestador_servico(prestador_servico_exemplo)
        
        # Assert
        assert ids == (1, 1)

    def test_atualizar_prestador_servico(self, test_db, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        usuario_repo.inserir_usuario(prestador_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        
        ps = Prestador(1, 1, "Observações iniciais", 100.0)
        prestador_servico_repo.inserir_prestador_servico(ps)
        
        # Act
        ps_atualizado = Prestador(1, 1, "Observações atualizadas", 150.0)
        sucesso = prestador_servico_repo.atualizar_prestador_servico(ps_atualizado)
        
        # Assert
        assert sucesso is True
        ps_obtido = prestador_servico_repo.obter_prestador_servico_por_id(1, 1)
        assert ps_obtido.observacoes == "Observações atualizadas"
        assert ps_obtido.preco == 150.0

    def test_excluir_prestador_servico(self, test_db, prestador_servico_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        usuario_repo.inserir_usuario(prestador_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        prestador_servico_repo.inserir_prestador_servico(prestador_servico_exemplo)
        
        # Act
        sucesso = prestador_servico_repo.excluir_prestador_servico(1, 1)
        
        # Assert
        assert sucesso is True
        assert prestador_servico_repo.obter_prestador_servico_por_id(1, 1) is None

    def test_obter_prestador_servico_por_id(self, test_db, prestador_servico_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        usuario_repo.inserir_usuario(prestador_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        prestador_servico_repo.inserir_prestador_servico(prestador_servico_exemplo)
        
        # Act
        ps = prestador_servico_repo.obter_prestador_servico_por_id(1, 1)
        
        # Assert
        assert ps is not None
        assert ps.id_prestador == 1
        assert ps.id_servico == 1
        assert ps.observacoes == "Observações teste"
        assert ps.preco == 100.0

    def test_obter_prestadores_servico_por_pagina(self, test_db, prestador_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        usuario_repo.inserir_usuario(prestador_exemplo)
        for servico in lista_servicos_exemplo[:5]:
            servico_repo.inserir_servico(servico)
        
        # Inserir relações
        for i in range(1, 6):
            ps = Prestador(1, i, f"Observações {i}", 100.0 * i)
            prestador_servico_repo.inserir_prestador_servico(ps)
        
        # Act
        pagina = prestador_servico_repo.obter_prestadores_servico_por_pagina(1, 3)
        
        # Assert
        assert len(pagina) == 3
        assert all(isinstance(ps, Prestador) for ps in pagina)

    def test_obter_prestador_servico_inexistente(self, test_db):
        # Arrange
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        # Act
        ps = prestador_servico_repo.obter_prestador_servico_por_id(999, 999)
        
        # Assert
        assert ps is None

    def test_atualizar_prestador_servico_inexistente(self, test_db):
        # Arrange
        prestador_servico_repo.criar_tabela_prestador_servico()
        ps = Prestador(999, 999, "Observações", 100.0)
        
        # Act
        sucesso = prestador_servico_repo.atualizar_prestador_servico(ps)
        
        # Assert
        assert sucesso is False

    def test_excluir_prestador_servico_inexistente(self, test_db, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        # Criar usuário e serviço necessários para satisfazer foreign key
        usuario_repo.inserir_usuario(prestador_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        
        # Act
        sucesso = prestador_servico_repo.excluir_prestador_servico(999, 999)
        
        # Assert
        assert sucesso is False
```

# tests/test_produto_repo.py

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
        assert produto_db.preco == 19.99, "O preço do produto inserido não confere"
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
        produto_inserido.preco = 20.99
        produto_inserido.descricao = "Descrição do produto atualizado"
        resultado = produto_repo.atualizar_produto(produto_inserido)
        # Assert
        assert resultado == True, "A atualização do produto deveria retornar True"
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_db.nome == "Produto Atualizado", "O nome do produto atualizado não confere"
        assert produto_db.preco == 20.99, "O preço do produto atualizado não confere"
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
        assert all(isinstance(u, Produto) for u in pagina_produtos), "Todos os itens da página devem ser do tipo Produto"
```

# tests/test_servicos_repo.py

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

    def test_obter_servico_por_id_inexistente(self, test_db):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        servico_db = servico_repo.obter_servico_por_id(999)
        # Assert
        assert servico_db is None, "O serviço buscado com ID inexistente deveria retornar None"

    def test_obter_servico_por_nome_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        servico_db = servico_repo.obter_servico_por_nome(servico_exemplo.nome)
        # Assert
        assert servico_db is not None, "O serviço buscado por nome deveria ser diferente de None"
        assert servico_db.id == id_servico_inserido, "O id do serviço buscado por nome deveria ser igual ao id do serviço inserido"
        assert servico_db.nome == servico_exemplo.nome, "O nome do serviço buscado deveria ser igual ao nome do serviço inserido"

    def test_obter_servico_por_nome_inexistente(self, test_db):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        servico_db = servico_repo.obter_servico_por_nome("Serviço Inexistente")
        # Assert
        assert servico_db is None, "O serviço buscado por nome inexistente deveria retornar None"

    def test_atualizar_servico_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        servico_db.nome = "Serviço Atualizado"
        servico_db.descricao = "Descrição Atualizada"
        servico_db.preco = 150.0
        resultado = servico_repo.atualizar_servico(servico_db)
        # Assert
        assert resultado == True, "A atualização do serviço deveria retornar True"
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_db.nome == "Serviço Atualizado", "O nome do serviço atualizado não confere"
        assert servico_db.descricao == "Descrição Atualizada", "A descrição do serviço atualizado não confere"
        assert servico_db.preco == 150.0, "O preço do serviço atualizado não confere"

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
        assert all(isinstance(s, Servico) for s in pagina_servicos), "Todos os itens da página devem ser do tipo Servico"
```

# tests/test_usuario_repo.py

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

    def test_inserir_noivo(self, test_db, usuario_exemplo):
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
        assert usuario_db.tipo == "ADMIN", "O tipo do usuário atualizado não confere"
        assert usuario_db.documento == "123.456.789-00", "O documento do usuário atualizado não confere"

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

# util/auth_decorator.py

```py
"""
Decorator para proteger rotas com autenticação e autorização
"""
from functools import wraps
from typing import List, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse


def obter_usuario_logado(request: Request) -> Optional[dict]:
    """
    Obtém os dados do usuário logado da sessão
    
    Args:
        request: Objeto Request do FastAPI
    
    Returns:
        Dicionário com dados do usuário ou None se não estiver logado
    """
    if not hasattr(request, 'session'):
        return None
    return request.session.get('usuario')


def esta_logado(request: Request) -> bool:
    """
    Verifica se há um usuário logado
    
    Args:
        request: Objeto Request do FastAPI
    
    Returns:
        True se há usuário logado, False caso contrário
    """
    return obter_usuario_logado(request) is not None


def criar_sessao(request: Request, usuario: dict) -> None:
    """
    Cria uma sessão para o usuário após login
    
    Args:
        request: Objeto Request do FastAPI
        usuario: Dicionário com dados do usuário
    """
    if hasattr(request, 'session'):
        # Remove senha da sessão por segurança
        usuario_sessao = usuario.copy()
        usuario_sessao.pop('senha', None)
        request.session['usuario'] = usuario_sessao


def destruir_sessao(request: Request) -> None:
    """
    Destrói a sessão do usuário (logout)
    
    Args:
        request: Objeto Request do FastAPI
    """
    if hasattr(request, 'session'):
        request.session.clear()


def requer_autenticacao(perfis_autorizados: List[str] = None):
    """
    Decorator para proteger rotas que requerem autenticação
    
    Args:
        perfis_autorizados: Lista de perfis autorizados a acessar a rota.
                           Se None, qualquer usuário logado pode acessar.
    
    Exemplo de uso:
        @router.get("/admin")
        @requer_autenticacao(['admin'])
        async def admin_page(request: Request):
            ...
        
        @router.get("/perfil")
        @requer_autenticacao()  # Qualquer usuário logado
        async def perfil(request: Request):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Encontra o objeto Request nos argumentos
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            # Verifica se o usuário está logado
            usuario = obter_usuario_logado(request)
            if not usuario:
                # Redireciona para login se não estiver autenticado
                return RedirectResponse(
                    url="/login?redirect=" + str(request.url.path),
                    status_code=status.HTTP_303_SEE_OTHER
                )
            
            # Verifica autorização se perfis foram especificados
            if perfis_autorizados:
                perfil_usuario = usuario.get('perfil', 'cliente')
                if perfil_usuario not in perfis_autorizados:
                    # Retorna erro 403 se não autorizado
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Você não tem permissão para acessar este recurso"
                    )
            
            # Adiciona o usuário aos kwargs para fácil acesso na rota
            kwargs['usuario_logado'] = usuario
            
            # Chama a função original
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Importação necessária para funções assíncronas
import asyncio
```

# util/database.py

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

# util/security.py

```py
"""
Módulo de segurança para gerenciar senhas e tokens
"""
import secrets
import string
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Contexto para hash de senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """
    Cria um hash seguro da senha usando bcrypt
    
    Args:
        senha: Senha em texto plano
    
    Returns:
        Hash da senha
    """
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash
    
    Args:
        senha_plana: Senha em texto plano
        senha_hash: Hash da senha armazenado no banco
    
    Returns:
        True se a senha está correta, False caso contrário
    """
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except:
        return False


def gerar_token_redefinicao(tamanho: int = 32) -> str:
    """
    Gera um token aleatório seguro para redefinição de senha
    
    Args:
        tamanho: Tamanho do token em caracteres
    
    Returns:
        Token aleatório
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))


def obter_data_expiracao_token(horas: int = 24) -> str:
    """
    Calcula a data de expiração do token
    
    Args:
        horas: Número de horas de validade do token
    
    Returns:
        Data de expiração no formato ISO
    """
    expiracao = datetime.now() + timedelta(hours=horas)
    return expiracao.isoformat()


def validar_forca_senha(senha: str) -> tuple[bool, str]:
    """
    Valida se a senha atende aos requisitos mínimos de segurança
    
    Args:
        senha: Senha a ser validada
    
    Returns:
        Tupla (válida, mensagem de erro se inválida)
    """
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    
    # Adicione mais validações conforme necessário
    # if not any(c.isupper() for c in senha):
    #     return False, "A senha deve conter pelo menos uma letra maiúscula"
    # if not any(c.islower() for c in senha):
    #     return False, "A senha deve conter pelo menos uma letra minúscula"
    # if not any(c.isdigit() for c in senha):
    #     return False, "A senha deve conter pelo menos um número"
    
    return True, ""


def gerar_senha_aleatoria(tamanho: int = 8) -> str:
    """
    Gera uma senha aleatória segura
    
    Args:
        tamanho: Tamanho da senha
    
    Returns:
        Senha aleatória
    """
    caracteres = string.ascii_letters + string.digits + "!@#$%"
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha
```

