from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from util.validacoes_dto import (
    validar_cpf, validar_telefone, validar_data_nascimento,
    validar_nome_pessoa, validar_senha, ValidacaoError
)


class AdminUsuarioDTO(BaseModel):
    """DTO para dados do formulário de criação/edição de usuário administrador"""

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do administrador")
    email: EmailStr = Field(..., description="E-mail do administrador")
    cpf: Optional[str] = Field(None, description="CPF do administrador")
    telefone: Optional[str] = Field(None, description="Telefone do administrador")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    senha: Optional[str] = Field(None, min_length=6, description="Senha (obrigatória apenas na criação)")

    @validator('nome')
    def validar_nome_dto(cls, v):
        try:
            return validar_nome_pessoa(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('cpf')
    def validar_cpf_dto(cls, v):
        try:
            return validar_cpf(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('telefone')
    def validar_telefone_dto(cls, v):
        if not v:
            return v
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('data_nascimento')
    def validar_data_nascimento_dto(cls, v):
        try:
            return validar_data_nascimento(v, idade_minima=18)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('senha')
    def validar_senha_dto(cls, v):
        try:
            return validar_senha(v, obrigatorio=False)
        except ValidacaoError as e:
            raise ValueError(str(e))

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        schema_extra = {
            "example": {
                "nome": "Carlos Santos",
                "email": "carlos.admin@casebem.com",
                "cpf": "123.456.789-01",
                "telefone": "(11) 99999-9999",
                "data_nascimento": "1985-03-15",
                "senha": "senhaSegura123"
            }
        }