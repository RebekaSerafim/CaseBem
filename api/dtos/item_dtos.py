"""
DTOs relacionados a itens e fornecedores.
Agrupa todas as validações e estruturas de dados para operações com itens e fornecedores.
"""

from pydantic import EmailStr, Field, field_validator, ValidationInfo, model_validator
from typing import Optional, Any
from decimal import Decimal
from .base_dto import BaseDTO
from model.tipo_fornecimento_model import TipoFornecimento
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional, validar_valor_monetario,
    validar_numero_inteiro, validar_enum_valor, validar_cpf, validar_cnpj,
    validar_telefone, validar_data_nascimento, validar_nome_pessoa,
    validar_senha, validar_senhas_coincidem, converter_checkbox_para_bool
)


class ItemFornecedorDTO(BaseDTO):
    """
    DTO para formulário de item do fornecedor.
    Usado por fornecedores para criar/editar seus itens.
    """

    nome: str = Field(..., min_length=2, max_length=100, description="Nome do item")
    tipo: TipoFornecimento = Field(..., description="Tipo do item (PRODUTO, SERVIÇO, ESPAÇO)")
    descricao: str = Field(..., min_length=10, max_length=1000, description="Descrição detalhada do item")
    preco: Decimal = Field(..., ge=0, description="Preço do item (deve ser >= 0)")
    categoria_id: Optional[int] = Field(None, description="ID da categoria do item")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações adicionais")
    ativo: bool = Field(True, description="Item está ativo")

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2, max_chars=100),
            "Nome do item"
        )
        return validador(v)

    @field_validator('descricao')
    @classmethod
    def validar_descricao_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=10, max_chars=1000),
            "Descrição"
        )
        return validador(v)

    @field_validator('preco')
    @classmethod
    def validar_preco_dto(cls, v: Decimal) -> Decimal:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_valor_monetario(valor, campo, obrigatorio=True),
            "Preço"
        )
        return validador(v)

    @field_validator('categoria_id')
    @classmethod
    def validar_categoria_dto(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_numero_inteiro(valor, campo, obrigatorio=False, min_valor=1),
            "ID da categoria"
        )
        return validador(v)

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Observações"
        )
        return validador(v)

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v: TipoFornecimento) -> TipoFornecimento:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_enum_valor(valor, TipoFornecimento, campo),
            "Tipo do item"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "Fotografia de Casamento",
            "tipo": "SERVIÇO",
            "descricao": "Cobertura fotográfica completa do casamento, incluindo cerimônia e festa",
            "preco": 2500.00,
            "categoria_id": 1,
            "observacoes": "Inclui álbum digital com 200 fotos tratadas",
            "ativo": True
        }
        exemplo.update(overrides)
        return exemplo


class CadastroFornecedorDTO(BaseDTO):
    """
    DTO para formulário de cadastro de fornecedor.
    Usado para registro de novos fornecedores no sistema.
    """

    # Dados pessoais
    nome: str = Field(..., min_length=2, description="Nome completo do fornecedor")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    cpf: Optional[str] = Field(None, description="CPF do fornecedor")

    # Dados do negócio
    nome_empresa: Optional[str] = Field(None, max_length=100, description="Nome da empresa/negócio")
    cnpj: Optional[str] = Field(None, description="CNPJ da empresa")
    descricao: Optional[str] = Field(None, max_length=1000, description="Descrição dos serviços/produtos")

    # Dados de contato
    email: EmailStr = Field(..., description="E-mail do fornecedor")
    telefone: str = Field(..., min_length=10, description="Telefone do fornecedor")

    # Dados de acesso
    senha: str = Field(..., min_length=8, description="Senha deve ter pelo menos 8 caracteres")
    confirmar_senha: str = Field(..., description="Confirmação da senha")

    # Outros
    newsletter: Optional[str] = Field(None, description="Aceita receber newsletter")

    @model_validator(mode='before')
    @classmethod
    def converter_checkboxes(cls, data: Any) -> Any:
        """Converter valores de checkbox vindos do form"""
        if isinstance(data, dict):
            if 'newsletter' in data:
                data['newsletter'] = converter_checkbox_para_bool(data['newsletter'])
        return data

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor),
            "Nome do fornecedor"
        )
        return validador(v)

    @field_validator('cpf')
    @classmethod
    def validar_cpf_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF"
        )
        return validador(v)

    @field_validator('cnpj')
    @classmethod
    def validar_cnpj_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cnpj(valor),
            "CNPJ"
        )
        return validador(v)

    @field_validator('nome_empresa')
    @classmethod
    def validar_nome_empresa_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Nome da empresa"
        )
        return validador(v)

    @field_validator('descricao')
    @classmethod
    def validar_descricao_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=1000),
            "Descrição"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_data_nascimento(valor, idade_minima=16),
            "Data de nascimento"
        )
        return validador(v)

    @field_validator('senha')
    @classmethod
    def validar_senha_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=8, obrigatorio=True),
            "Senha"
        )
        return validador(v)

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v: str, info: ValidationInfo) -> str:
        if 'senha' in info.data:
            validador = cls.validar_campo_wrapper(
                lambda valor, campo: validar_senhas_coincidem(info.data['senha'], valor),
                "Confirmação de senha"
            )
            return validador(v)
        return v

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "data_nascimento": "1985-03-15",
            "cpf": "123.456.789-01",
            "nome_empresa": "Silva Fotografia LTDA",
            "cnpj": "12.345.678/0001-90",
            "descricao": "Serviços profissionais de fotografia para casamentos e eventos",
            "email": "joao@silvafotografia.com",
            "telefone": "(11) 99999-9999",
            "senha": "senhaSegura123",
            "confirmar_senha": "senhaSegura123",
            "newsletter": True
        }
        exemplo.update(overrides)
        return exemplo


class PerfilFornecedorDTO(BaseDTO):
    """
    DTO para formulário de perfil do fornecedor.
    Usado para editar informações pessoais do fornecedor logado.
    """

    # Dados pessoais
    nome: str = Field(..., min_length=2, description="Nome completo do fornecedor")
    email: EmailStr = Field(..., description="E-mail do fornecedor")
    telefone: str = Field(..., min_length=10, description="Telefone do fornecedor")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    cpf: Optional[str] = Field(None, description="CPF do fornecedor")

    # Dados do negócio
    nome_empresa: Optional[str] = Field(None, description="Nome da empresa/negócio")
    cnpj: Optional[str] = Field(None, description="CNPJ da empresa")
    descricao: Optional[str] = Field(None, description="Descrição dos serviços/produtos/espaços")

    # Preferências
    newsletter: bool = Field(False, description="Aceita receber newsletter")

    @model_validator(mode='before')
    @classmethod
    def converter_checkboxes(cls, data: Any) -> Any:
        """Converter valores de checkbox vindos do form"""
        if isinstance(data, dict):
            if 'newsletter' in data:
                data['newsletter'] = converter_checkbox_para_bool(data['newsletter'])
        return data

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor),
            "Nome do fornecedor"
        )
        return validador(v)

    @field_validator('cpf')
    @classmethod
    def validar_cpf_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF"
        )
        return validador(v)

    @field_validator('cnpj')
    @classmethod
    def validar_cnpj_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cnpj(valor),
            "CNPJ"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_data_nascimento(valor, idade_minima=16),
            "Data de nascimento"
        )
        return validador(v)

    @field_validator('descricao')
    @classmethod
    def validar_descricao_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=1000),
            "Descrição"
        )
        return validador(v)

    @field_validator('nome_empresa')
    @classmethod
    def validar_nome_empresa_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Nome da empresa"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "email": "joao@empresa.com",
            "telefone": "(11) 99999-9999",
            "cpf": "123.456.789-01",
            "cnpj": "12.345.678/0001-90",
            "nome_empresa": "Empresa LTDA",
            "descricao": "Serviços de fotografia para casamentos",
            "newsletter": True
        }
        exemplo.update(overrides)
        return exemplo


# Configurar exemplos JSON nos model_config
ItemFornecedorDTO.model_config.update({
    "json_schema_extra": {
        "example": ItemFornecedorDTO.criar_exemplo_json()
    }
})

CadastroFornecedorDTO.model_config.update({
    "json_schema_extra": {
        "example": CadastroFornecedorDTO.criar_exemplo_json()
    }
})

PerfilFornecedorDTO.model_config.update({
    "json_schema_extra": {
        "example": PerfilFornecedorDTO.criar_exemplo_json()
    }
})