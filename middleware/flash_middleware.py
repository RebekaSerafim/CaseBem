"""
NOTA: Este middleware NÃO está ativo no sistema.

As mensagens flash são tratadas diretamente nas rotas usando o módulo
util/flash_messages.py. Este arquivo é mantido para referência futura
ou caso seja necessário ativar o middleware.

Para ativar este middleware, adicione em main.py:
    from middleware.flash_middleware import FlashMessageMiddleware
    app.add_middleware(FlashMessageMiddleware)

Atualmente, as mensagens flash funcionam sem este middleware porque
cada rota chama get_flashed_messages() diretamente nos templates.
"""

from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from util.flash_messages import get_flashed_messages


class FlashMessageMiddleware(BaseHTTPMiddleware):
    """
    Middleware que adiciona mensagens flash no contexto dos templates
    """

    async def dispatch(self, request: Request, call_next):
        # Processar a requisição
        response = await call_next(request)

        # Se é uma resposta de template HTML, não precisamos fazer nada
        # As mensagens serão recuperadas no template handler
        return response


def add_flash_messages_to_context(request: Request, context: dict) -> dict:
    """
    Adiciona mensagens flash ao contexto do template

    Args:
        request: Objeto Request do FastAPI
        context: Contexto do template

    Returns:
        Contexto atualizado com mensagens flash
    """
    # Recuperar mensagens flash
    flash_messages = get_flashed_messages(request)

    # Adicionar ao contexto
    context["flash_messages"] = flash_messages

    return context


def create_flash_aware_template_response(templates: Jinja2Templates, template_name: str, context: dict):
    """
    Cria uma TemplateResponse que inclui mensagens flash automaticamente

    Args:
        templates: Instância do Jinja2Templates
        template_name: Nome do template
        context: Contexto do template

    Returns:
        TemplateResponse com mensagens flash incluídas
    """
    # Adicionar mensagens flash ao contexto
    if "request" in context:
        context = add_flash_messages_to_context(context["request"], context)

    return templates.TemplateResponse(template_name, context)