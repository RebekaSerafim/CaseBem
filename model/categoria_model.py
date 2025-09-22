from dataclasses import dataclass
from typing import Optional
from model.item_model import TipoItem

@dataclass
class Categoria:
    id: int
    nome: str
    tipo_fornecimento: TipoItem
    descricao: Optional[str] = None
    ativo: bool = True