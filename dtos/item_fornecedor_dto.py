from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal
from enum import Enum
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_valor_monetario,
    validar_numero_inteiro, validar_enum_valor, ValidacaoError
)


class TipoItemEnum(str, Enum):
    """Enum para tipos de item"""
    PRODUTO = "PRODUTO"
    SERVICO = "SERVICO"
    ESPACO = "ESPACO"


class ItemFornecedorDTO(BaseModel):
    """DTO para dados do formulário de item do fornecedor"""

    nome: str = Field(..., min_length=2, max_length=100, description="Nome do item")
    tipo: TipoItemEnum = Field(..., description="Tipo do item (PRODUTO, SERVICO, ESPACO)")
    descricao: str = Field(..., min_length=10, max_length=1000, description="Descrição detalhada do item")
    preco: Decimal = Field(..., ge=0, description="Preço do item (deve ser >= 0)")
    categoria_id: Optional[int] = Field(None, description="ID da categoria do item")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações adicionais")
    ativo: bool = Field(True, description="Item está ativo")

    @validator('nome')
    def validar_nome_dto(cls, v):
        try:
            return validar_texto_obrigatorio(v, "Nome do item", min_chars=2, max_chars=100)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('descricao')
    def validar_descricao_dto(cls, v):
        try:
            return validar_texto_obrigatorio(v, "Descrição", min_chars=10, max_chars=1000)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('preco')
    def validar_preco_dto(cls, v):
        try:
            return validar_valor_monetario(v, "Preço", obrigatorio=True)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('categoria_id')
    def validar_categoria_dto(cls, v):
        if v is None:
            return v
        try:
            return validar_numero_inteiro(v, "ID da categoria", obrigatorio=False, min_valor=1)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('observacoes')
    def validar_observacoes_dto(cls, v):
        try:
            return validar_texto_opcional(v, max_chars=500)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('tipo')
    def validar_tipo_dto(cls, v):
        try:
            return validar_enum_valor(v, TipoItemEnum, "Tipo do item")
        except ValidacaoError as e:
            raise ValueError(str(e))

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "nome": "Fotografia de Casamento",
                "tipo": "SERVICO",
                "descricao": "Cobertura fotográfica completa do casamento, incluindo cerimônia e festa",
                "preco": 2500.00,
                "categoria_id": 1,
                "observacoes": "Inclui álbum digital com 200 fotos tratadas",
                "ativo": True
            }
        }