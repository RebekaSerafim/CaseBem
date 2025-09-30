"""
DTOs relacionados a categorias.
Agrupa todas as validações e estruturas de dados para operações com categorias.
"""

from pydantic import Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from core.models.tipo_fornecimento_model import TipoFornecimento
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_enum_valor,
    ValidadorWrapper
)
import re


class CategoriaDTO(BaseDTO):
    """
    DTO para operações com categorias (criar/editar).
    Usado em formulários de administração de categorias.
    """

    nome: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    tipo_fornecimento: TipoFornecimento = Field(..., description="Tipo de fornecimento (PRODUTO, SERVIÇO, ESPAÇO)")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição da categoria")
    ativo: bool = Field(True, description="Categoria está ativa")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        # Usar o wrapper da BaseDTO para tratamento de erros
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2, max_chars=50),
            "Nome da categoria"
        )
        nome = validador(v)

        # Validação específica de categoria - apenas letras, números e alguns símbolos
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-&/]+$', nome):
            raise ValueError('Nome deve conter apenas letras, números, espaços, hífens e símbolos (&, /)')

        return nome

    @field_validator('tipo_fornecimento')
    @classmethod
    def validar_tipo(cls, v):
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_enum_valor(valor, TipoFornecimento, campo),
            "Tipo de fornecimento"
        )
        return validador(v)

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Descrição"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "Fotografia",
            "tipo_fornecimento": "SERVIÇO",
            "descricao": "Serviços profissionais de fotografia para casamentos e eventos",
            "ativo": True
        }
        exemplo.update(overrides)
        return exemplo


class CategoriaListaDTO(BaseDTO):
    """
    DTO para filtros de listagem de categorias.
    Usado em consultas com filtros opcionais.
    """

    tipo_fornecimento: Optional[TipoFornecimento] = Field(None, description="Filtrar por tipo de fornecimento")
    ativo: Optional[bool] = Field(None, description="Filtrar por status ativo/inativo")
    nome_busca: Optional[str] = Field(None, max_length=50, description="Buscar no nome da categoria")

    @field_validator('nome_busca')
    @classmethod
    def validar_busca(cls, v: Optional[str]) -> Optional[str]:
        if v is None or not v.strip():
            return None
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=50),
            "Busca"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de filtros para documentação"""
        exemplo = {
            "tipo_fornecimento": "SERVIÇO",
            "ativo": True,
            "nome_busca": "foto"
        }
        exemplo.update(overrides)
        return exemplo


# Configurar exemplos JSON nos model_config
CategoriaDTO.model_config.update({
    "json_schema_extra": {
        "example": CategoriaDTO.criar_exemplo_json()
    }
})

CategoriaListaDTO.model_config.update({
    "json_schema_extra": {
        "example": CategoriaListaDTO.criar_exemplo_json()
    }
})