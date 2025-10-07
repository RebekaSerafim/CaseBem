"""
Classe base para todos os DTOs do sistema CaseBem.
Fornece configurações padrão e métodos de validação comuns.
"""

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Dict, Any, Callable, TypeVar
from util.validacoes_dto import ValidacaoError

T = TypeVar('T')


class BaseDTO(BaseModel):
    """
    Classe base para todos os DTOs do sistema.
    Fornece configurações padrão e métodos de validação comuns.

    Esta classe implementa:
    - Configurações padrão do Pydantic
    - Wrapper para tratamento de erros de validação
    - Métodos auxiliares para conversão de dados
    """

    model_config = ConfigDict(
        # Remover espaços em branco automaticamente
        str_strip_whitespace=True,
        # Validar na atribuição também (não só na criação)
        validate_assignment=True,
        # Usar valores dos enums ao invés dos objetos
        use_enum_values=True,
        # Permitir population by name (útil para formulários HTML)
        populate_by_name=True,
        # Validar valores padrão também
        validate_default=True
    )

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> Dict[str, Any]:
        """
        Cria um exemplo JSON para documentação da API.
        Pode ser sobrescrito nas classes filhas.

        Args:
            **overrides: Valores específicos para sobrescrever no exemplo

        Returns:
            Dict com exemplo de dados para este DTO
        """
        return {"exemplo": "Sobrescrever na classe filha", **overrides}

    @classmethod
    def validar_campo_wrapper(cls, validador_func: Callable[..., T], campo_nome: str = "") -> Callable[..., T]:
        """
        Wrapper para padronizar o tratamento de erros de validação.
        Evita repetir try/except em cada field_validator.

        Args:
            validador_func: Função de validação a ser envolvida
            campo_nome: Nome do campo para mensagens de erro

        Returns:
            Função wrapper que trata os erros automaticamente
        """
        def wrapper(valor: Any, **kwargs: Any) -> T:
            try:
                if campo_nome:
                    return validador_func(valor, campo_nome, **kwargs)
                else:
                    return validador_func(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return wrapper

    def to_dict(self) -> dict:
        """
        Converte DTO para dicionário simples.
        Remove campos None para limpar o retorno.

        Returns:
            Dicionário com os dados do DTO
        """
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        """
        Converte DTO para JSON.
        Remove campos None para limpar o retorno.

        Returns:
            String JSON com os dados do DTO
        """
        return self.model_dump_json(exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria DTO a partir de dicionário.

        Args:
            data: Dicionário com os dados

        Returns:
            Instância do DTO
        """
        return cls(**data)

    def __str__(self) -> str:
        """Representação string melhorada do DTO"""
        campos = ', '.join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"{self.__class__.__name__}({campos})"

    def __repr__(self) -> str:
        """Representação técnica do DTO"""
        return self.__str__()