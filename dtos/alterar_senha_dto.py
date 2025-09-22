from pydantic import BaseModel, Field, validator
from util.validacoes_dto import validar_senha, validar_senhas_coincidem, ValidacaoError


class AlterarSenhaDTO(BaseModel):
    """DTO para dados do formulário de alteração de senha"""

    senha_atual: str = Field(..., min_length=1, description="Senha atual do usuário")
    nova_senha: str = Field(..., min_length=6, description="Nova senha (mínimo 6 caracteres)")
    confirmar_senha: str = Field(..., min_length=6, description="Confirmação da nova senha")

    @validator('senha_atual')
    def senha_atual_nao_vazia(cls, v):
        try:
            return validar_senha(v, min_chars=1, obrigatorio=True)
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('nova_senha')
    def validar_nova_senha(cls, v, values):
        try:
            senha_validada = validar_senha(v, min_chars=6, obrigatorio=True)
            # Verificar se a nova senha é diferente da atual
            if 'senha_atual' in values and v == values['senha_atual']:
                raise ValidacaoError('A nova senha deve ser diferente da senha atual')
            return senha_validada
        except ValidacaoError as e:
            raise ValueError(str(e))

    @validator('confirmar_senha')
    def senhas_devem_coincidir(cls, v, values):
        try:
            if 'nova_senha' in values:
                return validar_senhas_coincidem(values['nova_senha'], v)
            return v
        except ValidacaoError as e:
            raise ValueError(str(e))

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        schema_extra = {
            "example": {
                "senha_atual": "senhaantiga123",
                "nova_senha": "novaSenha456",
                "confirmar_senha": "novaSenha456"
            }
        }