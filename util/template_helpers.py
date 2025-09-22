"""
Helpers para templates que incluem automaticamente mensagens flash
"""

from fastapi import Request
from fastapi.templating import Jinja2Templates
from util.flash_messages import get_flashed_messages


def template_response_with_flash(templates: Jinja2Templates, template_name: str, context: dict):
    """
    Cria uma TemplateResponse que inclui automaticamente mensagens flash

    Args:
        templates: Instância do Jinja2Templates
        template_name: Nome do template
        context: Contexto do template

    Returns:
        TemplateResponse com mensagens flash incluídas
    """
    if "request" in context:
        # Adicionar mensagens flash ao contexto
        flash_messages = get_flashed_messages(context["request"])
        context["flash_messages"] = flash_messages

    return templates.TemplateResponse(template_name, context)