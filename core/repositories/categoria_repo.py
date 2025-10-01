from typing import Optional, List
from core.repositories.base_repo import BaseRepo
from infrastructure.logging import logger
from core.sql import categoria_sql
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento


class CategoriaRepo(BaseRepo):
    """Repositório para operações com categorias"""

    def __init__(self):
        super().__init__("categoria", Categoria, categoria_sql)

    def _objeto_para_tupla_insert(self, categoria: Categoria) -> tuple:
        """Prepara dados da categoria para inserção"""
        return (
            categoria.nome,
            categoria.tipo_fornecimento.value,
            categoria.descricao,
            categoria.ativo,
        )

    def _objeto_para_tupla_update(self, categoria: Categoria) -> tuple:
        """Prepara dados da categoria para atualização"""
        return (
            categoria.nome,
            categoria.tipo_fornecimento.value,
            categoria.descricao,
            categoria.ativo,
            categoria.id,
        )

    def _linha_para_objeto(self, linha: dict) -> Categoria:
        """Converte linha do banco em objeto Categoria"""
        return Categoria(
            id=linha["id"],
            nome=linha["nome"],
            tipo_fornecimento=TipoFornecimento(linha["tipo_fornecimento"]),
            descricao=linha["descricao"],
            ativo=bool(linha["ativo"]),
        )

    def obter_por_tipo(self, tipo: TipoFornecimento) -> List[Categoria]:
        """Método específico: obter categorias por tipo"""
        resultados = self.executar_consulta(
            categoria_sql.OBTER_CATEGORIAS_POR_TIPO, (tipo.value,)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_ativas_por_tipo(self, tipo: TipoFornecimento) -> List[Categoria]:
        """Método específico: obter categorias ativas por tipo"""
        resultados = self.executar_consulta(
            categoria_sql.OBTER_CATEGORIAS_ATIVAS_POR_TIPO, (tipo.value,)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def contar_categorias(self) -> int:
        """Conta o total de categorias no sistema"""
        return self.contar_registros()

    def obter_por_nome(
        self, nome: str, tipo_fornecimento: TipoFornecimento
    ) -> Optional[Categoria]:
        """Busca uma categoria pelo nome e tipo de fornecimento"""
        resultados = self.executar_consulta(
            categoria_sql.OBTER_CATEGORIA_POR_NOME, (nome, tipo_fornecimento.value)
        )
        return self._linha_para_objeto(resultados[0]) if resultados else None

    def buscar_categorias(
        self, busca: str = "", tipo_fornecimento: str = "", status: str = ""
    ) -> List[Categoria]:
        """Busca categorias com filtros"""
        busca_like = f"%{busca}%" if busca else ""
        resultados = self.executar_consulta(
            categoria_sql.BUSCAR_CATEGORIAS,
            (
                busca,
                busca_like,
                busca_like,
                tipo_fornecimento,
                tipo_fornecimento,
                status,
                status,
                status,
            ),
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def ativar_categoria(self, id: int) -> bool:
        """Ativa uma categoria"""
        return self.ativar(id)

    def desativar_categoria(self, id: int) -> bool:
        """Desativa uma categoria"""
        return self.desativar(id)

    def obter_categorias_paginado(
        self, pagina: int, tamanho_pagina: int
    ) -> tuple[List[Categoria], int]:
        """Obtém categorias paginadas e retorna lista de categorias e total"""
        return self.obter_paginado(pagina, tamanho_pagina)

    def buscar_categorias_paginado(
        self,
        busca: str = "",
        tipo_fornecimento: str = "",
        status: str = "",
        pagina: int = 1,
        tamanho_pagina: int = 10,
    ) -> tuple[List[Categoria], int]:
        """Busca categorias paginadas com filtros e retorna lista de categorias e total"""
        offset = (pagina - 1) * tamanho_pagina
        busca_param = f"%{busca}%" if busca else ""

        # Parâmetros seguem a ordem da query: busca, busca_like, busca_like, tipo, tipo, status, status, status
        parametros_count = [
            busca,
            busca_param,
            busca_param,
            tipo_fornecimento,
            tipo_fornecimento,
            status,
            status,
            status,
        ]
        parametros_select = parametros_count + [tamanho_pagina, offset]

        # Contar total usando query parametrizada
        total_resultado = self.executar_consulta(
            categoria_sql.CONTAR_CATEGORIAS_FILTRADAS, parametros_count
        )
        total = total_resultado[0]["total"] if total_resultado else 0

        # Buscar categorias usando query parametrizada
        resultados = self.executar_consulta(
            categoria_sql.BUSCAR_CATEGORIAS, parametros_select
        )
        categorias = [self._linha_para_objeto(row) for row in resultados]

        return categorias, total


# Instância singleton do repositório
categoria_repo = CategoriaRepo()
