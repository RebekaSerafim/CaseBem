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
