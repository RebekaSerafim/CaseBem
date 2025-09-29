"""
Pacote de DTOs do sistema CaseBem.

Este módulo centraliza todos os DTOs (Data Transfer Objects) organizados por funcionalidade:
- BaseDTO: Classe base com configurações comuns
- categoria_dtos: DTOs relacionados a categorias
- usuario_dtos: DTOs relacionados a usuários e autenticação
- item_dtos: DTOs relacionados a itens e fornecedores
- noivos_dtos: DTOs relacionados a noivos e casais
- orcamento_dtos: DTOs relacionados a demandas e orçamentos

Imports facilitados para os DTOs mais comuns:
"""

# Base
from .base_dto import BaseDTO

# Categoria
from .categoria_dtos import CategoriaDTO, CategoriaListaDTO

# Usuário e Autenticação
from .usuario_dtos import (
    LoginDTO, AlterarSenhaDTO,
    AdminUsuarioDTO, PerfilAdminDTO
)

# Item e Fornecedor
from .item_dtos import (
    ItemFornecedorDTO, CadastroFornecedorDTO,
    PerfilFornecedorDTO
)

# Noivos e Casais
from .noivos_dtos import (
    CadastroNoivosDTO, PerfilNoivoDTO,
    GeneroEnum
)

# Demandas e Orçamentos
from .orcamento_dtos import (
    DemandaNoivoDTO, PropostaOrcamentoDTO,
    FormaPagamentoEnum
)

__all__ = [
    # Base
    'BaseDTO',

    # Categoria
    'CategoriaDTO', 'CategoriaListaDTO',

    # Usuário
    'LoginDTO', 'AlterarSenhaDTO', 'AdminUsuarioDTO', 'PerfilAdminDTO',

    # Item e Fornecedor
    'ItemFornecedorDTO', 'CadastroFornecedorDTO', 'PerfilFornecedorDTO',

    # Noivos
    'CadastroNoivosDTO', 'PerfilNoivoDTO', 'GeneroEnum',

    # Orçamentos
    'DemandaNoivoDTO', 'PropostaOrcamentoDTO', 'FormaPagamentoEnum'
]