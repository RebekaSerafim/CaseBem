# ⚠️ FASE 3: Centralizar e Padronizar Tratamento de Erros

## 🎯 Objetivo Principal
Criar um sistema centralizado e consistente de tratamento de erros, eliminando try/catch genéricos e melhorando a experiência do usuário com mensagens de erro claras.

## 🔍 Análise do Problema Atual

### Problemas Identificados:
- **Try/catch genérico** espalhado por todo código: `except Exception as e:`
- **Mensagens inconsistentes**: Cada lugar trata erro de forma diferente
- **Print statements** para debugging em produção
- **Falta de logging estruturado**
- **Experiência ruim do usuário**: Erros técnicos expostos na interface

### Exemplo Atual em `repo/usuario_repo.py`:
```python
def criar_tabela_usuarios() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_USUARIO)
            return True
    except Exception as e:
        # Problema: Exception muito genérica
        print(f"Erro ao criar tabela de usuários: {e}")  # Print em produção!
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with obter_conexao() as conexao:  # Sem tratamento de erro!
        cursor = conexao.cursor()
        cursor.execute(INSERIR_USUARIO, (...))
        return cursor.lastrowid
```

### Exemplo em Rotas `admin_routes.py`:
```python
@router.get("/admin/perfil")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def perfil_admin(request: Request, usuario_logado: dict = None):
    try:
        admin = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
        return templates.TemplateResponse("admin/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin,
        })
    except Exception as e:  # Exception muito genérica
        print(f"Erro ao carregar perfil admin: {e}")  # Print em produção!
        return templates.TemplateResponse("admin/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar perfil"  # Mensagem genérica demais
        })
```

## 💡 Solução Proposta

### 1. Criar Hierarquia de Exceções Personalizadas

#### `util/exceptions.py`:
```python
"""
Sistema de exceções personalizadas do CaseBem
Hierarquia clara para diferentes tipos de erro
"""

from typing import Optional, Dict, Any
from enum import Enum

class TipoErro(Enum):
    """Tipos de erro para categorização"""
    VALIDACAO = "VALIDACAO"
    NEGOCIO = "NEGOCIO"
    BANCO_DADOS = "BANCO_DADOS"
    AUTENTICACAO = "AUTENTICACAO"
    AUTORIZACAO = "AUTORIZACAO"
    NAO_ENCONTRADO = "NAO_ENCONTRADO"
    SISTEMA = "SISTEMA"


class CaseBemError(Exception):
    """
    Exceção base do sistema CaseBem.
    Todas as exceções personalizadas herdam desta classe.
    """

    def __init__(
        self,
        mensagem: str,
        tipo_erro: TipoErro = TipoErro.SISTEMA,
        codigo_erro: Optional[str] = None,
        detalhes: Optional[Dict[str, Any]] = None,
        erro_original: Optional[Exception] = None
    ):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.tipo_erro = tipo_erro
        self.codigo_erro = codigo_erro or self.tipo_erro.value
        self.detalhes = detalhes or {}
        self.erro_original = erro_original

    def to_dict(self) -> dict:
        """Converte exceção para dicionário (útil para logs e API)"""
        return {
            "tipo_erro": self.tipo_erro.value,
            "codigo_erro": self.codigo_erro,
            "mensagem": self.mensagem,
            "detalhes": self.detalhes
        }

    def __str__(self) -> str:
        return f"[{self.codigo_erro}] {self.mensagem}"


class ValidacaoError(CaseBemError):
    """Erro de validação de dados"""

    def __init__(self, mensagem: str, campo: Optional[str] = None, valor: Any = None):
        detalhes = {}
        if campo:
            detalhes["campo"] = campo
        if valor is not None:
            detalhes["valor_informado"] = str(valor)

        super().__init__(
            mensagem=mensagem,
            tipo_erro=TipoErro.VALIDACAO,
            codigo_erro="VALIDACAO_ERRO",
            detalhes=detalhes
        )
        self.campo = campo
        self.valor = valor


class RegraDeNegocioError(CaseBemError):
    """Erro de regra de negócio"""

    def __init__(self, mensagem: str, regra: Optional[str] = None):
        super().__init__(
            mensagem=mensagem,
            tipo_erro=TipoErro.NEGOCIO,
            codigo_erro=f"REGRA_NEGOCIO_{regra}" if regra else "REGRA_NEGOCIO",
            detalhes={"regra": regra} if regra else {}
        )


class RecursoNaoEncontradoError(CaseBemError):
    """Erro quando recurso não é encontrado"""

    def __init__(self, recurso: str, identificador: Any = None):
        mensagem = f"{recurso} não encontrado"
        if identificador:
            mensagem += f" (ID: {identificador})"

        super().__init__(
            mensagem=mensagem,
            tipo_erro=TipoErro.NAO_ENCONTRADO,
            codigo_erro="RECURSO_NAO_ENCONTRADO",
            detalhes={"recurso": recurso, "identificador": str(identificador)}
        )


class BancoDadosError(CaseBemError):
    """Erro relacionado ao banco de dados"""

    def __init__(self, mensagem: str, operacao: str = "desconhecida", erro_original: Exception = None):
        super().__init__(
            mensagem=f"Erro de banco de dados: {mensagem}",
            tipo_erro=TipoErro.BANCO_DADOS,
            codigo_erro="BANCO_DADOS_ERRO",
            detalhes={"operacao": operacao},
            erro_original=erro_original
        )


class AutenticacaoError(CaseBemError):
    """Erro de autenticação"""

    def __init__(self, mensagem: str = "Credenciais inválidas"):
        super().__init__(
            mensagem=mensagem,
            tipo_erro=TipoErro.AUTENTICACAO,
            codigo_erro="AUTENTICACAO_ERRO"
        )


class AutorizacaoError(CaseBemError):
    """Erro de autorização"""

    def __init__(self, mensagem: str = "Acesso negado", acao: Optional[str] = None):
        super().__init__(
            mensagem=mensagem,
            tipo_erro=TipoErro.AUTORIZACAO,
            codigo_erro="AUTORIZACAO_ERRO",
            detalhes={"acao": acao} if acao else {}
        )
```

### 2. Criar Sistema de Logging Estruturado

#### `util/logger.py`:
```python
"""
Sistema de logging padronizado do CaseBem
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from .exceptions import CaseBemError, TipoErro

class CaseBemLogger:
    """Logger personalizado para o sistema"""

    def __init__(self, nome: str = "casebem"):
        self.logger = logging.getLogger(nome)
        self._configurar_logger()

    def _configurar_logger(self):
        """Configura o logger com formato padronizado"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _criar_contexto_log(self, **kwargs) -> dict:
        """Cria contexto padronizado para logs"""
        return {
            "timestamp": datetime.now().isoformat(),
            "sistema": "casebem",
            **kwargs
        }

    def info(self, mensagem: str, **contexto):
        """Log de informação"""
        contexto_completo = self._criar_contexto_log(**contexto)
        self.logger.info(f"{mensagem} - {json.dumps(contexto_completo)}")

    def warning(self, mensagem: str, **contexto):
        """Log de aviso"""
        contexto_completo = self._criar_contexto_log(**contexto)
        self.logger.warning(f"{mensagem} - {json.dumps(contexto_completo)}")

    def error(self, mensagem: str, erro: Optional[Exception] = None, **contexto):
        """Log de erro"""
        contexto_completo = self._criar_contexto_log(**contexto)

        if isinstance(erro, CaseBemError):
            contexto_completo.update(erro.to_dict())
        elif erro:
            contexto_completo["erro_original"] = str(erro)
            contexto_completo["tipo_erro_original"] = type(erro).__name__

        self.logger.error(f"{mensagem} - {json.dumps(contexto_completo)}")

    def debug(self, mensagem: str, **contexto):
        """Log de debug"""
        contexto_completo = self._criar_contexto_log(**contexto)
        self.logger.debug(f"{mensagem} - {json.dumps(contexto_completo)}")


# Instância global do logger
logger = CaseBemLogger()
```

### 3. Criar Decoradores para Tratamento de Erros

#### `util/error_handlers.py`:
```python
"""
Decoradores e handlers para tratamento de erros
"""

import functools
import sqlite3
from typing import Callable, Any, Optional, List, Type
from fastapi import Request
from fastapi.templating import Jinja2Templates
from .exceptions import (
    CaseBemError, BancoDadosError, ValidacaoError,
    RecursoNaoEncontradoError, TipoErro
)
from .logger import logger
from .flash_messages import informar_erro

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
                return templates.TemplateResponse(template_erro, {
                    "request": request,
                    "erro": "Ocorreu um erro. Tente novamente."
                })

        return wrapper
    return decorator


def validar_parametros(*tipos_esperados: Type):
    """
    Decorador para validar tipos de parâmetros

    Args:
        *tipos_esperados: Tipos esperados para cada parâmetro
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Validar args
            for i, (arg, tipo_esperado) in enumerate(zip(args, tipos_esperados)):
                if arg is not None and not isinstance(arg, tipo_esperado):
                    raise ValidacaoError(
                        f"Parâmetro {i+1} deve ser do tipo {tipo_esperado.__name__}",
                        campo=f"param_{i+1}",
                        valor=arg
                    )

            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 4. Aplicar no BaseRepo (Fase 1 Atualizada)

#### Atualização de `util/base_repo.py`:
```python
from .error_handlers import tratar_erro_banco_dados
from .exceptions import RecursoNaoEncontradoError, BancoDadosError
from .logger import logger

class BaseRepo:
    # ... código anterior ...

    @tratar_erro_banco_dados("criação de tabela")
    def criar_tabela(self) -> bool:
        """Cria a tabela se não existir"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.CRIAR_TABELA)
            logger.info(f"Tabela {self.nome_tabela} criada/verificada com sucesso")
            return True

    @tratar_erro_banco_dados("inserção de registro")
    def inserir(self, objeto: Any) -> int:
        """Insere um novo registro e retorna o ID"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            valores = self._objeto_para_tupla_insert(objeto)
            cursor.execute(self.sql.INSERIR, valores)
            id_inserido = cursor.lastrowid

            if not id_inserido:
                raise BancoDadosError("Falha ao obter ID do registro inserido", "inserção")

            logger.info(f"Registro inserido em {self.nome_tabela}",
                       id_inserido=id_inserido)
            return id_inserido

    @tratar_erro_banco_dados("obtenção por ID")
    def obter_por_id(self, id: int) -> Any:
        """Obtém um registro pelo ID"""
        if not isinstance(id, int) or id <= 0:
            raise ValidacaoError("ID deve ser um número inteiro positivo", "id", id)

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.OBTER_POR_ID, (id,))
            resultado = cursor.fetchone()

            if not resultado:
                raise RecursoNaoEncontradoError(
                    recurso=self.nome_tabela.title(),
                    identificador=id
                )

            return self._linha_para_objeto(resultado)

    # ... outros métodos com decorador aplicado ...
```

### 5. Aplicar nas Rotas

#### Exemplo em `routes/admin_routes.py`:
```python
from util.error_handlers import tratar_erro_rota
from util.exceptions import RecursoNaoEncontradoError

@router.get("/admin/perfil")
@requer_autenticacao([TipoUsuario.ADMIN.value])
@tratar_erro_rota(template_erro="admin/perfil.html")
async def perfil_admin(request: Request, usuario_logado: dict = None):
    """Página de perfil do administrador"""
    admin = usuario_repo.obter_usuario_por_id(usuario_logado['id'])

    return templates.TemplateResponse("admin/perfil.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "admin": admin,
        "active_page": get_admin_active_page(request)
    })

@router.post("/admin/categorias")
@requer_autenticacao([TipoUsuario.ADMIN.value])
@tratar_erro_rota(redirect_erro="/admin/categorias")
async def criar_categoria(request: Request, categoria_dto: CategoriaDTO):
    """Criar nova categoria"""
    # Validação automática pelo DTO
    categoria = Categoria(
        id=0,
        nome=categoria_dto.nome,
        tipo_fornecimento=categoria_dto.tipo_fornecimento,
        descricao=categoria_dto.descricao,
        ativo=categoria_dto.ativo
    )

    id_categoria = categoria_repo.inserir(categoria)
    logger.info("Categoria criada com sucesso",
               id_categoria=id_categoria, nome=categoria.nome)

    informar_sucesso(request, f"Categoria '{categoria.nome}' criada com sucesso!")
    return RedirectResponse("/admin/categorias", status_code=status.HTTP_302_FOUND)
```

## 📊 Análise de Impacto

### Antes:
- **Try/catch genérico** em 50+ lugares
- **Print statements** para debugging
- **Mensagens inconsistentes** para o usuário
- **Sem logging estruturado**
- **Códigos de erro inexistentes**

### Depois:
- **Exceções tipadas** e organizadas
- **Logging estruturado** com contexto
- **Mensagens de erro padronizadas**
- **Decoradores reutilizáveis**
- **Experiência do usuário melhorada**

## 🎓 Conceitos Ensinados aos Alunos

1. **Hierarquia de Exceções**: Como criar exceções personalizadas
2. **Decoradores**: Padrão para funcionalidades transversais
3. **Logging Estruturado**: Como fazer logs úteis para debugging
4. **Separação de Responsabilidades**: Erro técnico vs erro de negócio
5. **Experiência do Usuário**: Mensagens de erro amigáveis

## 📝 Passo a Passo da Implementação

### Passo 1: Criar Sistema de Exceções
1. Criar `util/exceptions.py` com hierarquia de exceções
2. Criar `util/logger.py` com sistema de logging
3. Testar exceções básicas

### Passo 2: Criar Decoradores
1. Implementar decoradores em `util/error_handlers.py`
2. Testar decoradores isoladamente
3. Documentar uso dos decoradores

### Passo 3: Aplicar no BaseRepo
1. Atualizar BaseRepo com decoradores
2. Remover try/catch genéricos
3. Adicionar validações específicas

### Passo 4: Migrar Rotas Gradualmente
1. Migrar 2-3 rotas piloto
2. Testar funcionamento com usuários reais
3. Migrar todas as rotas restantes

### Passo 5: Configurar Logging
1. Configurar níveis de log por ambiente
2. Adicionar logs estruturados importantes
3. Remover print statements antigos

## ⚠️ Riscos e Mitigações

### Risco 1: Over-engineering
**Mitigação**: Manter simplicidade, usar apenas exceções necessárias

### Risco 2: Performance do logging
**Mitigação**: Usar níveis de log apropriados por ambiente

### Risco 3: Quebrar tratamento existente
**Mitigação**: Migração gradual, mantendo compatibilidade

## ✅ Critérios de Sucesso

- [ ] Sistema de exceções funcionando
- [ ] Logging estruturado implementado
- [ ] Decoradores aplicados no BaseRepo
- [ ] 3+ rotas migradas com sucesso
- [ ] Mensagens de erro amigáveis
- [ ] Redução de print statements

## 🔍 Exemplos de Mensagens de Erro

### Antes:
```
Erro ao criar tabela de usuários: near "AUTOINCREMENT": syntax error
```

### Depois:
```
Para o usuário: "Ocorreu um problema interno. Tente novamente em instantes."
Para o log: {
  "timestamp": "2024-01-15T10:30:00",
  "tipo_erro": "BANCO_DADOS",
  "codigo_erro": "BANCO_DADOS_ERRO",
  "mensagem": "Erro de banco de dados: erro de sintaxe SQL",
  "detalhes": {"operacao": "criação de tabela"},
  "funcao": "criar_tabela_usuarios"
}
```

## 🚀 Próximos Passos

Após completar a Fase 3:
- **Fase 4**: Simplificar estrutura de testes
- **Fase 5**: Limpeza final e organização

## 💬 Exemplo de Explicação para Alunos

> "Imaginem um pronto-socorro: quando chega um paciente, não dizem 'tem algo errado'. Eles classificam: 'fratura no braço', 'dor de cabeça', etc. Cada tipo tem um tratamento específico. É isso que faremos com erros no nosso sistema - classificar para tratar melhor!"