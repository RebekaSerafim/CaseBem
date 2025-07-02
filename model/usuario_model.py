from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nome: str
    telefone: str
    email: str    
    senha_hash: str
    tipo: str
    