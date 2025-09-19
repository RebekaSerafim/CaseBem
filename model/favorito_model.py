from dataclasses import dataclass
from typing import Optional

@dataclass
class Favorito:
    id: int
    id_noivo: int
    id_item: int
    data_adicao: Optional[str] = None