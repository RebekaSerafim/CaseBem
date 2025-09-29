# 📋 Guia de Estilo - CaseBem

## 🎯 Princípios Gerais

1. **Clareza sobre Brevidade**: Prefira código claro a código conciso
2. **Consistência**: Siga sempre os mesmos padrões
3. **Simplicidade**: Evite over-engineering
4. **Educativo**: Código deve ensinar boas práticas

## 📝 Convenções de Nomenclatura

### Arquivos e Diretórios
```python
# ✅ Bom
usuario_service.py
categoria_repository.py
infrastructure/database/

# ❌ Evitar
UsuarioService.py
categoriaRepo.py
Infrastructure/Database/
```

### Classes
```python
# ✅ Bom
class UsuarioService:
    pass

class BaseRepository:
    pass

# ❌ Evitar
class usuarioService:
    pass

class baseRepo:
    pass
```

### Funções e Variáveis
```python
# ✅ Bom
def criar_usuario():
    nome_completo = "João Silva"
    email_usuario = "joao@teste.com"

# ❌ Evitar
def criarUsuario():
    nomeCompleto = "João Silva"
    emailUsuario = "joao@teste.com"
```

### Constantes
```python
# ✅ Bom
CRIAR_TABELA_USUARIO = "CREATE TABLE..."
TIMEOUT_CONEXAO = 30
BASE_URL = "https://api.casebem.com"

# ❌ Evitar
criar_tabela_usuario = "CREATE TABLE..."
TimeoutConexao = 30
```

## 📚 Docstrings

### Formato Padrão Google Style
```python
def processar_pagamento(valor: Decimal, usuario_id: int) -> bool:
    """
    Processa pagamento para um usuário específico.

    Esta função valida o valor do pagamento, verifica se o usuário existe
    e processa o pagamento através do gateway configurado.

    Args:
        valor: Valor a ser processado (deve ser positivo)
        usuario_id: ID do usuário válido no sistema

    Returns:
        True se processado com sucesso, False caso contrário

    Raises:
        ValidacaoError: Se valor for inválido ou negativo
        RecursoNaoEncontradoError: Se usuário não existir
        PagamentoError: Se falha no gateway de pagamento

    Example:
        >>> processar_pagamento(Decimal("100.50"), 123)
        True

        >>> processar_pagamento(Decimal("-10.00"), 123)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidacaoError: Valor deve ser positivo
    """
    pass
```

### Classes
```python
class UsuarioService:
    """
    Serviço para operações de negócio com usuários.

    Esta classe centraliza toda a lógica de negócio relacionada aos usuários,
    incluindo criação, autenticação, validações e operações complexas que
    envolvem múltiplos repositórios.

    Attributes:
        repo: Repositório de usuários para acesso aos dados
        logger: Logger para registrar operações importantes

    Example:
        >>> service = UsuarioService()
        >>> usuario_id = service.criar_usuario(dados_validos)
        >>> usuario = service.obter_usuario_por_id(usuario_id)
    """
    pass
```

## 🚨 Tratamento de Erros

### Use Exceções Específicas
```python
# ✅ Bom
if not usuario:
    raise RecursoNaoEncontradoError("Usuário", usuario_id)

if valor <= 0:
    raise ValidacaoError("Valor deve ser positivo", "valor", valor)

# ❌ Evitar
if not usuario:
    raise Exception("Usuário não encontrado")

if valor <= 0:
    return None  # Falha silenciosa
```

### Logs Estruturados
```python
# ✅ Bom
logger.log_error("Falha ao processar pagamento", extra={
    'usuario_id': usuario_id,
    'valor': float(valor),
    'erro': str(e),
    'metodo_pagamento': 'cartao'
})

# ❌ Evitar
print(f"Erro: {e}")
logging.error("Erro no pagamento")
```

### Context Managers para Recursos
```python
# ✅ Bom
from infrastructure.database.connection import obter_conexao

def obter_usuario(user_id: int) -> Usuario:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        # ... operações
        return usuario

# ❌ Evitar
def obter_usuario(user_id: int) -> Usuario:
    conn = sqlite3.connect('banco.db')
    # ... operações sem finally
    conn.close()
```

## 🧪 Testes

### Nomenclatura de Testes
```python
# ✅ Bom
def test_criar_usuario_com_email_duplicado_deve_falhar():
    pass

def test_autenticar_usuario_com_credenciais_validas_retorna_usuario():
    pass

def test_listar_categorias_ativas_retorna_apenas_ativas():
    pass

# ❌ Evitar
def test_user_creation():
    pass

def test_login():
    pass

def test1():
    pass
```

### Estrutura AAA (Arrange, Act, Assert)
```python
def test_criar_categoria_com_sucesso():
    # Arrange
    dados = {
        'nome': 'Fotografia',
        'tipo_fornecimento': TipoFornecimento.SERVICO,
        'descricao': 'Serviços de fotografia profissional'
    }

    # Act
    categoria_id = categoria_service.criar_categoria(dados)

    # Assert
    assert categoria_id is not None
    assert categoria_id > 0

    categoria = categoria_service.obter_categoria_por_id(categoria_id)
    assert categoria.nome == 'Fotografia'
    assert categoria.ativo is True
```

### Use Factories para Dados de Teste
```python
# ✅ Bom
def test_inserir_usuario():
    # Arrange
    usuario = usuario_factory.criar(nome="João", email="joao@teste.com")

    # Act
    user_id = repo.inserir(usuario)

    # Assert
    assert_usuario_valido(repo.obter_por_id(user_id))

# ❌ Evitar
def test_inserir_usuario():
    # Dados hardcoded, difíceis de manter
    usuario = Usuario(0, "João Silva", "123.456.789-00", ...)
    # ...
```

## 📊 Estrutura de Arquivos

### Organização de Imports
```python
# 1. Imports da biblioteca padrão
import os
import sys
from datetime import datetime
from typing import Optional, List, Dict

# 2. Imports de terceiros
import pytest
from fastapi import FastAPI
from pydantic import BaseModel

# 3. Imports do projeto (por camada)
from core.models.usuario_model import Usuario
from core.services.usuario_service import usuario_service
from infrastructure.database.connection import obter_conexao
from api.dtos.usuario_dtos import UsuarioDTO
```

### Estrutura de Módulos
```python
# Início do arquivo: docstring do módulo
"""
Serviço de usuários - Lógica de negócio centralizada

Este módulo contém toda a lógica de negócio relacionada aos usuários,
incluindo validações, regras de domínio e orquestração de operações.
"""

# Imports (organizados como acima)

# Constantes do módulo
DEFAULT_TIMEOUT = 30
MAX_TENTATIVAS = 3

# Classes e funções (principais primeiro)
class UsuarioService:
    pass

# Funções auxiliares
def _validar_email(email: str) -> bool:
    pass

# Instância global (se necessário)
usuario_service = UsuarioService()
```

## 🔍 Code Review - Checklist

### Antes de Fazer Commit
- [ ] Código segue convenções de nomenclatura
- [ ] Funções têm docstrings adequadas
- [ ] Tratamento de erros com exceções específicas
- [ ] Testes cobrem cenários principais
- [ ] Logs estruturados onde necessário
- [ ] Imports organizados
- [ ] Não há comentários óbvios
- [ ] Código é autoexplicativo

### Durante Code Review
- [ ] Código é fácil de entender?
- [ ] Responsabilidades estão bem separadas?
- [ ] Testes são suficientes?
- [ ] Performance é adequada?
- [ ] Segurança foi considerada?
- [ ] Documentação está atualizada?

## 💡 Dicas Específicas do CaseBem

### Padrões do Projeto
1. **Repositórios**: Sempre herdem de `BaseRepo`
2. **Serviços**: Centralizem lógica de negócio
3. **DTOs**: Para validação de entrada
4. **Exceptions**: Sempre tipadas e específicas
5. **Testes**: Usem factories e helpers

### Validações
```python
# ✅ Padrão do projeto
if user_id <= 0:
    raise ValidacaoError("ID deve ser positivo", "user_id", user_id)

# Service layer valida regras de negócio
if self._email_ja_existe(email):
    raise RegraDeNegocioError("Email já cadastrado", regra="EMAIL_UNICO")
```

### Logging
```python
# ✅ Padrão do projeto
logger.log_info("Usuário criado", extra={
    'usuario_id': user_id,
    'email': email,
    'perfil': perfil.value
})
```

---

**Este guia deve ser seguido por todos os desenvolvedores do projeto CaseBem para manter consistência e qualidade do código.**