from dataclasses import dataclass
from typing import Optional

@dataclass
class Noivo:
    id: Optional[int] = None
    orcamento: float
    id_noivo1: str
    id_noivo2: str
    tipo: Optional[str] = None
