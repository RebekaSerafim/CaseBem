from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from core.models.usuario_model import Usuario

@dataclass
class Chat:    
    id_remetente: int
    id_destinatario: int
    data_hora_envio: datetime
    mensagem: str
    data_hora_leitura: Optional[datetime] = None
    remetente: Optional[Usuario] = None
    destinatario: Optional[Usuario] = None
