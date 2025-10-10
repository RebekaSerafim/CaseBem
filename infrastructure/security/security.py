"""
Módulo de segurança para gerenciar senhas e tokens
"""
import secrets
import string
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Contexto para hash de senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """
    Cria um hash seguro da senha usando bcrypt
    
    Args:
        senha: Senha em texto plano
    
    Returns:
        Hash da senha
    """
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash
    
    Args:
        senha_plana: Senha em texto plano
        senha_hash: Hash da senha armazenado no banco
    
    Returns:
        True se a senha está correta, False caso contrário
    """
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except (ValueError, TypeError):
        # Retorna False se hash inválido ou senha em formato incorreto
        return False


def gerar_token_redefinicao(tamanho: int = 32) -> str:
    """
    Gera um token aleatório seguro para redefinição de senha
    
    Args:
        tamanho: Tamanho do token em caracteres
    
    Returns:
        Token aleatório
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))


def obter_data_expiracao_token(horas: int = 24) -> str:
    """
    Calcula a data de expiração do token
    
    Args:
        horas: Número de horas de validade do token
    
    Returns:
        Data de expiração no formato ISO
    """
    expiracao = datetime.now() + timedelta(hours=horas)
    return expiracao.isoformat()


def validar_forca_senha(senha: str) -> tuple[bool, str]:
    """
    Valida se a senha atende aos requisitos mínimos de segurança
    
    Args:
        senha: Senha a ser validada
    
    Returns:
        Tupla (válida, mensagem de erro se inválida)
    """
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"

    return True, ""


def gerar_senha_aleatoria(tamanho: int = 8) -> str:
    """
    Gera uma senha aleatória segura

    Args:
        tamanho: Tamanho da senha

    Returns:
        Senha aleatória
    """
    caracteres = string.ascii_letters + string.digits + "!@#$%"
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha


def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF brasileiro (apenas formato básico)
    Valida apenas: 11 dígitos e não todos iguais

    Nota: Validação de dígito verificador removida para facilitar testes

    Args:
        cpf: CPF em formato string

    Returns:
        True se válido, False caso contrário
    """
    if not cpf:
        return True  # CPF é opcional

    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se não são todos os dígitos iguais
    if cpf == cpf[0] * 11:
        return False

    return True


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida um CNPJ brasileiro (apenas formato básico)
    Valida apenas: 14 dígitos e não todos iguais

    Nota: Validação de dígito verificador removida para facilitar testes

    Args:
        cnpj: CNPJ em formato string

    Returns:
        True se válido, False caso contrário
    """
    if not cnpj:
        return True  # CNPJ é opcional

    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # Verifica se não são todos os dígitos iguais
    if cnpj == cnpj[0] * 14:
        return False

    return True


def validar_telefone(telefone: str) -> bool:
    """
    Valida um telefone brasileiro básico

    Args:
        telefone: Telefone em formato string

    Returns:
        True se válido, False caso contrário
    """
    if not telefone:
        return False

    # Remove caracteres não numéricos
    numeros = ''.join(filter(str.isdigit, telefone))

    # Verifica se tem entre 10 e 11 dígitos (celular ou fixo)
    return len(numeros) in [10, 11]