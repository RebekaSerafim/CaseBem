from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from enum import Enum
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_enum_valor,
    ValidacaoError
)
import re


class TipoFornecimentoEnum(str, Enum):
    """Enum para tipos de fornecimento"""
    PRESTADOR = "PRESTADOR"
    VENDEDOR = "VENDEDOR"
    LOCADOR = "LOCADOR"


class CategoriaDTO(BaseModel):
    """DTO para dados do formulário de categoria"""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "nome": "Fotografia",
                "tipo_fornecimento": "PRESTADOR",
                "descricao": "Serviços de fotografia para eventos e casamentos",
                "ativo": True
            }
        }
    )

    nome: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    tipo_fornecimento: TipoFornecimentoEnum = Field(..., description="Tipo de fornecimento (PRESTADOR, VENDEDOR, LOCADOR)")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição da categoria")
    ativo: bool = Field(True, description="Categoria está ativa")

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        try:
            nome = validar_texto_obrigatorio(v, "Nome da categoria", min_chars=2, max_chars=50)

            # Verificar se contém apenas letras, números, espaços e alguns caracteres especiais
            if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-&/]+$', nome):
                raise ValidacaoError('Nome deve conter apenas letras, números, espaços, hífens e símbolos (&, /)')

            return nome
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('tipo_fornecimento')
    @classmethod
    def validar_tipo_fornecimento_dto(cls, v):
        try:
            return validar_enum_valor(v, TipoFornecimentoEnum, "Tipo de fornecimento")
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('descricao')
    @classmethod
    def validar_descricao_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_texto_opcional(v, max_chars=500)
        except ValidacaoError as e:
            raise ValueError(str(e))