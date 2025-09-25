from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo, Field, ConfigDict, model_validator
from typing import Optional, List, Any
from util.validacoes_dto import (
    validar_nome_pessoa, validar_cpf, validar_cnpj, validar_telefone, validar_data_nascimento,
    validar_senha, validar_senhas_coincidem, validar_texto_opcional, converter_checkbox_para_bool,
    ValidacaoError
)


class CadastroFornecedorDTO(BaseModel):
    """DTO para dados do formulário de cadastro de fornecedor"""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    # Dados pessoais
    nome: str = Field(..., min_length=2, description="Nome completo do fornecedor")
    data_nascimento: Optional[str] = None
    cpf: Optional[str] = None

    # Dados do negócio
    nome_empresa: Optional[str] = None
    cnpj: Optional[str] = None
    descricao: Optional[str] = None

    # Dados de contato
    email: EmailStr = Field(..., description="E-mail do fornecedor")
    telefone: str = Field(..., min_length=10, description="Telefone do fornecedor")

    # Dados de acesso
    senha: str = Field(..., min_length=8, description="Senha deve ter pelo menos 8 caracteres")
    confirmar_senha: str = Field(..., description="Confirmação da senha")

    # Outros
    newsletter: Optional[str] = None

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
        try:
            return validar_nome_pessoa(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

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

    @field_validator('nome_empresa')
    @classmethod
    def validar_nome_empresa_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_texto_opcional(v, max_chars=100)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('descricao')
    @classmethod
    def validar_descricao_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_texto_opcional(v, max_chars=1000)
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

    @field_validator('senha')
    @classmethod
    def validar_senha_dto(cls, v: str) -> str:
        try:
            return validar_senha(v, min_chars=8, obrigatorio=True)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v: str, info: ValidationInfo) -> str:
        try:
            if 'senha' in info.data:
                return validar_senhas_coincidem(info.data['senha'], v)
            return v
        except ValidacaoError as e:
            raise ValueError(str(e))