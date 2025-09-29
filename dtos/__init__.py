"""
Pacote de DTOs do sistema CaseBem.

Este módulo centraliza todos os DTOs (Data Transfer Objects) organizados por funcionalidade:
- BaseDTO: Classe base com configurações comuns
- categoria_dtos: DTOs relacionados a categorias
- usuario_dtos: DTOs relacionados a usuários e autenticação
- item_dtos: DTOs relacionados a itens e fornecedores

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

# Outros DTOs que ainda não foram migrados
from .cadastro_noivos_dto import CadastroNoivosDTO
from .perfil_noivo_dto import PerfilNoivoDTO
from .demanda_noivo_dto import DemandaNoivoDTO
from .proposta_orcamento_dto import PropostaOrcamentoDTO

__all__ = [
    # Base
    'BaseDTO',

    # Categoria
    'CategoriaDTO', 'CategoriaListaDTO',

    # Usuário
    'LoginDTO', 'AlterarSenhaDTO', 'AdminUsuarioDTO', 'PerfilAdminDTO',

    # Item e Fornecedor
    'ItemFornecedorDTO', 'CadastroFornecedorDTO', 'PerfilFornecedorDTO',

    # Outros (não migrados ainda)
    'CadastroNoivosDTO', 'PerfilNoivoDTO', 'DemandaNoivoDTO', 'PropostaOrcamentoDTO'
]