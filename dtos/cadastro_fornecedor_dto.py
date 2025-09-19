from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List


class CadastroFornecedorDTO(BaseModel):
    """DTO para dados do formulário de cadastro de fornecedor"""

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

    # Perfis (tipos de fornecimento)
    perfis: List[str] = Field(..., min_items=1, description="Selecione pelo menos um tipo de fornecimento")

    # Outros
    newsletter: Optional[str] = None

    @validator('confirmar_senha')
    def senhas_devem_coincidir(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('As senhas não coincidem')
        return v

    @validator('perfis')
    def validar_perfis(cls, v):
        perfis_validos = ['prestador', 'vendedor', 'locador']
        for perfil in v:
            if perfil not in perfis_validos:
                raise ValueError(f'Perfil inválido: {perfil}')
        return v

    class Config:
        # Permite que o modelo aceite dados de formulário HTML
        str_strip_whitespace = True
        validate_assignment = True