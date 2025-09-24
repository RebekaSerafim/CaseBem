from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.template_helpers import configurar_filtros_jinja

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)

@router.get("/blocked")
async def blocked_page(request: Request):
    """Página mostrada quando um IP está bloqueado"""
    return templates.TemplateResponse("blocked.html", {
        "request": request
    })

@router.get("/security/status")
async def security_status(request: Request):
    """Endpoint para verificar status de segurança (para monitoramento)"""
    from util.security_middleware import failed_attempts, blocked_ips, active_sessions

    # Só retorna informações básicas, sem dados sensíveis
    return {
        "blocked_ips_count": len(blocked_ips),
        "failed_attempts_count": len(failed_attempts),
        "active_sessions_count": sum(len(sessions) for sessions in active_sessions.values()),
        "status": "operational"
    }