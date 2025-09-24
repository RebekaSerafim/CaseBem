from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ConfigDict
from typing import Optional, Any, Dict
from util.validacoes_dto import (
    validar_cpf, validar_cnpj, validar_telefone, validar_data_nascimento,
    validar_nome_pessoa, converter_checkbox_para_bool, ValidacaoError
)


class PerfilFornecedorDTO(BaseModel):
    """DTO para dados do formulário de perfil do fornecedor"""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "nome": "João Silva",
                "email": "joao@empresa.com",
                "telefone": "(11) 99999-9999",
                "cpf": "123.456.789-01",
                "cnpj": "12.345.678/0001-90",
                "nome_empresa": "Empresa LTDA",
                "descricao": "Serviços de fotografia para casamentos",
                "newsletter": True
            }
        }
    )

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

    @field_validator('cpf')
    @classmethod
    def validar_cpf_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_cpf(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('cnpj')
    @classmethod
    def validar_cnpj_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_cnpj(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('telefone')
    @classmethod
    def validar_telefone_dto(cls, v: str) -> str:
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_data_nascimento(v, idade_minima=16)
        except ValidacaoError as e:
            raise ValueError(str(e))