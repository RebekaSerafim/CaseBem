"""
DTOs relacionados a usuários e autenticação.
Agrupa todas as validações e estruturas de dados para operações com usuários.
"""

from pydantic import EmailStr, Field, field_validator, ValidationInfo
from typing import Optional
from .base_dto import BaseDTO
from util.validacoes_dto import (
    validar_cpf, validar_telefone, validar_data_nascimento,
    validar_nome_pessoa, validar_senha, validar_senhas_coincidem,
    validar_texto_opcional, validar_estado_brasileiro
)


class LoginDTO(BaseDTO):
    """
    DTO para formulário de login.
    Usado para autenticação de usuários no sistema.
    """

    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")
    redirect: Optional[str] = Field(None, description="URL de redirecionamento após login")

    @field_validator('senha')
    @classmethod
    def validar_senha_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=1, obrigatorio=True),
            "Senha"
        )
        return validador(v)  # type: ignore[return-value]

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "email": "usuario@exemplo.com",
            "senha": "minhasenha123",
            "redirect": "/dashboard"
        }
        exemplo.update(overrides)
        return exemplo


class AlterarSenhaDTO(BaseDTO):
    """
    DTO para formulário de alteração de senha.
    Usado quando usuário quer alterar sua senha atual.
    """

    senha_atual: str = Field(..., min_length=1, description="Senha atual do usuário")
    nova_senha: str = Field(..., min_length=6, description="Nova senha (mínimo 6 caracteres)")
    confirmar_senha: str = Field(..., min_length=6, description="Confirmação da nova senha")

    @field_validator('senha_atual')
    @classmethod
    def senha_atual_nao_vazia(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=1, obrigatorio=True),
            "Senha atual"
        )
        return validador(v)  # type: ignore[return-value]

    @field_validator('nova_senha')
    @classmethod
    def validar_nova_senha(cls, v: str, info: ValidationInfo) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=6, obrigatorio=True),
            "Nova senha"
        )
        senha_validada = validador(v)

        # Verificar se a nova senha é diferente da atual
        if 'senha_atual' in info.data and v == info.data['senha_atual']:
            raise ValueError('A nova senha deve ser diferente da senha atual')
        return senha_validada  # type: ignore[return-value]

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v: str, info: ValidationInfo) -> str:
        if 'nova_senha' in info.data:
            validador = cls.validar_campo_wrapper(
                lambda valor, campo: validar_senhas_coincidem(info.data['nova_senha'], valor),
                "Confirmação de senha"
            )
            return validador(v)
        return v

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "senha_atual": "senhaantiga123",
            "nova_senha": "novaSenha456",
            "confirmar_senha": "novaSenha456"
        }
        exemplo.update(overrides)
        return exemplo


class AdminUsuarioDTO(BaseDTO):
    """
    DTO para formulário de criação/edição de usuário administrador.
    Usado pelo admin para gerenciar outros usuários admin.
    """

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do administrador")
    email: EmailStr = Field(..., description="E-mail do administrador")
    cpf: Optional[str] = Field(None, description="CPF do administrador")
    telefone: Optional[str] = Field(None, description="Telefone do administrador")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento (formato: YYYY-MM-DD)")
    senha: Optional[str] = Field(None, min_length=6, description="Senha (obrigatória apenas na criação)")

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor),
            "Nome do administrador"
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

    @field_validator('telefone')
    @classmethod
    def validar_telefone_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
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
            lambda valor, campo: validar_data_nascimento(valor, idade_minima=18),
            "Data de nascimento"
        )
        return validador(v)

    @field_validator('senha')
    @classmethod
    def validar_senha_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, obrigatorio=False),
            "Senha"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "Carlos Santos",
            "email": "carlos.admin@casebem.com",
            "cpf": "123.456.789-01",
            "telefone": "(11) 99999-9999",
            "data_nascimento": "1985-03-15",
            "senha": "senhaSegura123"
        }
        exemplo.update(overrides)
        return exemplo


class PerfilAdminDTO(BaseDTO):
    """
    DTO para formulário de perfil do administrador.
    Usado para editar informações pessoais do admin logado.
    """

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do administrador")
    email: EmailStr = Field(..., description="E-mail do administrador")
    telefone: Optional[str] = Field(None, description="Telefone do administrador")
    cargo: Optional[str] = Field(None, max_length=50, description="Cargo do administrador")
    endereco: Optional[str] = Field(None, max_length=200, description="Endereço completo")
    cidade: Optional[str] = Field(None, max_length=50, description="Cidade")
    estado: Optional[str] = Field(None, max_length=2, description="Estado (sigla UF)")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações sobre o administrador")

    @field_validator('nome')
    @classmethod
    def validar_nome_dto(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor, min_chars=2, max_chars=100),
            "Nome"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @field_validator('cargo')
    @classmethod
    def validar_cargo_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=50),
            "Cargo"
        )
        return validador(v)

    @field_validator('endereco')
    @classmethod
    def validar_endereco_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=200),
            "Endereço"
        )
        return validador(v)

    @field_validator('cidade')
    @classmethod
    def validar_cidade_dto(cls, v: Optional[str]) -> Optional[str]:
        # Primeira validação: se existe, deve ser um nome válido
        if v:
            validador_nome = cls.validar_campo_wrapper(
                lambda valor, campo: validar_nome_pessoa(valor, min_chars=1, max_chars=50),
                "Cidade"
            )
            validador_nome(v)

        # Segunda validação: tamanho máximo
        validador_texto = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=50),
            "Cidade"
        )
        return validador_texto(v)

    @field_validator('estado')
    @classmethod
    def validar_estado_dto(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_estado_brasileiro(valor),
            "Estado"
        )
        return validador(v)

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes_dto(cls, v: Optional[str]) -> Optional[str]:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=1000),
            "Observações"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "Maria Silva",
            "email": "maria.admin@casebem.com",
            "telefone": "(11) 99999-9999",
            "cargo": "Gerente de Sistemas",
            "endereco": "Rua das Flores, 123 - Centro",
            "cidade": "São Paulo",
            "estado": "SP",
            "observacoes": "Responsável pela administração geral do sistema"
        }
        exemplo.update(overrides)
        return exemplo


# Configurar exemplos JSON nos model_config
LoginDTO.model_config.update({
    "json_schema_extra": {
        "example": LoginDTO.criar_exemplo_json()
    }
})

AlterarSenhaDTO.model_config.update({
    "json_schema_extra": {
        "example": AlterarSenhaDTO.criar_exemplo_json()
    }
})

AdminUsuarioDTO.model_config.update({
    "json_schema_extra": {
        "example": AdminUsuarioDTO.criar_exemplo_json()
    }
})

PerfilAdminDTO.model_config.update({
    "json_schema_extra": {
        "example": PerfilAdminDTO.criar_exemplo_json()
    }
})