from dataclasses import dataclass
from typing import Optional
from model.orcamento_model import Orcamento
from model.produto_model import Produto

@dataclass
class ItemOrcamentoProduto:
    id_orcamento: int
    id_produto: int
    preco_unitario: float
    quantidade: int
    observacoes: Optional[str] = None
    orcamento: Optional[Orcamento] = None
    produto: Optional[Produto] = None