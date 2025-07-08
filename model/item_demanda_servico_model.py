from dataclasses import dataclass
from typing import Optional

from model.demanda_model import Demanda
from model.servico_model import Servico

@dataclass
class ItemDemandaServico:
    id_demanda: int
    id_servico: int
    quantidade: int
    observacoes: Optional[str] = None
    demanda: Optional[Demanda] = None
    servico: Optional[Servico] = None