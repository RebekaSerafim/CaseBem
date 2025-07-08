from dataclasses import dataclass
from datetime import datetime

@dataclass
class Demanda:
    id: int
    id_casal: int
    data_hora_cadastro: datetime    
    