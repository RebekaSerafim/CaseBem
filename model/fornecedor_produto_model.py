from dataclasses import dataclass
from typing import Optional

from model.produto_model import Produto
from model.fornecedor_model import Fornecedor

@dataclass
class FornecedorProduto:
    id_fornecedor: int
    id_produto: int
    observacoes: Optional[str]
    preco: Optional[float]
    fornecedor: Optional[Fornecedor] = None
    produto: Optional[Produto] = None
