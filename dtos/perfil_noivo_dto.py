from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from enum import Enum
from util.validacoes_dto import (
    validar_cpf, validar_telefone, validar_data_nascimento,
    validar_nome_pessoa, validar_enum_valor, ValidacaoError
)


class GeneroEnum(str, Enum):
    """Enum para gêneros"""
    MASCULINO = "MASCULINO"
    FEMININO = "FEMININO"
    OUTROS = "OUTROS"
    NAO_INFORMAR = "NAO_INFORMAR"


class PerfilNoivoDTO(BaseModel):
    """DTO para dados do formulário de perfil do noivo"""

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do noivo")
    email: EmailStr = Field(..., description="E-mail do noivo")
    telefone: str = Field(..., min_length=10, description="Telefone do noivo")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    cpf: Optional[str] = Field(None, description="CPF do noivo")
    genero: Optional[GeneroEnum] = Field(None, description="Gênero do noivo")

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
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('data_nascimento')
    def validar_data_nascimento_dto(cls, v):
        try:
            return validar_data_nascimento(v, idade_minima=16)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('genero')
    def validar_genero_dto(cls, v):
        if v is None:
            return v
        try:
            return validar_enum_valor(v, GeneroEnum, "Gênero")
        except ValidacaoError as e:
            raise ValueError(str(e))

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao@email.com",
                "telefone": "(11) 99999-9999",
                "data_nascimento": "1990-05-15",
                "cpf": "123.456.789-01",
                "genero": "MASCULINO"
            }
        }