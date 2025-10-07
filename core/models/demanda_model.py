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
    """
    Representa uma demanda criada por um casal de noivos.

    A demanda contém informações gerais sobre o que os noivos precisam.
    Os itens específicos são armazenados em ItemDemanda (tabela separada).

    Campos data_casamento e cidade_casamento são preenchidos automaticamente
    a partir dos dados do casal.
    """
    id: int
    id_casal: int
    descricao: str  # Descrição geral da demanda
    orcamento_total: Optional[float] = None  # Orçamento total da demanda
    data_casamento: Optional[str] = None  # Data do casamento (do casal)
    cidade_casamento: Optional[str] = None  # Cidade do casamento (do casal)
    prazo_entrega: Optional[str] = None  # Prazo desejado
    status: StatusDemanda = StatusDemanda.ATIVA
    data_criacao: Optional[str] = None
    observacoes: Optional[str] = None  # Observações adicionais

    def __post_init__(self) -> None:
        if isinstance(self.status, str):
            self.status = StatusDemanda(self.status)