from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Casal:
    id_noivo1: int
    id_noivo2: int
    orcamento: float
    noivo1: Optional[Usuario] = None
    noivo2: Optional[Usuario] = None