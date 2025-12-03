"""
Sistema de mensagens flash para FastAPI
Permite enviar mensagens através de redirects usando sessões
"""

from fastapi import Request
from typing import List, Dict, Any

def flash(request: Request, message: str, type: str = "info") -> None:
    """
    Adiciona uma mensagem flash à sessão

    Args:
        request: Objeto Request do FastAPI
        message: Mensagem a ser exibida
        type: Tipo da mensagem (success, danger, warning, info, alert)
    """
    if "flash_messages" not in request.session:
        request.session["flash_messages"] = []

    request.session["flash_messages"].append({
        "text": message,
        "type": type
    })

def informar_sucesso(request: Request, message: str) -> None:
    """Adiciona mensagem de sucesso"""
    flash(request, message, "success")

def informar_erro(request: Request, message: str) -> None:
    """Adiciona mensagem de erro"""
    flash(request, message, "danger")

def informar_aviso(request: Request, message: str) -> None:
    """Adiciona mensagem de aviso"""
    flash(request, message, "warning")

def informar_info(request: Request, message: str) -> None:
    """Adiciona mensagem informativa"""
    flash(request, message, "info")

def informar_alerta(request: Request, message: str) -> None:
    """Adiciona mensagem de alerta"""
    flash(request, message, "alert")

def get_flashed_messages(request: Request) -> List[Dict[str, Any]]:
    """
    Recupera e remove as mensagens flash da sessão

    Args:
        request: Objeto Request do FastAPI

    Returns:
        Lista de mensagens flash
    """
    messages = request.session.pop("flash_messages", [])
    return messages  # type: ignore[no-any-return]

def has_flashed_messages(request: Request) -> bool:
    """
    Verifica se há mensagens flash na sessão

    Args:
        request: Objeto Request do FastAPI

    Returns:
        True se há mensagens, False caso contrário
    """
    return "flash_messages" in request.session and len(request.session["flash_messages"]) > 0