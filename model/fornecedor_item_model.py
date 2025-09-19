from dataclasses import dataclass
from typing import Optional
from model.item_model import TipoItem

@dataclass
class FornecedorItem:
    id_fornecedor: int
    id_item: int
    observacoes: Optional[str] = None
    preco_personalizado: Optional[float] = None
    disponivel: bool = True