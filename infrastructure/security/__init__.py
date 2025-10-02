"""
Infrastructure Security - Segurança e autenticação

Este módulo gerencia toda a infraestrutura de segurança:
- security: Hash de senhas, validação CPF/CNPJ, tokens
- auth_decorator: Decorators de autenticação e autorização
"""

# Funções de segurança (senhas, tokens, validações)
from infrastructure.security.security import (
    criar_hash_senha,
    verificar_senha,
    gerar_token_redefinicao,
    obter_data_expiracao_token,
    validar_forca_senha,
    gerar_senha_aleatoria,
    validar_cpf,
    validar_cnpj,
    validar_telefone,
)

# Decorators e funções de autenticação
from infrastructure.security.auth_decorator import (
    obter_usuario_logado,
    esta_logado,
    criar_sessao,
    destruir_sessao,
    requer_autenticacao,
)

__all__ = [
    # Security
    'criar_hash_senha',
    'verificar_senha',
    'gerar_token_redefinicao',
    'obter_data_expiracao_token',
    'validar_forca_senha',
    'gerar_senha_aleatoria',
    'validar_cpf',
    'validar_cnpj',
    'validar_telefone',
    # Auth decorator
    'obter_usuario_logado',
    'esta_logado',
    'criar_sessao',
    'destruir_sessao',
    'requer_autenticacao',
]
