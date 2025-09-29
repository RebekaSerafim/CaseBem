from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TipoUsuario(Enum):
    ADMIN = "ADMIN"
    NOIVO = "NOIVO"
    FORNECEDOR = "FORNECEDOR"

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
    token_redefinicao: Optional[str]
    data_token: Optional[str]
    data_cadastro: Optional[str]
    ativo: bool = True