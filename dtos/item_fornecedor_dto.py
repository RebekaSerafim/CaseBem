from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from decimal import Decimal
from model.tipo_fornecimento_model import TipoFornecimento
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_valor_monetario,
    validar_numero_inteiro, validar_enum_valor, ValidacaoError
)


class ItemFornecedorDTO(BaseModel):
    """DTO para dados do formulário de item do fornecedor"""

    nome: str = Field(..., min_length=2, max_length=100, description="Nome do item")
    tipo: TipoFornecimento = Field(..., description="Tipo do item (PRODUTO, SERVIÇO, ESPAÇO)")
    descricao: str = Field(..., min_length=10, max_length=1000, description="Descrição detalhada do item")
    preco: Decimal = Field(..., ge=0, description="Preço do item (deve ser >= 0)")
    categoria_id: Optional[int] = Field(None, description="ID da categoria do item")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações adicionais")
    ativo: bool = Field(True, description="Item está ativo")

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v):
        try:
            return validar_texto_obrigatorio(v, "Nome do item", min_chars=2, max_chars=100)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('descricao')
    @classmethod
    def validar_descricao_dto(cls, v):
        try:
            return validar_texto_obrigatorio(v, "Descrição", min_chars=10, max_chars=1000)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('preco')
    @classmethod
    def validar_preco_dto(cls, v):
        try:
            return validar_valor_monetario(v, "Preço", obrigatorio=True)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('categoria_id')
    @classmethod
    def validar_categoria_dto(cls, v):
        if v is None:
            return v
        try:
            return validar_numero_inteiro(v, "ID da categoria", obrigatorio=False, min_valor=1)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes_dto(cls, v):
        try:
            return validar_texto_opcional(v, max_chars=500)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v):
        try:
            return validar_enum_valor(v, TipoFornecimento, "Tipo do item")
        except ValidacaoError as e:
            raise ValueError(str(e))

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        json_schema_extra = {
            "example": {
                "nome": "Fotografia de Casamento",
                "tipo": "SERVIÇO",
                "descricao": "Cobertura fotográfica completa do casamento, incluindo cerimônia e festa",
                "preco": 2500.00,
                "categoria_id": 1,
                "observacoes": "Inclui álbum digital com 200 fotos tratadas",
                "ativo": True
            }
        }
    )