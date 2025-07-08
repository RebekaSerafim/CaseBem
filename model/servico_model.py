from dataclasses import dataclass
from typing import Optional

@dataclass
class Servico:
    id: int
    nome: str
    preco: float
    descricao: str    

    