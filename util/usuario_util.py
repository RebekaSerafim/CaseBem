"""
Utilitários para manipulação de dados de usuário
"""
from typing import Dict, Any
from core.models.usuario_model import TipoUsuario, Usuario


def usuario_para_sessao(usuario: Usuario) -> Dict[str, Any]:
    """
    Converte um objeto Usuario para dicionário de sessão,
    convertendo o Enum para string.

    Args:
        usuario: Objeto Usuario

    Returns:
        Dicionário com dados para armazenar na sessão
    """
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil.value  # Converter Enum para string
    }


def obter_perfil_enum(perfil_string: str) -> TipoUsuario:
    """
    Converte string de perfil para Enum TipoUsuario

    Args:
        perfil_string: String do perfil

    Returns:
        TipoUsuario correspondente

    Raises:
        ValueError: Se o perfil não for válido
    """
    try:
        return TipoUsuario(perfil_string)
    except ValueError:
        # Se não encontrar, tenta com valores comuns de legado
        perfil_map = {
            'admin': TipoUsuario.ADMIN,
            'cliente': TipoUsuario.NOIVO,  # Assumindo que cliente = noivo no contexto
        }
        if perfil_string.lower() in perfil_map:
            return perfil_map[perfil_string.lower()]
        raise ValueError(f"Perfil inválido: {perfil_string}")


def validar_permissao(usuario_perfil: str, perfis_permitidos: list[str]) -> bool:
    """
    Valida se o perfil do usuário está na lista de perfis permitidos

    Args:
        usuario_perfil: Perfil do usuário (string)
        perfis_permitidos: Lista de perfis permitidos

    Returns:
        True se o usuário tem permissão, False caso contrário
    """
    return usuario_perfil in perfis_permitidos


def eh_admin(usuario_dict: Dict[str, Any]) -> bool:
    """
    Verifica se o usuário é administrador

    Args:
        usuario_dict: Dados do usuário da sessão

    Returns:
        True se for admin, False caso contrário
    """
    return usuario_dict.get('perfil') == TipoUsuario.ADMIN.value