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
    email: str
    senha: str
    perfil: str = 'cliente'
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None