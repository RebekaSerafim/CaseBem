from dataclasses import dataclass
from typing import Optional
from model.orcamento_model import Orcamento
from model.servico_model import Servico

@dataclass
class ItemOrcamentoServico:
    id_orcamento: int
    id_servico: int
    preco_unitario: float
    quantidade: int
    observacoes: Optional[str] = None
    orcamento: Optional[Orcamento] = None
    servico: Optional[Servico] = None