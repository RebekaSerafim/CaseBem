from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TipoUsuario(Enum):
    ADMIN = "ADMIN"
    NOIVO = "NOIVO"
    PROFISSIONAL = "PROFISSIONAL"

@dataclass
class Usuario:
    id: int
    nome: str
    cpf: Optional[str]
    data_nascimento: Optional[str]
    email: str
    telefone: str
    senha: str
    perfil: TipoUsuario
    foto: Optional[str]
    token_redefinicao: Optional[str]
    data_token: Optional[str]
    data_cadastro: Optional[str]