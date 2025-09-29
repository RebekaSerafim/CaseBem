# 📋 FASE 2: Simplificar DTOs e Centralizar Validações

## 🎯 Objetivo Principal
Reduzir a complexidade dos DTOs criando uma estrutura base reutilizável e otimizando o sistema de validações já existente em `util/validacoes_dto.py`.

## 🔍 Análise do Problema Atual

### Estatísticas dos DTOs:
- **12 arquivos DTO** na pasta `dtos/`
- **Padrão repetitivo** em todos: configuração Pydantic, field_validators similares
- **Validações bem organizadas** em `util/validacoes_dto.py` (477 linhas) - PONTO POSITIVO!
- **Código duplicado**: Configurações e imports repetidos

### Exemplo Atual (categoria_dto.py):
```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from model.tipo_fornecimento_model import TipoFornecimento
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_enum_valor,
    ValidacaoError
)
import re

class CategoriaDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "nome": "Fotografia",
                "tipo_fornecimento": "SERVIÇO",
                "descricao": "Serviços de fotografia para eventos",
                "ativo": True
            }
        }
    )

    nome: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    tipo_fornecimento: TipoFornecimento = Field(..., description="Tipo de fornecimento")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição da categoria")
    ativo: bool = Field(True, description="Categoria está ativa")

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        # Padrão repetido em todos os DTOs
        try:
            nome = validar_texto_obrigatorio(v, "Nome da categoria", min_chars=2, max_chars=50)
            if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-&/]+$', nome):
                raise ValidacaoError('Nome deve conter apenas letras, números...')
            return nome
        except ValidacaoError as e:
            raise ValueError(str(e))
```

## 💡 Solução Proposta

### 1. Criar `dtos/base_dto.py`:

```python
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Dict, Any
from util.validacoes_dto import ValidacaoError

class BaseDTO(BaseModel):
    """
    Classe base para todos os DTOs do sistema.
    Fornece configurações padrão e métodos de validação comuns.
    """

    model_config = ConfigDict(
        # Remover espaços em branco automaticamente
        str_strip_whitespace=True,
        # Validar na atribuição também (não só na criação)
        validate_assignment=True,
        # Usar valores dos enums ao invés dos objetos
        use_enum_values=True,
        # Permitir population by name (útil para formulários HTML)
        populate_by_name=True,
        # Validar valores padrão também
        validate_default=True
    )

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> Dict[str, Any]:
        """
        Cria um exemplo JSON para documentação da API.
        Pode ser sobrescrito nas classes filhas.
        """
        return {"exemplo": "Sobrescrever na classe filha", **overrides}

    @classmethod
    def validar_campo_wrapper(cls, validador_func, campo_nome: str):
        """
        Wrapper para padronizar o tratamento de erros de validação.
        Evita repetir try/except em cada field_validator.
        """
        def wrapper(valor):
            try:
                return validador_func(valor, campo_nome)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return wrapper

    def to_dict(self) -> dict:
        """Converte DTO para dicionário simples"""
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        """Converte DTO para JSON"""
        return self.model_dump_json(exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict):
        """Cria DTO a partir de dicionário"""
        return cls(**data)
```

### 2. Criar DTOs Específicos por Domínio:

#### `dtos/categoria_dtos.py`:
```python
from pydantic import Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from model.tipo_fornecimento_model import TipoFornecimento
from util.validacoes_dto import validar_texto_obrigatorio, validar_texto_opcional, validar_enum_valor
import re

class CategoriaDTO(BaseDTO):
    """DTO para operações com categorias"""

    nome: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    tipo_fornecimento: TipoFornecimento = Field(..., description="Tipo de fornecimento")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição da categoria")
    ativo: bool = Field(True, description="Categoria está ativa")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2, max_chars=50),
            "Nome da categoria"
        )
        nome = validador(v)

        # Validação específica de categoria
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-&/]+$', nome):
            raise ValueError('Nome deve conter apenas letras, números, espaços, hífens e símbolos (&, /)')
        return nome

    @field_validator('tipo_fornecimento')
    @classmethod
    def validar_tipo(cls, v):
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_enum_valor(valor, TipoFornecimento, campo),
            "Tipo de fornecimento"
        )
        return validador(v)

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(validar_texto_opcional, "Descrição")
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        exemplo = {
            "nome": "Fotografia",
            "tipo_fornecimento": "SERVIÇO",
            "descricao": "Serviços profissionais de fotografia para casamentos",
            "ativo": True
        }
        exemplo.update(overrides)
        return exemplo

# Adicionar ao model_config da classe
CategoriaDTO.model_config.json_schema_extra = {
    "example": CategoriaDTO.criar_exemplo_json()
}


class CategoriaListaDTO(BaseDTO):
    """DTO para listar categorias com filtros"""

    tipo_fornecimento: Optional[TipoFornecimento] = Field(None, description="Filtrar por tipo")
    ativo: Optional[bool] = Field(None, description="Filtrar por status ativo")
    nome_busca: Optional[str] = Field(None, max_length=50, description="Buscar no nome")

    @field_validator('nome_busca')
    @classmethod
    def validar_busca(cls, v: Optional[str]) -> Optional[str]:
        if v:
            validador = cls.validar_campo_wrapper(validar_texto_opcional, "Busca")
            return validador(v)
        return v
```

#### `dtos/usuario_dtos.py`:
```python
from pydantic import Field, field_validator, EmailStr
from typing import Optional
from .base_dto import BaseDTO
from model.usuario_model import TipoUsuario
from util.validacoes_dto import (
    validar_nome_pessoa, validar_cpf, validar_telefone,
    validar_data_nascimento, validar_senha, validar_senhas_coincidem
)

class UsuarioBaseDTO(BaseDTO):
    """DTO base para dados comuns de usuário"""

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo")
    cpf: Optional[str] = Field(None, description="CPF (opcional)")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento (YYYY-MM-DD)")
    email: EmailStr = Field(..., description="Email válido")
    telefone: str = Field(..., description="Telefone com DDD")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(validar_nome_pessoa, "Nome")
        return validador(v)

    @field_validator('cpf')
    @classmethod
    def validar_cpf_campo(cls, v: Optional[str]) -> Optional[str]:
        if v:
            validador = cls.validar_campo_wrapper(validar_cpf, "CPF")
            return validador(v)
        return v

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(validar_telefone, "Telefone")
        return validador(v)

    @field_validator('data_nascimento')
    @classmethod
    def validar_data(cls, v: Optional[str]) -> Optional[str]:
        if v:
            validador = cls.validar_campo_wrapper(validar_data_nascimento, "Data de nascimento")
            return validador(v)
        return v


class CriarUsuarioDTO(UsuarioBaseDTO):
    """DTO para criação de usuário"""

    senha: str = Field(..., min_length=6, max_length=128, description="Senha")
    confirmar_senha: str = Field(..., description="Confirmação da senha")
    perfil: TipoUsuario = Field(TipoUsuario.NOIVO, description="Tipo de usuário")

    @field_validator('senha')
    @classmethod
    def validar_senha_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(validar_senha, "Senha")
        return validador(v)

    def model_post_init(self, __context):
        """Validação que precisa de múltiplos campos"""
        validar_senhas_coincidem(self.senha, self.confirmar_senha)


class AtualizarUsuarioDTO(UsuarioBaseDTO):
    """DTO para atualização de dados do usuário (sem senha)"""
    pass


class AlterarSenhaDTO(BaseDTO):
    """DTO específico para alteração de senha"""

    senha_atual: str = Field(..., description="Senha atual")
    nova_senha: str = Field(..., min_length=6, max_length=128, description="Nova senha")
    confirmar_nova_senha: str = Field(..., description="Confirmação da nova senha")

    @field_validator('nova_senha')
    @classmethod
    def validar_nova_senha(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(validar_senha, "Nova senha")
        return validador(v)

    def model_post_init(self, __context):
        validar_senhas_coincidem(self.nova_senha, self.confirmar_nova_senha)
```

### 3. Otimizar Validações Existentes:

#### Adicionar em `util/validacoes_dto.py`:
```python
# Adicionar no final do arquivo

class ValidadorWrapper:
    """Classe para facilitar o uso de validadores em field_validators"""

    @staticmethod
    def criar_validador(funcao_validacao, campo_nome: str = None, **kwargs):
        """
        Cria um validador pronto para usar com @field_validator

        Exemplo:
        validar_nome = ValidadorWrapper.criar_validador(
            validar_nome_pessoa, "Nome", min_chars=2, max_chars=100
        )
        """
        def validador(valor):
            try:
                return funcao_validacao(valor, campo_nome or "Campo", **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador

    @staticmethod
    def criar_validador_opcional(funcao_validacao, **kwargs):
        """Cria validador para campos opcionais"""
        def validador(valor):
            if valor is None:
                return None
            try:
                return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador


# Validadores pré-configurados comuns
VALIDADOR_NOME = ValidadorWrapper.criar_validador(validar_nome_pessoa, "Nome")
VALIDADOR_CPF = ValidadorWrapper.criar_validador_opcional(validar_cpf)
VALIDADOR_TELEFONE = ValidadorWrapper.criar_validador(validar_telefone, "Telefone")
VALIDADOR_SENHA = ValidadorWrapper.criar_validador(validar_senha, "Senha")
```

## 📁 Nova Estrutura de DTOs

### Organização Proposta:
```
dtos/
├── base_dto.py          # Classe base
├── usuario_dtos.py      # Todos DTOs de usuário
├── categoria_dtos.py    # DTOs de categoria
├── item_dtos.py         # DTOs de itens
├── orcamento_dtos.py    # DTOs de orçamento
└── __init__.py          # Imports facilitados
```

### `dtos/__init__.py`:
```python
"""
DTOs do sistema CaseBem - Importações facilitadas
"""

from .base_dto import BaseDTO

# DTOs de usuário
from .usuario_dtos import (
    UsuarioBaseDTO, CriarUsuarioDTO,
    AtualizarUsuarioDTO, AlterarSenhaDTO
)

# DTOs de categoria
from .categoria_dtos import CategoriaDTO, CategoriaListaDTO

# DTOs de item (quando criados)
# from .item_dtos import ItemDTO, ItemListaDTO

__all__ = [
    # Base
    'BaseDTO',

    # Usuário
    'UsuarioBaseDTO', 'CriarUsuarioDTO',
    'AtualizarUsuarioDTO', 'AlterarSenhaDTO',

    # Categoria
    'CategoriaDTO', 'CategoriaListaDTO',
]
```

## 📊 Análise de Impacto

### Antes:
- **12 arquivos DTO** individuais com ~60 linhas cada = **720 linhas**
- Configurações duplicadas em cada DTO
- Validações espalhadas e inconsistentes
- Imports repetitivos

### Depois:
- **1 arquivo base** + **4-5 arquivos agrupados** = ~**500 linhas totais**
- **Redução de ~30%** no código dos DTOs
- Configurações centralizadas
- Validações padronizadas
- Imports facilitados através do `__init__.py`

## 🎓 Conceitos Ensinados aos Alunos

1. **Herança com Pydantic**: Como usar classes base com BaseModel
2. **Organização por Domínio**: Agrupar funcionalidades relacionadas
3. **Wrapper Functions**: Como simplificar código repetitivo
4. **Validation Patterns**: Padrões comuns de validação
5. **Module Organization**: Como organizar imports e módulos

## 📝 Passo a Passo da Implementação

### Passo 1: Criar estrutura base
1. Criar `dtos/base_dto.py` com configurações comuns
2. Criar `dtos/__init__.py` para imports facilitados
3. Testar a base com um DTO simples

### Passo 2: Migrar DTOs por domínio
1. **Usuário**: Migrar todos DTOs relacionados a usuário
2. **Categoria**: Migrar DTOs de categoria
3. **Item**: Agrupar DTOs de itens e fornecedores
4. **Outros**: Agrupar demais DTOs

### Passo 3: Otimizar validações
1. Adicionar ValidadorWrapper em validacoes_dto.py
2. Criar validadores pré-configurados comuns
3. Simplificar field_validators existentes

### Passo 4: Atualizar imports
1. Atualizar imports nas rotas
2. Atualizar testes que usam DTOs
3. Verificar que tudo funciona

## ⚠️ Riscos e Mitigações

### Risco 1: Quebrar imports existentes
**Mitigação**: Fazer imports retrocompatíveis no `__init__.py`

### Risco 2: Validações muito genéricas
**Mitigação**: Permitir validações específicas nas classes filhas

### Risco 3: Complexidade do ValidadorWrapper
**Mitigação**: Manter sintaxe simples e documentar bem

## ✅ Critérios de Sucesso

- [ ] BaseDTO criado e funcionando
- [ ] Pelo menos 3 domínios de DTO agrupados
- [ ] Redução de 150+ linhas de código
- [ ] Todos os testes passando
- [ ] Imports facilitados funcionando

## 🔄 Compatibilidade com Código Existente

Para não quebrar código, manter imports retrocompatíveis:

```python
# Em dtos/__init__.py - compatibilidade
from .categoria_dtos import CategoriaDTO as CategoriaDTO_old
from .usuario_dtos import CriarUsuarioDTO as CadastroNoivosDTO

# Para código antigo continuar funcionando
CategoriaDTO = CategoriaDTO_old
```

## 🚀 Próximos Passos

Após completar a Fase 2:
- **Fase 3**: Centralizar tratamento de erros
- **Fase 4**: Simplificar estrutura de testes

## 💬 Exemplo de Explicação para Alunos

> "Imaginem que vocês têm vários formulários web. Todos precisam validar email, telefone, etc. Em vez de escrever essas validações em cada formulário, vocês criam um 'formulário base' com as validações comuns. É isso que faremos com nossos DTOs - uma classe base que todos vão herdar!"