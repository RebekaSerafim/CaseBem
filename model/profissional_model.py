from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Profissional(Usuario):
    nome_empresa: Optional[str] = None
    cnpj: Optional[str] = None
    descricao: Optional[str] = None
    prestador: bool = False
    fornecedor: bool = False
    locador: bool = False