"""
DTOs relacionados a demandas e orçamentos.
Agrupa todas as validações e estruturas de dados para operações com demandas e propostas de orçamento.
"""

from pydantic import Field, field_validator, ValidationInfo
from typing import Optional
from decimal import Decimal
from enum import Enum
from .base_dto import BaseDTO
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


class DemandaNoivoDTO(BaseDTO):
    """
    DTO para formulário de demanda do noivo.
    Usado pelos noivos para criar solicitações de produtos/serviços.
    """

    titulo: str = Field(..., min_length=5, max_length=100, description="Título da demanda")
    descricao: str = Field(..., min_length=20, max_length=2000, description="Descrição detalhada da demanda")
    orcamento_min: Optional[Decimal] = Field(None, ge=0, description="Orçamento mínimo (deve ser >= 0)")
    orcamento_max: Optional[Decimal] = Field(None, ge=0, description="Orçamento máximo (deve ser >= 0)")
    prazo_entrega: Optional[str] = Field(None, max_length=100, description="Prazo de entrega desejado")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")

    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=5, max_chars=100),
            "Título"
        )
        return validador(v)

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=20, max_chars=2000),
            "Descrição"
        )
        return validador(v)

    @field_validator('orcamento_min')
    @classmethod
    def validar_orcamento_min(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is None:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_valor_monetario(valor, campo, obrigatorio=False, min_valor=Decimal('0')),
            "Orçamento mínimo"
        )
        return validador(v)

    @field_validator('orcamento_max')
    @classmethod
    def validar_orcamento_max(cls, v: Optional[Decimal], info: ValidationInfo) -> Optional[Decimal]:
        if v is None:
            return v

        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_valor_monetario(valor, campo, obrigatorio=False, min_valor=Decimal('0')),
            "Orçamento máximo"
        )
        valor_validado = validador(v)

        # Verificar se o orçamento máximo é maior que o mínimo
        if valor_validado is not None and 'orcamento_min' in info.data and info.data['orcamento_min'] is not None:
            if valor_validado < info.data['orcamento_min']:
                raise ValueError('Orçamento máximo deve ser maior ou igual ao mínimo')

        return valor_validado

    @field_validator('prazo_entrega')
    @classmethod
    def validar_prazo_entrega(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Prazo de entrega"
        )
        return validador(v)

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=1000),
            "Observações"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "titulo": "Fotografia para casamento",
            "descricao": "Procuramos um fotógrafo para nosso casamento que será realizado no dia 15 de junho. Gostaríamos de cobertura completa da cerimônia e festa, com entrega de álbum digital.",
            "orcamento_min": 2000.00,
            "orcamento_max": 4000.00,
            "prazo_entrega": "30 dias após o evento",
            "observacoes": "Preferimos um estilo mais natural e espontâneo nas fotos"
        }
        exemplo.update(overrides)
        return exemplo


class PropostaOrcamentoDTO(BaseDTO):
    """
    DTO para formulário de proposta de orçamento.
    Usado pelos fornecedores para enviar propostas aos noivos.
    """

    titulo: str = Field(..., min_length=5, max_length=100, description="Título da proposta")
    descricao: str = Field(..., min_length=20, max_length=2000, description="Descrição detalhada da proposta")
    valor_total: Decimal = Field(..., gt=0, description="Valor total da proposta (deve ser > 0)")
    prazo_entrega: int = Field(..., ge=1, description="Prazo de entrega em dias (mínimo 1)")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")
    forma_pagamento: Optional[FormaPagamentoEnum] = Field(None, description="Forma de pagamento preferencial")

    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=5, max_chars=100),
            "Título"
        )
        return validador(v)

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=20, max_chars=2000),
            "Descrição"
        )
        return validador(v)

    @field_validator('valor_total')
    @classmethod
    def validar_valor_total(cls, v: Decimal) -> Decimal:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_valor_monetario(valor, campo, obrigatorio=True, min_valor=Decimal('0.01')),
            "Valor total"
        )
        return validador(v)

    @field_validator('prazo_entrega')
    @classmethod
    def validar_prazo_entrega(cls, v: int) -> int:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_numero_inteiro(valor, campo, obrigatorio=True, min_valor=1, max_valor=365),
            "Prazo de entrega"
        )
        return validador(v)

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=1000),
            "Observações"
        )
        return validador(v)

    @field_validator('forma_pagamento')
    @classmethod
    def validar_forma_pagamento(cls, v: Optional[FormaPagamentoEnum]) -> Optional[FormaPagamentoEnum]:
        if v is None:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_enum_valor(valor, FormaPagamentoEnum, campo),
            "Forma de pagamento"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "titulo": "Cobertura Fotográfica Premium",
            "descricao": "Proposta para cobertura fotográfica completa do casamento, incluindo pré-wedding, cerimônia e festa. Entrega de álbum digital com 300 fotos tratadas e álbum físico de 50 páginas.",
            "valor_total": 3500.00,
            "prazo_entrega": 30,
            "observacoes": "Inclui sessão de pré-wedding em local à escolha dos noivos",
            "forma_pagamento": "PARCELADO"
        }
        exemplo.update(overrides)
        return exemplo


# Configurar exemplos JSON nos model_config
DemandaNoivoDTO.model_config.update({
    "json_schema_extra": {
        "example": DemandaNoivoDTO.criar_exemplo_json()
    }
})

PropostaOrcamentoDTO.model_config.update({
    "json_schema_extra": {
        "example": PropostaOrcamentoDTO.criar_exemplo_json()
    }
})