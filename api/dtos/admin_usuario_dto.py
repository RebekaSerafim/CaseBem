from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
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

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        try:
            return validar_nome_pessoa(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('cpf')
    @classmethod
    def validar_cpf_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_cpf(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('telefone')
    @classmethod
    def validar_telefone_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_data_nascimento(v, idade_minima=18)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('senha')
    @classmethod
    def validar_senha_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_senha(v, obrigatorio=False)
        except ValidacaoError as e:
            raise ValueError(str(e))

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "nome": "Carlos Santos",
                "email": "carlos.admin@casebem.com",
                "cpf": "123.456.789-01",
                "telefone": "(11) 99999-9999",
                "data_nascimento": "1985-03-15",
                "senha": "senhaSegura123"
            }
        }
    )