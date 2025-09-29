from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemOrcamento:
    id_orcamento: int
    id_item: int
    quantidade: int
    preco_unitario: float
    observacoes: Optional[str] = None
    desconto: Optional[float] = None

    @property
    def preco_total(self) -> float:
        subtotal = self.quantidade * self.preco_unitario
        if self.desconto:
            return subtotal - self.desconto
        return subtotal