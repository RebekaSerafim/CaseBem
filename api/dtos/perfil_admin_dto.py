from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Optional
from util.validacoes_dto import (
    validar_nome_pessoa, validar_telefone, validar_texto_opcional,
    validar_estado_brasileiro, ValidacaoError
)


class PerfilAdminDTO(BaseModel):
    """DTO para dados do formulário de perfil do administrador"""

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do administrador")
    email: EmailStr = Field(..., description="E-mail do administrador")
    telefone: Optional[str] = Field(None, description="Telefone do administrador")
    cargo: Optional[str] = Field(None, max_length=50, description="Cargo do administrador")
    endereco: Optional[str] = Field(None, max_length=200, description="Endereço completo")
    cidade: Optional[str] = Field(None, max_length=50, description="Cidade")
    estado: Optional[str] = Field(None, max_length=2, description="Estado (sigla UF)")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações sobre o administrador")

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v):
        try:
            return validar_nome_pessoa(v, min_chars=2, max_chars=100)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('telefone')
    @classmethod
    def validar_telefone_dto(cls, v):
        if not v:
            return v
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('cargo')
    @classmethod
    def validar_cargo_dto(cls, v):
        try:
            return validar_texto_opcional(v, max_chars=50)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('endereco')
    @classmethod
    def validar_endereco_dto(cls, v):
        try:
            return validar_texto_opcional(v, max_chars=200)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('cidade')
    @classmethod
    def validar_cidade_dto(cls, v):
        try:
            # Validar como nome de pessoa (apenas letras e espaços)
            if v:
                validar_nome_pessoa(v, min_chars=1, max_chars=50)
            return validar_texto_opcional(v, max_chars=50)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('estado')
    @classmethod
    def validar_estado_dto(cls, v):
        try:
            return validar_estado_brasileiro(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes_dto(cls, v):
        try:
            return validar_texto_opcional(v, max_chars=1000)
        except ValidacaoError as e:
            raise ValueError(str(e))

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra = {
            "example": {
                "nome": "Maria Silva",
                "email": "maria.admin@casebem.com",
                "telefone": "(11) 99999-9999",
                "cargo": "Gerente de Sistemas",
                "endereco": "Rua das Flores, 123 - Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "observacoes": "Responsável pela administração geral do sistema"
            }
        }    )

