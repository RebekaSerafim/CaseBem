from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from core.models.demanda_model import Demanda
from core.models.usuario_model import Usuario

@dataclass
class Orcamento:
    id: int
    id_demanda: int
    id_fornecedor_prestador: int
    data_hora_cadastro: datetime
    data_hora_validade: Optional[datetime] = None
    status: str = "PENDENTE"  # PENDENTE, ACEITO, REJEITADO
    observacoes: Optional[str] = None
    valor_total: Optional[float] = None
    demanda: Optional[Demanda] = None
    fornecedor_prestador: Optional[Usuario] = None
    # Campos para enriquecimento de dados na listagem
    itens_count: Optional[int] = None
    data_envio: Optional[str] = None
    demanda_titulo: Optional[str] = None
    total_itens: Optional[int] = None
    itens: Optional[list] = None