from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TipoItem(Enum):
    PRODUTO = "PRODUTO"
    SERVICO = "SERVIÇO"
    ESPACO = "ESPAÇO"

@dataclass
class Item:
    id: int
    id_fornecedor: int
    tipo: TipoItem
    nome: str
    descricao: str
    preco: float
    id_categoria: int
    observacoes: Optional[str] = None
    ativo: bool = True
    data_cadastro: Optional[str] = None