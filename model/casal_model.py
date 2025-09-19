from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Casal:
    id: int
    id_noivo1: int
    id_noivo2: int
    orcamento_estimado: float
    data_prevista: Optional[str]
    local_previsto: Optional[str]
    numero_convidados: Optional[int]
    noivo1: Optional[Usuario] = None
    noivo2: Optional[Usuario] = None