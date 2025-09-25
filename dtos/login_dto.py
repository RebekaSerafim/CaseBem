from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from util.validacoes_dto import validar_senha, ValidacaoError


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
    def validar_senha_dto(cls, v: str) -> str:
        try:
            return validar_senha(v, min_chars=1, obrigatorio=True)
        except ValidacaoError as e:
            raise ValueError(str(e))