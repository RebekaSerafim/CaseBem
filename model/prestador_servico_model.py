from dataclasses import dataclass
from typing import Optional

from model.servico_model import Servico
from model.fornecedor_model import Fornecedor

@dataclass
class PrestadorServico:
    id_fornecedor: int
    id_servico: int
    observacoes: str
    preco: Optional[float] = None
    fornecedor: Optional[Fornecedor] = None
    servico: Optional[Servico] = None
