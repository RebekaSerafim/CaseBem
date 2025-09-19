from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

class StatusDemanda(Enum):
    ATIVA = "ATIVA"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"

@dataclass
class Demanda:
    id: int
    id_noivo: int
    titulo: str
    descricao: str
    orcamento_min: Optional[float] = None
    orcamento_max: Optional[float] = None
    prazo_entrega: Optional[str] = None
    status: StatusDemanda = StatusDemanda.ATIVA
    data_criacao: Optional[str] = None
    observacoes: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = StatusDemanda(self.status)