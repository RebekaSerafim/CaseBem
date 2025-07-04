from dataclasses import dataclass
from typing import Optional

@dataclass
class PrestadorServico:
    id: Optional[int]
    id_prestador: int
    descricao: str
