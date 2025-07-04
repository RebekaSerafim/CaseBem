from dataclasses import dataclass
from typing import Optional

@dataclass
class FornecedorProduto:
    id_fornecedor: int
    id_produto: int
    observacoes: Optional[str]
    preco: Optional[float]
