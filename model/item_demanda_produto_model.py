from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemDemandaProduto:
    id_demanda: int
    id_produto: int    
    quantidade: int
    observacoes: Optional[str] = None
    demanda: Optional[Demanda] = None
    produto: Optional[Produto] = None
