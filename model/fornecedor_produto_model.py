from dataclasses import dataclass
from typing import Optional

from model.produto_model import Produto
from model.usuario_model import Usuario

@dataclass
class FornecedorProduto:
    id_fornecedor: int
    id_produto: int
    observacoes: Optional[str]
    preco: Optional[float]
    fornecedor: Optional[Usuario] = None
    produto: Optional[Produto] = None
