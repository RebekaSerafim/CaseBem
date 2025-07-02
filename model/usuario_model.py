from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome: str
    telefone: str
    email: str    
    senha_hash: Optional[str] = None
    tipo: Optional[str] = None
    