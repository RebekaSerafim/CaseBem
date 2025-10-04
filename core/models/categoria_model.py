from dataclasses import dataclass
from typing import Optional
from core.models.tipo_fornecimento_model import TipoFornecimento

@dataclass
class Categoria:
    id: int
    nome: str
    tipo_fornecimento: TipoFornecimento
    descricao: Optional[str] = None
    ativo: bool = True