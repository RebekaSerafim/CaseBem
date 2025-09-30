from dataclasses import dataclass
from typing import Optional

from core.models.usuario_model import Usuario

@dataclass
class Casal:
    id: int
    id_noivo1: int
    id_noivo2: Optional[int] = None
    data_casamento: Optional[str] = None
    local_previsto: Optional[str] = None
    orcamento_estimado: Optional[str] = None
    numero_convidados: Optional[int] = None
    data_cadastro: Optional[str] = None
    noivo1: Optional[Usuario] = None
    noivo2: Optional[Usuario] = None