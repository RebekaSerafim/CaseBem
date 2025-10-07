"""
DTOs relacionados a noivos e casais.
Agrupa todas as validações e estruturas de dados para operações com noivos.
"""

from pydantic import EmailStr, Field, field_validator, ValidationInfo, model_validator
from typing import Optional, Any
from enum import Enum
from .base_dto import BaseDTO
from util.validacoes_dto import (
    validar_nome_pessoa, validar_cpf, validar_telefone, validar_data_nascimento,
    validar_senha, validar_senhas_coincidem, validar_valor_monetario, validar_numero_inteiro,
    validar_enum_valor, converter_checkbox_para_bool
)


class GeneroEnum(str, Enum):
    """Enum para gêneros"""
    MASCULINO = "MASCULINO"
    FEMININO = "FEMININO"
    OUTROS = "OUTROS"
    NAO_INFORMAR = "NAO_INFORMAR"


class CadastroNoivosDTO(BaseDTO):
    """
    DTO para formulário de cadastro de noivos.
    Usado para registro de novo casal no sistema.
    """

    # Dados do casamento
    data_casamento: Optional[str] = Field(None, description="Data prevista do casamento (formato: YYYY-MM-DD)")
    local_previsto: Optional[str] = Field(None, max_length=200, description="Local previsto do casamento")
    orcamento_estimado: Optional[str] = Field(None, description="Orçamento estimado para o casamento")
    numero_convidados: Optional[str] = Field(None, description="Número estimado de convidados")

    # Dados do primeiro noivo
    nome1: str = Field(..., min_length=2, max_length=100, description="Nome completo do primeiro noivo")
    data_nascimento1: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    cpf1: Optional[str] = Field(None, description="CPF do primeiro noivo")
    email1: EmailStr = Field(..., description="E-mail do primeiro noivo")
    telefone1: str = Field(..., min_length=10, description="Telefone do primeiro noivo")
    genero1: Optional[str] = Field(None, description="Gênero do primeiro noivo")

    # Dados do segundo noivo
    nome2: str = Field(..., min_length=2, max_length=100, description="Nome completo do segundo noivo")
    data_nascimento2: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    cpf2: Optional[str] = Field(None, description="CPF do segundo noivo")
    email2: EmailStr = Field(..., description="E-mail do segundo noivo")
    telefone2: str = Field(..., min_length=10, description="Telefone do segundo noivo")
    genero2: Optional[str] = Field(None, description="Gênero do segundo noivo")

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

    @field_validator('nome1')
    @classmethod
    def validar_nome1(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor),
            "Nome do primeiro noivo"
        )
        return validador(v)

    @field_validator('nome2')
    @classmethod
    def validar_nome2(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor),
            "Nome do segundo noivo"
        )
        return validador(v)

    @field_validator('cpf1')
    @classmethod
    def validar_cpf1(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF do primeiro noivo"
        )
        return validador(v)

    @field_validator('cpf2')
    @classmethod
    def validar_cpf2(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF do segundo noivo"
        )
        return validador(v)

    @field_validator('telefone1')
    @classmethod
    def validar_telefone1(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone do primeiro noivo"
        )
        return validador(v)

    @field_validator('telefone2')
    @classmethod
    def validar_telefone2(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone do segundo noivo"
        )
        return validador(v)

    @field_validator('data_nascimento1')
    @classmethod
    def validar_data_nascimento1(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_data_nascimento(valor, idade_minima=16),
            "Data de nascimento do primeiro noivo"
        )
        return validador(v)

    @field_validator('data_nascimento2')
    @classmethod
    def validar_data_nascimento2(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_data_nascimento(valor, idade_minima=16),
            "Data de nascimento do segundo noivo"
        )
        return validador(v)

    @field_validator('orcamento_estimado')
    @classmethod
    def validar_orcamento_estimado(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_valor_monetario(valor, campo, obrigatorio=False),
            "Orçamento estimado"
        )
        validador(v)
        return v

    @field_validator('numero_convidados')
    @classmethod
    def validar_numero_convidados(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_numero_inteiro(valor, campo, obrigatorio=False, min_valor=1, max_valor=9999),
            "Número de convidados"
        )
        validador(v)
        return v

    @field_validator('senha')
    @classmethod
    def validar_senha_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=8, obrigatorio=True),
            "Senha"
        )
        return validador(v)  # type: ignore[return-value]

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

    @field_validator('email2')
    @classmethod
    def emails_devem_ser_diferentes(cls, v: EmailStr, info: ValidationInfo) -> EmailStr:
        if 'email1' in info.data and v == info.data['email1']:
            raise ValueError('Os e-mails dos noivos devem ser diferentes')
        return v

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "data_casamento": "2025-12-15",
            "local_previsto": "Igreja São Pedro",
            "orcamento_estimado": "50000.00",
            "numero_convidados": "150",
            "nome1": "João Silva",
            "data_nascimento1": "1990-05-15",
            "cpf1": "123.456.789-01",
            "email1": "joao@email.com",
            "telefone1": "(11) 99999-9999",
            "genero1": "MASCULINO",
            "nome2": "Maria Santos",
            "data_nascimento2": "1992-08-20",
            "cpf2": "987.654.321-09",
            "email2": "maria@email.com",
            "telefone2": "(11) 98888-8888",
            "genero2": "FEMININO",
            "senha": "senhaSegura123",
            "confirmar_senha": "senhaSegura123",
            "newsletter": True
        }
        exemplo.update(overrides)
        return exemplo


class PerfilNoivoDTO(BaseDTO):
    """
    DTO para formulário de perfil do noivo.
    Usado para editar informações pessoais do noivo logado.
    """

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do noivo")
    email: EmailStr = Field(..., description="E-mail do noivo")
    telefone: str = Field(..., min_length=10, description="Telefone do noivo")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    cpf: Optional[str] = Field(None, description="CPF do noivo")
    genero: Optional[GeneroEnum] = Field(None, description="Gênero do noivo")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor),
            "Nome do noivo"
        )
        return validador(v)

    @field_validator('cpf')
    @classmethod
    def validar_cpf_campo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento_campo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_data_nascimento(valor, idade_minima=16),
            "Data de nascimento"
        )
        return validador(v)

    @field_validator('genero')
    @classmethod
    def validar_genero_campo(cls, v: Optional[GeneroEnum]) -> Optional[GeneroEnum]:
        if v is None:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_enum_valor(valor, GeneroEnum, campo),
            "Gênero"
        )
        return validador(v)  # type: ignore[no-any-return]

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "email": "joao@email.com",
            "telefone": "(11) 99999-9999",
            "data_nascimento": "1990-05-15",
            "cpf": "123.456.789-01",
            "genero": "MASCULINO"
        }
        exemplo.update(overrides)
        return exemplo


# Configurar exemplos JSON nos model_config
CadastroNoivosDTO.model_config.update({
    "json_schema_extra": {
        "example": CadastroNoivosDTO.criar_exemplo_json()
    }
})

PerfilNoivoDTO.model_config.update({
    "json_schema_extra": {
        "example": PerfilNoivoDTO.criar_exemplo_json()
    }
})