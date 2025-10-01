"""
Decoradores e handlers para tratamento de erros
"""

import functools
import sqlite3
from typing import Callable, Any, Optional, Type
from fastapi import Request
from fastapi.templating import Jinja2Templates
from util.exceptions import (
    CaseBemError, BancoDadosError, ValidacaoError,
    RecursoNaoEncontradoError, TipoErro
)
from infrastructure.logging import logger
from util.flash_messages import informar_erro
from util.template_helpers import configurar_filtros_jinja


def tratar_erro_banco_dados(operacao: str = "operação de banco"):
    """
    Decorador para tratar erros de banco de dados de forma padronizada

    Args:
        operacao: Nome da operação sendo executada
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.IntegrityError as e:
                erro_msg = "Violação de integridade dos dados"
                if "UNIQUE constraint failed" in str(e):
                    erro_msg = "Este registro já existe no sistema"
                elif "FOREIGN KEY constraint failed" in str(e):
                    erro_msg = "Registro relacionado não encontrado"

                logger.error(f"Erro de integridade em {operacao}", erro=e,
                           funcao=func.__name__, args_count=len(args))
                raise BancoDadosError(erro_msg, operacao, e)

            except sqlite3.OperationalError as e:
                erro_msg = "Erro na operação de banco de dados"
                logger.error(f"Erro operacional em {operacao}", erro=e,
                           funcao=func.__name__)
                raise BancoDadosError(erro_msg, operacao, e)

            except Exception as e:
                if isinstance(e, CaseBemError):
                    raise  # Re-lança exceções personalizadas

                logger.error(f"Erro inesperado em {operacao}", erro=e,
                           funcao=func.__name__)
                raise BancoDadosError(f"Erro interno durante {operacao}", operacao, e)

        return wrapper
    return decorator


def tratar_erro_rota(template_erro: Optional[str] = None,
                     redirect_erro: Optional[str] = None):
    """
    Decorador para tratar erros em rotas web

    Args:
        template_erro: Template para renderizar em caso de erro
        redirect_erro: URL para redirecionar em caso de erro
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                return await func(request, *args, **kwargs)

            except ValidacaoError as e:
                logger.warning("Erro de validação em rota", erro=e, rota=str(request.url))
                informar_erro(request, f"Dados inválidos: {e.mensagem}")

                if template_erro:
                    templates = Jinja2Templates(directory="templates")
                    configurar_filtros_jinja(templates)
                    return templates.TemplateResponse(template_erro, {
                        "request": request,
                        "erro": e.mensagem
                    })

            except RecursoNaoEncontradoError as e:
                logger.info("Recurso não encontrado", erro=e, rota=str(request.url))
                informar_erro(request, e.mensagem)

            except CaseBemError as e:
                logger.error("Erro de negócio em rota", erro=e, rota=str(request.url))
                informar_erro(request, e.mensagem)

            except Exception as e:
                logger.error("Erro inesperado em rota", erro=e, rota=str(request.url))
                informar_erro(request, "Erro interno do sistema. Tente novamente.")

            # Fallback para redirect ou template
            if redirect_erro:
                from fastapi.responses import RedirectResponse
                return RedirectResponse(redirect_erro)
            elif template_erro:
                templates = Jinja2Templates(directory="templates")
                configurar_filtros_jinja(templates)
                return templates.TemplateResponse(template_erro, {
                    "request": request,
                    "erro": "Ocorreu um erro. Tente novamente."
                })

        return wrapper
    return decorator


def validar_parametros(*tipos_esperados: Type):
    """
    Decorador para validar tipos de parâmetros
    Pula o primeiro parâmetro (self) em métodos de instância

    Args:
        *tipos_esperados: Tipos esperados para cada parâmetro (excluindo self)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Pular o primeiro parâmetro (self) se é um método de instância
            args_para_validar = args[1:] if len(args) > 0 and hasattr(args[0], '__dict__') else args

            # Validar args
            for i, (arg, tipo_esperado) in enumerate(zip(args_para_validar, tipos_esperados)):
                if arg is not None and not isinstance(arg, tipo_esperado):
                    raise ValidacaoError(
                        f"Parâmetro {i+1} deve ser do tipo {tipo_esperado.__name__}",
                        campo=f"param_{i+1}",
                        valor=arg
                    )

            return func(*args, **kwargs)
        return wrapper
    return decorator


def tratar_erro_simples(operacao: str = "operação"):
    """
    Decorador simples para funções que não precisam de tratamento específico

    Args:
        operacao: Nome da operação sendo executada
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CaseBemError:
                raise  # Re-lança exceções personalizadas
            except Exception as e:
                logger.error(f"Erro em {operacao}", erro=e, funcao=func.__name__)
                raise CaseBemError(f"Erro durante {operacao}", erro_original=e)

        return wrapper
    return decorator