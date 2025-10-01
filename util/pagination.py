"""
Helper de paginação para o sistema CaseBem.

Centraliza lógica de paginação que estava duplicada em múltiplas rotas.
"""

from typing import List, Any, Optional, Dict
from dataclasses import dataclass
from fastapi import Request
import math


@dataclass
class PageInfo:
    """Informações de paginação"""
    items: List[Any]
    total_items: int
    current_page: int
    total_pages: int
    page_size: int
    has_previous: bool
    has_next: bool

    @property
    def start_item(self) -> int:
        """Número do primeiro item da página (para exibição)"""
        if self.total_items == 0:
            return 0
        return (self.current_page - 1) * self.page_size + 1

    @property
    def end_item(self) -> int:
        """Número do último item da página (para exibição)"""
        end = self.current_page * self.page_size
        return min(end, self.total_items)

    @property
    def previous_page(self) -> int:
        """Número da página anterior"""
        return max(1, self.current_page - 1)

    @property
    def next_page(self) -> int:
        """Número da próxima página"""
        return min(self.total_pages, self.current_page + 1)

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário (útil para templates)"""
        return {
            'items': self.items,
            'total_items': self.total_items,
            'current_page': self.current_page,
            'total_pages': self.total_pages,
            'page_size': self.page_size,
            'has_previous': self.has_previous,
            'has_next': self.has_next,
            'start_item': self.start_item,
            'end_item': self.end_item,
            'previous_page': self.previous_page,
            'next_page': self.next_page,
        }


class PaginationHelper:
    """Helper para paginação consistente em todo o sistema"""

    # Tamanhos de página padrão
    DEFAULT_PAGE_SIZE = 10
    PUBLIC_PAGE_SIZE = 12  # Para listagens públicas (mais visual)
    MAX_PAGE_SIZE = 100  # Limite máximo para evitar sobrecarga

    @staticmethod
    def paginate(
        items: List[Any],
        total: int,
        page: int = 1,
        page_size: Optional[int] = None
    ) -> PageInfo:
        """
        Cria objeto de paginação com informações completas.

        Args:
            items: Itens da página atual
            total: Total de itens disponíveis
            page: Número da página atual (começa em 1)
            page_size: Tamanho da página (usa DEFAULT_PAGE_SIZE se None)

        Returns:
            PageInfo: Objeto com informações de paginação

        Examples:
            >>> usuarios = usuario_repo.obter_paginado(pagina=2, tamanho=10)
            >>> total = usuario_repo.contar()
            >>> page_info = PaginationHelper.paginate(usuarios, total, page=2, page_size=10)
            >>> print(f"Exibindo {page_info.start_item}-{page_info.end_item} de {page_info.total_items}")
        """
        if page_size is None:
            page_size = PaginationHelper.DEFAULT_PAGE_SIZE

        # Validar page_size
        page_size = min(page_size, PaginationHelper.MAX_PAGE_SIZE)
        page_size = max(1, page_size)

        # Calcular total de páginas
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # Validar página atual
        page = max(1, min(page, total_pages))

        return PageInfo(
            items=items,
            total_items=total,
            current_page=page,
            total_pages=total_pages,
            page_size=page_size,
            has_previous=page > 1,
            has_next=page < total_pages
        )

    @staticmethod
    def extract_filters(
        request: Request,
        allowed_filters: List[str],
        strip: bool = True
    ) -> Dict[str, str]:
        """
        Extrai filtros da query string de forma segura.

        Args:
            request: Request do FastAPI
            allowed_filters: Lista de nomes de filtros permitidos
            strip: Se True, remove espaços em branco dos valores

        Returns:
            Dict[str, str]: Dicionário com filtros extraídos (apenas não-vazios)

        Examples:
            >>> filters = PaginationHelper.extract_filters(
            ...     request,
            ...     ['search', 'tipo', 'status', 'categoria']
            ... )
            >>> # filters = {'search': 'teste', 'tipo': 'produto'}
        """
        filters = {}
        for filter_name in allowed_filters:
            value = request.query_params.get(filter_name, "")
            if strip:
                value = value.strip()
            if value:  # Só adiciona se não for vazio
                filters[filter_name] = value
        return filters

    @staticmethod
    def get_page_number(request: Request, default: int = 1) -> int:
        """
        Extrai número da página da query string.

        Args:
            request: Request do FastAPI
            default: Valor padrão se não especificado ou inválido

        Returns:
            int: Número da página (mínimo 1)

        Examples:
            >>> page = PaginationHelper.get_page_number(request)
        """
        try:
            page = int(request.query_params.get("page", default))
            return max(1, page)  # Mínimo 1
        except (ValueError, TypeError):
            return default

    @staticmethod
    def build_pagination_links(
        request: Request,
        page_info: PageInfo,
        preserve_filters: bool = True
    ) -> Dict[str, Optional[str]]:
        """
        Constrói URLs de paginação mantendo filtros.

        Args:
            request: Request do FastAPI
            page_info: Informações de paginação
            preserve_filters: Se True, mantém filtros na URL

        Returns:
            Dict[str, str]: Dicionário com URLs (first, previous, next, last)

        Examples:
            >>> links = PaginationHelper.build_pagination_links(request, page_info)
            >>> # links = {
            >>> #     'first': '/admin/usuarios?search=joao&page=1',
            >>> #     'next': '/admin/usuarios?search=joao&page=3',
            >>> #     ...
            >>> # }
        """
        base_url = str(request.url.path)
        params = dict(request.query_params)

        # Remove 'page' dos params para adicionar depois
        params.pop('page', None)

        def build_url(page: int) -> str:
            """Constrói URL com número de página"""
            if preserve_filters and params:
                query = "&".join([f"{k}={v}" for k, v in params.items()])
                return f"{base_url}?{query}&page={page}"
            return f"{base_url}?page={page}"

        return {
            'first': build_url(1),
            'previous': build_url(page_info.previous_page) if page_info.has_previous else None,
            'next': build_url(page_info.next_page) if page_info.has_next else None,
            'last': build_url(page_info.total_pages),
        }
