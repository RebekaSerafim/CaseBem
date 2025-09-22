from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum


class TipoFornecimentoEnum(str, Enum):
    """Enum para tipos de fornecimento"""
    PRESTADOR = "PRESTADOR"
    VENDEDOR = "VENDEDOR"
    LOCADOR = "LOCADOR"


class CategoriaItemDTO(BaseModel):
    """DTO para dados do formulário de categoria de item"""

    nome: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    tipo_fornecimento: TipoFornecimentoEnum = Field(..., description="Tipo de fornecimento (PRESTADOR, VENDEDOR, LOCADOR)")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição da categoria")
    ativo: bool = Field(True, description="Categoria está ativa")

    @validator('nome')
    def validar_nome(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome da categoria é obrigatório')

        # Remover espaços extras
        nome = ' '.join(v.split())

        if len(nome) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')

        if len(nome) > 50:
            raise ValueError('Nome deve ter no máximo 50 caracteres')

        # Verificar se contém apenas letras, números, espaços e alguns caracteres especiais
        import re
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-&/]+$', nome):
            raise ValueError('Nome deve conter apenas letras, números, espaços, hífens e símbolos (&, /)')

        return nome

    @validator('tipo_fornecimento')
    def validar_tipo_fornecimento(cls, v):
        if isinstance(v, str):
            try:
                return TipoFornecimentoEnum(v.upper())
            except ValueError:
                tipos_validos = [tipo.value for tipo in TipoFornecimentoEnum]
                raise ValueError(f'Tipo de fornecimento deve ser uma das opções: {", ".join(tipos_validos)}')
        return v

    @validator('descricao')
    def validar_descricao(cls, v):
        if v is not None:
            # Remover espaços extras
            descricao = ' '.join(v.split()) if v.strip() else None

            if descricao and len(descricao) > 500:
                raise ValueError('Descrição deve ter no máximo 500 caracteres')

            return descricao
        return v

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "nome": "Fotografia",
                "tipo_fornecimento": "PRESTADOR",
                "descricao": "Serviços de fotografia para eventos e casamentos",
                "ativo": True
            }
        }