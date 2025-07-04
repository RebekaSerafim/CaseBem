from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Chat:
    id_remetente: int
    id_destinatario: int
    mensagem: str
    data_hora_envio: datetime
    data_hora_leitura: Optional[datetime] = None
