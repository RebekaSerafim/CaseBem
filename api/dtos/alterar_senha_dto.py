from pydantic import BaseModel, Field, field_validator, ValidationInfo, ConfigDict
from util.validacoes_dto import validar_senha, validar_senhas_coincidem, ValidacaoError


class AlterarSenhaDTO(BaseModel):
    """DTO para dados do formulário de alteração de senha"""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "senha_atual": "senhaantiga123",
                "nova_senha": "novaSenha456",
                "confirmar_senha": "novaSenha456"
            }
        }
    )

    senha_atual: str = Field(..., min_length=1, description="Senha atual do usuário")
    nova_senha: str = Field(..., min_length=6, description="Nova senha (mínimo 6 caracteres)")
    confirmar_senha: str = Field(..., min_length=6, description="Confirmação da nova senha")

    @field_validator('senha_atual')
    @classmethod
    def senha_atual_nao_vazia(cls, v: str) -> str:
        try:
            return validar_senha(v, min_chars=1, obrigatorio=True)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('nova_senha')
    @classmethod
    def validar_nova_senha(cls, v: str, info: ValidationInfo) -> str:
        try:
            senha_validada = validar_senha(v, min_chars=6, obrigatorio=True)
            # Verificar se a nova senha é diferente da atual
            if 'senha_atual' in info.data and v == info.data['senha_atual']:
                raise ValidacaoError('A nova senha deve ser diferente da senha atual')
            return senha_validada
        except ValidacaoError as e:
            raise ValueError(str(e))

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v: str, info: ValidationInfo) -> str:
        try:
            if 'nova_senha' in info.data:
                return validar_senhas_coincidem(info.data['nova_senha'], v)
            return v
        except ValidacaoError as e:
            raise ValueError(str(e))