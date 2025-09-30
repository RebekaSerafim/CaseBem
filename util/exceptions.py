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

    def __init__(self, mensagem: str, operacao: str = "desconhecida", erro_original: Optional[Exception] = None):
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