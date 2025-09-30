from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from core.models.tipo_fornecimento_model import TipoFornecimento

@dataclass
class Item:
    id: int
    id_fornecedor: int
    tipo: TipoFornecimento
    nome: str
    descricao: str
    preco: Decimal
    id_categoria: int
    observacoes: Optional[str] = None
    ativo: bool = True
    data_cadastro: Optional[str] = None