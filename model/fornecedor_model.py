from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Fornecedor(Usuario):
    id_fornecedor: int
    