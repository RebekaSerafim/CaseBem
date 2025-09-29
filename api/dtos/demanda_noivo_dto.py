from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo
from typing import Optional
from decimal import Decimal
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_valor_monetario,
    ValidacaoError
)


class DemandaNoivoDTO(BaseModel):
    """DTO para dados do formulário de demanda do noivo"""

    titulo: str = Field(..., min_length=5, max_length=100, description="Título da demanda")
    descricao: str = Field(..., min_length=20, max_length=2000, description="Descrição detalhada da demanda")
    orcamento_min: Optional[Decimal] = Field(None, ge=0, description="Orçamento mínimo (deve ser >= 0)")
    orcamento_max: Optional[Decimal] = Field(None, ge=0, description="Orçamento máximo (deve ser >= 0)")
    prazo_entrega: Optional[str] = Field(None, max_length=100, description="Prazo de entrega desejado")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")

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

    @field_validator('orcamento_min')
    @classmethod
    def validar_orcamento_min_dto(cls, v):
        try:
            return validar_valor_monetario(v, "Orçamento mínimo", obrigatorio=False, min_valor=Decimal('0'))
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('orcamento_max')
    @classmethod
    def validar_orcamento_max_dto(cls, v, info: ValidationInfo):
        try:
            valor_validado = validar_valor_monetario(v, "Orçamento máximo", obrigatorio=False, min_valor=Decimal('0'))

            # Verificar se o orçamento máximo é maior que o mínimo
            if valor_validado is not None and 'orcamento_min' in info.data and info.data['orcamento_min'] is not None:
                if valor_validado < info.data['orcamento_min']:
                    raise ValidacaoError('Orçamento máximo deve ser maior ou igual ao mínimo')

            return valor_validado
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('prazo_entrega')
    @classmethod
    def validar_prazo_entrega_dto(cls, v):
        try:
            return validar_texto_opcional(v, max_chars=100)
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
                "titulo": "Fotografia para casamento",
                "descricao": "Procuramos um fotógrafo para nosso casamento que será realizado no dia 15 de junho. Gostaríamos de cobertura completa da cerimônia e festa, com entrega de álbum digital.",
                "orcamento_min": 2000.00,
                "orcamento_max": 4000.00,
                "prazo_entrega": "30 dias após o evento",
                "observacoes": "Preferimos um estilo mais natural e espontâneo nas fotos"
            }
        }    )

