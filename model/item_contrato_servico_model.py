from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemContratoServico:
    id_item_contrato_servico: Optional[int]
    valor: Optional[float]
    quantidade: int
    id_servico: int
