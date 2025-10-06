from dataclasses import dataclass
from typing import Optional
from core.models.tipo_fornecimento_model import TipoFornecimento

@dataclass
class ItemDemanda:
    """
    Representa um item solicitado em uma demanda.

    IMPORTANTE: Este item NÃO está vinculado a um item específico do catálogo
    de fornecedores. É uma descrição livre do que o noivo deseja.

    O fornecedor vinculará seus itens do catálogo no ORÇAMENTO, não aqui.
    """
    id: int
    id_demanda: int
    tipo: TipoFornecimento  # PRODUTO, SERVICO ou ESPACO
    id_categoria: int  # Categoria do tipo de item desejado
    descricao: str  # Descrição livre do que o noivo quer
    quantidade: int
    preco_maximo: Optional[float] = None
    observacoes: Optional[str] = None

    def __post_init__(self):
        """Converte tipo de string para enum se necessário"""
        if isinstance(self.tipo, str):
            self.tipo = TipoFornecimento(self.tipo)