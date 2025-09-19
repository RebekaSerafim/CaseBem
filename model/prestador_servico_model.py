from dataclasses import dataclass
from typing import Optional

from model.servico_model import Servico
from model.profissional_model import Profissional

@dataclass
class PrestadorServico:
    id_profissional: int
    id_servico: int
    observacoes: str
    preco: Optional[float] = None
    profissional: Optional[Profissional] = None
    servico: Optional[Servico] = None
