from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Produto:
    id: int
    nome: str
    preco: float    
    descricao: str
    
    