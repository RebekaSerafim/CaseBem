from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemDemanda:
    id_demanda: int
    id_item: int
    quantidade: int
    observacoes: Optional[str] = None
    preco_maximo: Optional[float] = None