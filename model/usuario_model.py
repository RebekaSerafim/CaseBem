from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TipoUsuario(Enum):
    ADMIN = "ADMIN"
    NOIVO = "NOIVO"        
    FORNECEDOR = "FORNECEDOR"
    PRESTADOR = "PRESTADOR"

@dataclass
class Usuario:
    id: int
    nome: str
    telefone: str
    email: str    
    senha_hash: str
    tipo: TipoUsuario
    documento: Optional[str] = None