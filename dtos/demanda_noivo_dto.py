from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal


class DemandaNoivoDTO(BaseModel):
    """DTO para dados do formulário de demanda do noivo"""

    titulo: str = Field(..., min_length=5, max_length=100, description="Título da demanda")
    descricao: str = Field(..., min_length=20, max_length=2000, description="Descrição detalhada da demanda")
    orcamento_min: Optional[Decimal] = Field(None, ge=0, description="Orçamento mínimo (deve ser >= 0)")
    orcamento_max: Optional[Decimal] = Field(None, ge=0, description="Orçamento máximo (deve ser >= 0)")
    prazo_entrega: Optional[str] = Field(None, max_length=100, description="Prazo de entrega desejado")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")

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

    @validator('orcamento_min')
    def validar_orcamento_min(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError('Orçamento mínimo não pode ser negativo')

            # Verificar se tem no máximo 2 casas decimais
            if v != round(v, 2):
                raise ValueError('Orçamento deve ter no máximo 2 casas decimais')

            # Verificar se não é um valor absurdamente alto
            if v > 9999999.99:
                raise ValueError('Orçamento não pode ser superior a R$ 9.999.999,99')

        return v

    @validator('orcamento_max')
    def validar_orcamento_max(cls, v, values):
        if v is not None:
            if v < 0:
                raise ValueError('Orçamento máximo não pode ser negativo')

            # Verificar se tem no máximo 2 casas decimais
            if v != round(v, 2):
                raise ValueError('Orçamento deve ter no máximo 2 casas decimais')

            # Verificar se não é um valor absurdamente alto
            if v > 9999999.99:
                raise ValueError('Orçamento não pode ser superior a R$ 9.999.999,99')

            # Verificar se o orçamento máximo é maior que o mínimo
            if 'orcamento_min' in values and values['orcamento_min'] is not None:
                if v < values['orcamento_min']:
                    raise ValueError('Orçamento máximo deve ser maior ou igual ao mínimo')

        return v

    @validator('prazo_entrega')
    def validar_prazo_entrega(cls, v):
        if v is not None:
            # Remover espaços extras
            prazo = ' '.join(v.split()) if v.strip() else None

            if prazo and len(prazo) > 100:
                raise ValueError('Prazo de entrega deve ter no máximo 100 caracteres')

            return prazo
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

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        schema_extra = {
            "example": {
                "titulo": "Fotografia para casamento",
                "descricao": "Procuramos um fotógrafo para nosso casamento que será realizado no dia 15 de junho. Gostaríamos de cobertura completa da cerimônia e festa, com entrega de álbum digital.",
                "orcamento_min": 2000.00,
                "orcamento_max": 4000.00,
                "prazo_entrega": "30 dias após o evento",
                "observacoes": "Preferimos um estilo mais natural e espontâneo nas fotos"
            }
        }