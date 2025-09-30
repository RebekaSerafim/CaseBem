from typing import Optional, List
from util.base_repo import BaseRepo
from util.error_handlers import tratar_erro_banco_dados
from util.logger import logger
from core.sql import categoria_sql
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento

class CategoriaRepo(BaseRepo):
    """Repositório para operações com categorias"""

    def __init__(self):
        super().__init__('categoria', Categoria, categoria_sql)

    def _objeto_para_tupla_insert(self, categoria: Categoria) -> tuple:
        """Prepara dados da categoria para inserção"""
        return (
            categoria.nome,
            categoria.tipo_fornecimento.value,
            categoria.descricao,
            categoria.ativo
        )

    def _objeto_para_tupla_update(self, categoria: Categoria) -> tuple:
        """Prepara dados da categoria para atualização"""
        return (
            categoria.nome,
            categoria.tipo_fornecimento.value,
            categoria.descricao,
            categoria.ativo,
            categoria.id
        )

    def _linha_para_objeto(self, linha: dict) -> Categoria:
        """Converte linha do banco em objeto Categoria"""
        return Categoria(
            id=linha["id"],
            nome=linha["nome"],
            tipo_fornecimento=TipoFornecimento(linha["tipo_fornecimento"]),
            descricao=linha["descricao"],
            ativo=bool(linha["ativo"])
        )

    def obter_por_tipo(self, tipo: TipoFornecimento) -> List[Categoria]:
        """Método específico: obter categorias por tipo"""
        resultados = self.executar_query(
            categoria_sql.OBTER_CATEGORIAS_POR_TIPO,
            (tipo.value,)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_por_tipo_ativas(self, tipo: TipoFornecimento) -> List[Categoria]:
        """Método específico: obter categorias ativas por tipo"""
        resultados = self.executar_query(
            categoria_sql.OBTER_CATEGORIAS_POR_TIPO_ATIVAS,
            (tipo.value,)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    @tratar_erro_banco_dados("contagem de categorias")
    def contar_categorias(self) -> int:
        """Conta o total de categorias no sistema"""
        resultados = self.executar_query("SELECT COUNT(*) as total FROM categoria")
        total = resultados[0]["total"] if resultados else 0
        logger.info("Contagem de categorias realizada", total_categorias=total)
        return total

    def obter_por_nome(self, nome: str, tipo_fornecimento: TipoFornecimento) -> Optional[Categoria]:
        """Busca uma categoria pelo nome e tipo de fornecimento"""
        resultados = self.executar_query(
            categoria_sql.OBTER_CATEGORIA_POR_NOME,
            (nome, tipo_fornecimento.value)
        )
        return self._linha_para_objeto(resultados[0]) if resultados else None

    def buscar_categorias(self, busca: str = "", tipo_fornecimento: str = "", status: str = "") -> List[Categoria]:
        """Busca categorias com filtros"""
        busca_like = f"%{busca}%" if busca else ""
        resultados = self.executar_query(
            categoria_sql.BUSCAR_CATEGORIAS,
            (busca, busca_like, busca_like, tipo_fornecimento, tipo_fornecimento, status, status, status)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def ativar_categoria(self, id: int) -> bool:
        """Ativa uma categoria"""
        return self.executar_comando(categoria_sql.ATIVAR_CATEGORIA, (id,))

    def desativar_categoria(self, id: int) -> bool:
        """Desativa uma categoria"""
        return self.executar_comando(categoria_sql.DESATIVAR_CATEGORIA, (id,))

    def obter_categorias_paginado(self, pagina: int, tamanho_pagina: int) -> tuple[List[Categoria], int]:
        """Obtém categorias paginadas e retorna lista de categorias e total"""
        return self.obter_paginado(pagina, tamanho_pagina)

    def buscar_categorias_paginado(self, busca: str = "", tipo_fornecimento: str = "", status: str = "", pagina: int = 1, tamanho_pagina: int = 10) -> tuple[List[Categoria], int]:
        """Busca categorias paginadas com filtros e retorna lista de categorias e total"""
        try:
            condicoes = []
            parametros = []

            if busca:
                condicoes.append("(nome LIKE ? OR descricao LIKE ?)")
                busca_param = f"%{busca}%"
                parametros.extend([busca_param, busca_param])

            if tipo_fornecimento:
                condicoes.append("tipo_fornecimento = ?")
                parametros.append(tipo_fornecimento)

            if status == "ativo":
                condicoes.append("ativo = 1")
            elif status == "inativo":
                condicoes.append("ativo = 0")

            where_clause = "WHERE " + " AND ".join(condicoes) if condicoes else ""

            # Contar total
            sql_count = f"SELECT COUNT(*) as total FROM categoria {where_clause}"
            total_resultado = self.executar_query(sql_count, parametros[:])
            total = total_resultado[0]["total"] if total_resultado else 0

            # Buscar categorias da página
            offset = (pagina - 1) * tamanho_pagina
            sql_select = f"SELECT * FROM categoria {where_clause} ORDER BY id DESC LIMIT ? OFFSET ?"
            resultados = self.executar_query(sql_select, parametros + [tamanho_pagina, offset])

            categorias = [self._linha_para_objeto(row) for row in resultados]
            return categorias, total
        except Exception as e:
            print(f"Erro ao buscar categorias paginadas: {e}")
            return [], 0

# Instância singleton do repositório
categoria_repo = CategoriaRepo()