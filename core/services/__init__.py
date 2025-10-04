"""
Serviços do sistema CaseBem

Camada de lógica de negócio (Service Layer).
Aqui ficam as regras de negócio e orquestração entre repositórios.
"""

from core.services.usuario_service import usuario_service, UsuarioService
from core.services.categoria_service import categoria_service, CategoriaService
from core.services.fornecedor_service import fornecedor_service, FornecedorService
from core.services.item_service import item_service, ItemService
from core.services.casal_service import casal_service, CasalService
from core.services.demanda_service import demanda_service, DemandaService
from core.services.orcamento_service import orcamento_service, OrcamentoService
from core.services.chat_service import chat_service, ChatService
from core.services.favorito_service import favorito_service, FavoritoService

__all__ = [
    'usuario_service', 'UsuarioService',
    'categoria_service', 'CategoriaService',
    'fornecedor_service', 'FornecedorService',
    'item_service', 'ItemService',
    'casal_service', 'CasalService',
    'demanda_service', 'DemandaService',
    'orcamento_service', 'OrcamentoService',
    'chat_service', 'ChatService',
    'favorito_service', 'FavoritoService',
]