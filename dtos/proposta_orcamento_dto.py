from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal
from enum import Enum


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

    @validator('titulo')
    def validar_titulo(cls, v):
        if not v or not v.strip():
            raise ValueError('Título é obrigatório')

        # Remover espaços extras
        titulo = ' '.join(v.split())

        if len(titulo) < 5:
            raise ValueError('Título deve ter pelo menos 5 caracteres')

        if len(titulo) > 100:
            raise ValueError('Título deve ter no máximo 100 caracteres')

        return titulo

    @validator('descricao')
    def validar_descricao(cls, v):
        if not v or not v.strip():
            raise ValueError('Descrição é obrigatória')

        # Remover espaços extras
        descricao = ' '.join(v.split())

        if len(descricao) < 20:
            raise ValueError('Descrição deve ter pelo menos 20 caracteres')

        if len(descricao) > 2000:
            raise ValueError('Descrição deve ter no máximo 2000 caracteres')

        return descricao

    @validator('valor_total')
    def validar_valor_total(cls, v):
        if v is None:
            raise ValueError('Valor total é obrigatório')

        if v <= 0:
            raise ValueError('Valor total deve ser maior que zero')

        # Verificar se tem no máximo 2 casas decimais
        if v != round(v, 2):
            raise ValueError('Valor deve ter no máximo 2 casas decimais')

        # Verificar se não é um valor absurdamente alto
        if v > 9999999.99:
            raise ValueError('Valor não pode ser superior a R$ 9.999.999,99')

        return v

    @validator('prazo_entrega')
    def validar_prazo_entrega(cls, v):
        if v is None:
            raise ValueError('Prazo de entrega é obrigatório')

        if v < 1:
            raise ValueError('Prazo de entrega deve ser de pelo menos 1 dia')

        if v > 365:
            raise ValueError('Prazo de entrega não pode ser superior a 365 dias')

        return v

    @validator('observacoes')
    def validar_observacoes(cls, v):
        if v is not None:
            # Remover espaços extras
            observacoes = ' '.join(v.split()) if v.strip() else None

            if observacoes and len(observacoes) > 1000:
                raise ValueError('Observações devem ter no máximo 1000 caracteres')

            return observacoes
        return v

    @validator('forma_pagamento')
    def validar_forma_pagamento(cls, v):
        if v is not None and isinstance(v, str):
            try:
                return FormaPagamentoEnum(v.upper())
            except ValueError:
                formas_validas = [forma.value for forma in FormaPagamentoEnum]
                raise ValueError(f'Forma de pagamento deve ser uma das opções: {", ".join(formas_validas)}')
        return v

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "titulo": "Cobertura Fotográfica Premium",
                "descricao": "Proposta para cobertura fotográfica completa do casamento, incluindo pré-wedding, cerimônia e festa. Entrega de álbum digital com 300 fotos tratadas e álbum físico de 50 páginas.",
                "valor_total": 3500.00,
                "prazo_entrega": 30,
                "observacoes": "Inclui sessão de pré-wedding em local à escolha dos noivos",
                "forma_pagamento": "PARCELADO"
            }
        }