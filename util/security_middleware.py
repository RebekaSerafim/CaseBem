"""
Middleware avançado de segurança e autenticação
"""
import logging
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Set, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse

# Configurar logging de segurança
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# Armazenamento temporário em memória (em produção usar Redis)
failed_attempts: Dict[str, int] = {}
blocked_ips: Dict[str, datetime] = {}
active_sessions: Dict[str, Set[str]] = {}  # user_id -> set of session_ids

# Configurações de segurança
MAX_FAILED_ATTEMPTS = 5
BLOCK_DURATION_MINUTES = 15
SESSION_TIMEOUT_HOURS = 8
MAX_SESSIONS_PER_USER = 3

def get_client_ip(request: Request) -> str:
    """Obtém o IP real do cliente considerando proxies"""
    # Verifica headers de proxy
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fallback para o IP direto
    return request.client.host if request.client else "unknown"

def get_session_id(request: Request) -> str:
    """Gera um ID único para a sessão"""
    user_agent = request.headers.get("User-Agent", "")
    ip = get_client_ip(request)
    session_data = f"{ip}:{user_agent}:{time.time()}"
    return hashlib.md5(session_data.encode()).hexdigest()

def is_ip_blocked(ip: str) -> bool:
    """Verifica se um IP está bloqueado"""
    if ip in blocked_ips:
        block_time = blocked_ips[ip]
        if datetime.now() < block_time + timedelta(minutes=BLOCK_DURATION_MINUTES):
            return True
        else:
            # Remove IP expirado
            del blocked_ips[ip]
            if ip in failed_attempts:
                del failed_attempts[ip]
    return False

def register_failed_attempt(ip: str):
    """Registra uma tentativa de login falhada"""
    failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

    if failed_attempts[ip] >= MAX_FAILED_ATTEMPTS:
        blocked_ips[ip] = datetime.now()
        security_logger.warning(f"IP {ip} bloqueado após {MAX_FAILED_ATTEMPTS} tentativas falhadas")

def clear_failed_attempts(ip: str):
    """Limpa tentativas falhadas após login bem-sucedido"""
    if ip in failed_attempts:
        del failed_attempts[ip]

def validate_session_security(request: Request, usuario: dict) -> bool:
    """Valida aspectos de segurança da sessão"""

    # Verifica se IP está bloqueado
    client_ip = get_client_ip(request)
    if is_ip_blocked(client_ip):
        security_logger.warning(f"Acesso negado para IP bloqueado: {client_ip}")
        return False

    # Verifica timeout da sessão
    if 'login_time' in request.session:
        login_time = datetime.fromisoformat(request.session['login_time'])
        if datetime.now() > login_time + timedelta(hours=SESSION_TIMEOUT_HOURS):
            security_logger.info(f"Sessão expirada para usuário {usuario.get('id')}")
            return False

    return True

def manage_user_sessions(request: Request, user_id: str, action: str = "add"):
    """Gerencia sessões ativas do usuário"""
    session_id = get_session_id(request)

    if action == "add":
        if user_id not in active_sessions:
            active_sessions[user_id] = set()

        active_sessions[user_id].add(session_id)

        # Limita o número de sessões simultâneas
        if len(active_sessions[user_id]) > MAX_SESSIONS_PER_USER:
            # Remove a sessão mais antiga (primeira do set)
            oldest_session = next(iter(active_sessions[user_id]))
            active_sessions[user_id].remove(oldest_session)
            security_logger.info(f"Sessão mais antiga removida para usuário {user_id}")

    elif action == "remove":
        if user_id in active_sessions:
            active_sessions[user_id].discard(session_id)
            if not active_sessions[user_id]:
                del active_sessions[user_id]

def log_security_event(event_type: str, request: Request, usuario: dict = {}, details: str = ""):
    """Registra eventos de segurança"""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "")
    user_id = usuario.get('id') if usuario else 'anonymous'

    security_logger.info(
        f"SECURITY_EVENT: {event_type} | "
        f"User: {user_id} | "
        f"IP: {client_ip} | "
        f"UserAgent: {user_agent} | "
        f"Path: {request.url.path} | "
        f"Details: {details}"
    )

def enhanced_create_session(request: Request, usuario: dict) -> None:
    """Cria sessão com recursos de segurança avançados"""
    from util.auth_decorator import criar_sessao

    # Cria sessão básica
    criar_sessao(request, usuario)

    # Adiciona informações de segurança
    request.session['login_time'] = datetime.now().isoformat()
    request.session['client_ip'] = get_client_ip(request)
    request.session['user_agent_hash'] = hashlib.md5(
        request.headers.get("User-Agent", "").encode()
    ).hexdigest()

    user_id = str(usuario['id'])

    # Gerencia sessões ativas
    manage_user_sessions(request, user_id, "add")

    # Limpa tentativas falhadas
    clear_failed_attempts(get_client_ip(request))

    # Log do evento
    log_security_event("LOGIN_SUCCESS", request, usuario)

def enhanced_destroy_session(request: Request) -> None:
    """Destrói sessão com limpeza completa"""
    from util.auth_decorator import destruir_sessao, obter_usuario_logado

    usuario = obter_usuario_logado(request)
    if usuario:
        user_id = str(usuario['id'])
        manage_user_sessions(request, user_id, "remove")
        log_security_event("LOGOUT", request, usuario)

    destruir_sessao(request)

def security_middleware():
    """Middleware de segurança para ser usado com FastAPI"""
    async def middleware(request: Request, call_next):
        # Verifica bloqueio de IP antes de processar qualquer request
        client_ip = get_client_ip(request)

        if is_ip_blocked(client_ip):
            log_security_event("BLOCKED_IP_ACCESS", request, details=f"IP {client_ip} está bloqueado")
            return RedirectResponse(
                url="/blocked",
                status_code=status.HTTP_403_FORBIDDEN
            )

        # Valida integridade da sessão
        if hasattr(request, 'session') and 'usuario' in request.session:
            usuario = request.session['usuario']

            # Verifica se a sessão é válida
            if not validate_session_security(request, usuario):
                enhanced_destroy_session(request)
                return RedirectResponse(
                    url="/login?reason=session_expired",
                    status_code=status.HTTP_303_SEE_OTHER
                )

            # Verifica mudança de IP suspeita
            session_ip = request.session.get('client_ip')
            if session_ip and session_ip != client_ip:
                log_security_event(
                    "SUSPICIOUS_IP_CHANGE",
                    request,
                    usuario,
                    f"Session IP: {session_ip}, Current IP: {client_ip}"
                )
                # Em ambiente de alta segurança, poderia forçar logout

        response = await call_next(request)
        return response

    return middleware

def requires_secure_access(min_security_level: int = 1):
    """
    Decorator adicional para rotas que requerem segurança extra

    Args:
        min_security_level: Nível mínimo de segurança (1-3)
                          1 = básico, 2 = médio, 3 = alto
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Encontra request
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )

            # Validações de segurança baseadas no nível
            if min_security_level >= 2:
                # Nível médio: verifica headers de segurança
                if not request.headers.get("User-Agent"):
                    log_security_event("MISSING_USER_AGENT", request)
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Acesso negado"
                    )

            if min_security_level >= 3:
                # Nível alto: verifica HTTPS em produção
                if not request.url.scheme == "https" and request.headers.get("host") != "localhost":
                    log_security_event("INSECURE_CONNECTION", request)
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Conexão segura requerida"
                    )

            return await func(*args, **kwargs)

        return wrapper
    return decorator