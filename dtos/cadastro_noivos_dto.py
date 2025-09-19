from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional


class CadastroNoivosDTO(BaseModel):
    """DTO para dados do formulário de cadastro de noivos"""

    # Dados do casamento
    data_casamento: Optional[str] = None
    local_previsto: Optional[str] = None
    orcamento_estimado: Optional[str] = None
    numero_convidados: Optional[str] = None

    # Dados do primeiro noivo
    nome1: str = Field(..., min_length=2, description="Nome completo do primeiro noivo")
    data_nascimento1: Optional[str] = None
    cpf1: Optional[str] = None
    email1: EmailStr = Field(..., description="E-mail do primeiro noivo")
    telefone1: str = Field(..., min_length=10, description="Telefone do primeiro noivo")
    genero1: Optional[str] = None

    # Dados do segundo noivo
    nome2: str = Field(..., min_length=2, description="Nome completo do segundo noivo")
    data_nascimento2: Optional[str] = None
    cpf2: Optional[str] = None
    email2: EmailStr = Field(..., description="E-mail do segundo noivo")
    telefone2: str = Field(..., min_length=10, description="Telefone do segundo noivo")
    genero2: Optional[str] = None

    # Dados de acesso
    senha: str = Field(..., min_length=8, description="Senha deve ter pelo menos 8 caracteres")
    confirmar_senha: str = Field(..., description="Confirmação da senha")

    # Outros
    newsletter: Optional[str] = None

    @validator('confirmar_senha')
    def senhas_devem_coincidir(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('As senhas não coincidem')
        return v

    @validator('email2')
    def emails_devem_ser_diferentes(cls, v, values):
        if 'email1' in values and v == values['email1']:
            raise ValueError('Os e-mails dos noivos devem ser diferentes')
        return v

    class Config:
        # Permite que o modelo aceite dados de formulário HTML
        str_strip_whitespace = True