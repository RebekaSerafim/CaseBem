from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from decimal import Decimal
from enum import Enum
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_valor_monetario,
    validar_numero_inteiro, validar_enum_valor, ValidacaoError
)


class FormaPagamentoEnum(str, Enum):
    """Enum para formas de pagamento"""
    A_VISTA = "A_VISTA"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    PIX = "PIX"
    TRANSFERENCIA = "TRANSFERENCIA"
    BOLETO = "BOLETO"
    PARCELADO = "PARCELADO"


class PropostaOrcamentoDTO(BaseModel):
    """DTO para dados do formulário de proposta de orçamento"""

    titulo: str = Field(..., min_length=5, max_length=100, description="Título da proposta")
    descricao: str = Field(..., min_length=20, max_length=2000, description="Descrição detalhada da proposta")
    valor_total: Decimal = Field(..., gt=0, description="Valor total da proposta (deve ser > 0)")
    prazo_entrega: int = Field(..., ge=1, description="Prazo de entrega em dias (mínimo 1)")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")
    forma_pagamento: Optional[FormaPagamentoEnum] = Field(None, description="Forma de pagamento preferencial")

    @field_validator('titulo')
    @classmethod
    def validar_titulo_dto(cls, v):
        try:
            return validar_texto_obrigatorio(v, "Título", min_chars=5, max_chars=100)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('descricao')
    @classmethod
    def validar_descricao_dto(cls, v):
        try:
            return validar_texto_obrigatorio(v, "Descrição", min_chars=20, max_chars=2000)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('valor_total')
    @classmethod
    def validar_valor_total_dto(cls, v):
        try:
            return validar_valor_monetario(v, "Valor total", obrigatorio=True, min_valor=Decimal('0.01'))
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('prazo_entrega')
    @classmethod
    def validar_prazo_entrega_dto(cls, v):
        try:
            return validar_numero_inteiro(v, "Prazo de entrega", obrigatorio=True, min_valor=1, max_valor=365)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes_dto(cls, v):
        try:
            return validar_texto_opcional(v, max_chars=1000)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('forma_pagamento')
    @classmethod
    def validar_forma_pagamento_dto(cls, v):
        if v is None:
            return v
        try:
            return validar_enum_valor(v, FormaPagamentoEnum, "Forma de pagamento")
        except ValidacaoError as e:
            raise ValueError(str(e))

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        json_schema_extra = {
            "example": {
                "titulo": "Cobertura Fotográfica Premium",
                "descricao": "Proposta para cobertura fotográfica completa do casamento, incluindo pré-wedding, cerimônia e festa. Entrega de álbum digital com 300 fotos tratadas e álbum físico de 50 páginas.",
                "valor_total": 3500.00,
                "prazo_entrega": 30,
                "observacoes": "Inclui sessão de pré-wedding em local à escolha dos noivos",
                "forma_pagamento": "PARCELADO"
            }
        }    )

