from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class LoginDTO(BaseModel):
    """DTO para dados do formulário de login"""

    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")
    redirect: Optional[str] = Field(None, description="URL de redirecionamento após login")

    @validator('senha')
    def senha_nao_vazia(cls, v):
        if not v or not v.strip():
            raise ValueError('Senha é obrigatória')
        return v

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "senha": "minhasenha123",
                "redirect": "/dashboard"
            }
        }