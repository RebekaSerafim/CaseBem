from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemDemandaServico:
    id_demanda: int
    id_servico: int
    quantidade: int
    observacoes: Optional[str] = None
    demanda: Optional[Demanda] = None
    servico: Optional[Servico] = None