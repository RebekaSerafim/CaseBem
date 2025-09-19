from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Casal:
    id: int
    id_noivo1: int
    id_noivo2: Optional[int] = None
    nome_parceiro: Optional[str] = None
    data_casamento: Optional[str] = None
    local_cerimonia: Optional[str] = None
    local_festa: Optional[str] = None
    numero_convidados: Optional[int] = None
    observacoes: Optional[str] = None
    data_criacao: Optional[str] = None
    noivo1: Optional[Usuario] = None
    noivo2: Optional[Usuario] = None