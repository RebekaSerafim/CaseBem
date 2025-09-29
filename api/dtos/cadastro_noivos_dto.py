from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo, Field, ConfigDict, model_validator
from typing import Optional, Any
from util.validacoes_dto import (
    validar_nome_pessoa, validar_cpf, validar_telefone, validar_data_nascimento,
    validar_senha, validar_senhas_coincidem, validar_valor_monetario, validar_numero_inteiro,
    converter_checkbox_para_bool, ValidacaoError
)


class CadastroNoivosDTO(BaseModel):
    """DTO para dados do formulário de cadastro de noivos"""

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    # Dados do casamento
    data_casamento: Optional[str] = None
    local_previsto: Optional[str] = None
    orcamento_estimado: Optional[str] = None
    numero_convidados: Optional[str] = None

    # Dados do primeiro noivo
    nome1: str = Field(..., min_length=2, description="Nome completo do primeiro noivo")
    data_nascimento1: Optional[str] = None
    cpf1: Optional[str] = None
    email1: EmailStr = Field(..., description="E-mail do primeiro noivo")
    telefone1: str = Field(..., min_length=10, description="Telefone do primeiro noivo")
    genero1: Optional[str] = None

    # Dados do segundo noivo
    nome2: str = Field(..., min_length=2, description="Nome completo do segundo noivo")
    data_nascimento2: Optional[str] = None
    cpf2: Optional[str] = None
    email2: EmailStr = Field(..., description="E-mail do segundo noivo")
    telefone2: str = Field(..., min_length=10, description="Telefone do segundo noivo")
    genero2: Optional[str] = None

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

    @field_validator('nome1')
    @classmethod
    def validar_nome1_dto(cls, v: str) -> str:
        try:
            return validar_nome_pessoa(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('nome2')
    @classmethod
    def validar_nome2_dto(cls, v: str) -> str:
        try:
            return validar_nome_pessoa(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('cpf1')
    @classmethod
    def validar_cpf1_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_cpf(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('cpf2')
    @classmethod
    def validar_cpf2_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_cpf(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('telefone1')
    @classmethod
    def validar_telefone1_dto(cls, v: str) -> str:
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('telefone2')
    @classmethod
    def validar_telefone2_dto(cls, v: str) -> str:
        try:
            return validar_telefone(v)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('data_nascimento1')
    @classmethod
    def validar_data_nascimento1_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_data_nascimento(v, idade_minima=16)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('data_nascimento2')
    @classmethod
    def validar_data_nascimento2_dto(cls, v: Optional[str]) -> Optional[str]:
        try:
            return validar_data_nascimento(v, idade_minima=16)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('orcamento_estimado')
    @classmethod
    def validar_orcamento_estimado_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        try:
            validar_valor_monetario(v, "Orçamento estimado", obrigatorio=False)
            return v
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('numero_convidados')
    @classmethod
    def validar_numero_convidados_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        try:
            validar_numero_inteiro(v, "Número de convidados", obrigatorio=False, min_valor=1, max_valor=9999)
            return v
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

    @field_validator('email2')
    @classmethod
    def emails_devem_ser_diferentes(cls, v: EmailStr, info: ValidationInfo) -> EmailStr:
        if 'email1' in info.data and v == info.data['email1']:
            raise ValueError('Os e-mails dos noivos devem ser diferentes')
        return v