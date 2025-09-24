from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Fornecedor(Usuario):
    nome_empresa: Optional[str] = None
    cnpj: Optional[str] = None
    descricao: Optional[str] = None
    verificado: bool = False
    data_verificacao: Optional[str] = None
    newsletter: bool = False