from dataclasses import dataclass
from typing import Optional

from model.servico_model import Servico
from model.usuario_model import Usuario

@dataclass
class PrestadorServico:
    id_prestador: int
    id_servico: int
    observacoes: str
    preco: Optional[float] = None
    prestador: Optional[Usuario] = None
    servico: Optional[Servico] = None
