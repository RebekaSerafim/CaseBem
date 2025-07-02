from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Prestador(Usuario):
    tipo_pessoa: str
    documento: str
    