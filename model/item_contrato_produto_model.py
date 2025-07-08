from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemContratoProduto:
    id_item_contrato_produto: Optional[int]
    valor: Optional[float]
    quantidade: int
    id_produto: int
