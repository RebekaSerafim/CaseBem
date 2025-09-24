from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo, Field, ConfigDict
from typing import Optional, List


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

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v: str, info: ValidationInfo) -> str:
        if 'senha' in info.data and v != info.data['senha']:
            raise ValueError('As senhas não coincidem')
        return v