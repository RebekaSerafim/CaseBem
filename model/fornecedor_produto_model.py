from dataclasses import dataclass
from typing import Optional

from model.produto_model import Produto
from model.profissional_model import Profissional

@dataclass
class FornecedorProduto:
    id_profissional: int
    id_produto: int
    observacoes: Optional[str]
    preco: Optional[float]
    profissional: Optional[Profissional] = None
    produto: Optional[Produto] = None
