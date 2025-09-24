from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional


class LoginDTO(BaseModel):
    """DTO para dados do formulário de login"""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "email": "usuario@exemplo.com",
                "senha": "minhasenha123",
                "redirect": "/dashboard"
            }
        }
    )

    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")
    redirect: Optional[str] = Field(None, description="URL de redirecionamento após login")

    @field_validator('senha')
    @classmethod
    def senha_nao_vazia(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Senha é obrigatória')
        return v