from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from util.validacoes_dto import (
    validar_cpf, validar_cnpj, validar_telefone, validar_data_nascimento,
    validar_nome_pessoa, converter_checkbox_para_bool, ValidacaoError
)


class PerfilFornecedorDTO(BaseModel):
    """DTO para dados do formulário de perfil do fornecedor"""

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

    # Tipos de fornecimento (checkboxes)
    prestador: bool = Field(False, description="Fornece serviços")
    vendedor: bool = Field(False, description="Fornece produtos")
    locador: bool = Field(False, description="Fornece espaços")

    # Preferências
    newsletter: bool = Field(False, description="Aceita receber newsletter")

    @validator('cpf')
    def validar_cpf_dto(cls, v):
        try:
            return validar_cpf(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('cnpj')
    def validar_cnpj_dto(cls, v):
        try:
            return validar_cnpj(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('telefone')
    def validar_telefone_dto(cls, v):
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('data_nascimento')
    def validar_data_nascimento_dto(cls, v):
        try:
            return validar_data_nascimento(v, idade_minima=16)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('prestador', 'vendedor', 'locador')
    def validar_pelo_menos_um_tipo(cls, v, values, field):
        # Esta validação será executada após todos os campos
        # Será feita uma validação final no método __init__ ou usando root_validator
        return v

    @validator('*', pre=True)
    def converter_checkboxes(cls, v, field):
        """Converter valores de checkbox vindos do form"""
        if field.name in ['prestador', 'vendedor', 'locador', 'newsletter']:
            return converter_checkbox_para_bool(v)
        return v

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao@empresa.com",
                "telefone": "(11) 99999-9999",
                "cpf": "123.456.789-01",
                "cnpj": "12.345.678/0001-90",
                "nome_empresa": "Empresa LTDA",
                "descricao": "Serviços de fotografia para casamentos",
                "prestador": True,
                "vendedor": False,
                "locador": False,
                "newsletter": True
            }
        }

    def __init__(self, **data):
        super().__init__(**data)

        # Validar que pelo menos um tipo de fornecimento foi selecionado
        if not (self.prestador or self.vendedor or self.locador):
            raise ValueError('Selecione pelo menos um tipo de fornecimento')