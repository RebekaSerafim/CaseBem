from typing import Optional, List, Dict, Any
from core.repositories.base_repo import BaseRepo
from infrastructure.logging import logger
from core.sql import item_demanda_sql
from core.models.item_demanda_model import ItemDemanda
from core.models.tipo_fornecimento_model import TipoFornecimento


class ItemDemandaRepo(BaseRepo):
    """
    Repositório para operações com item_demanda.

    REFATORAÇÃO V2: ItemDemanda agora tem PK própria (id auto-increment).
    Não é mais uma tabela de relacionamento com chave composta.
    Representa descrições livres do que o noivo quer, não itens específicos.
    """

    def __init__(self) -> None:
        super().__init__(
            nome_tabela="item_demanda",
            model_class=ItemDemanda,
            sql_module=item_demanda_sql,
        )

    def _objeto_para_tupla_insert(self, item_demanda: ItemDemanda) -> tuple:
        """Converte objeto ItemDemanda em tupla para INSERT"""
        return (
            item_demanda.id_demanda,
            item_demanda.tipo.value if isinstance(item_demanda.tipo, TipoFornecimento) else item_demanda.tipo,
            item_demanda.id_categoria,
            item_demanda.descricao,
            item_demanda.quantidade,
            item_demanda.preco_maximo,
            item_demanda.observacoes,
        )

    def _objeto_para_tupla_update(self, item_demanda: ItemDemanda) -> tuple:
        """Converte objeto ItemDemanda em tupla para UPDATE"""
        return (
            item_demanda.tipo.value if isinstance(item_demanda.tipo, TipoFornecimento) else item_demanda.tipo,
            item_demanda.id_categoria,
            item_demanda.descricao,
            item_demanda.quantidade,
            item_demanda.preco_maximo,
            item_demanda.observacoes,
            item_demanda.id,
        )

    def _linha_para_objeto(self, linha: dict) -> ItemDemanda:
        """Converte linha do banco em objeto ItemDemanda"""
        return ItemDemanda(
            id=linha["id"],
            id_demanda=linha["id_demanda"],
            tipo=linha["tipo"],  # __post_init__ converte string para enum
            id_categoria=linha["id_categoria"],
            descricao=linha["descricao"],
            quantidade=linha["quantidade"],
            preco_maximo=self._safe_get(linha, "preco_maximo"),
            observacoes=self._safe_get(linha, "observacoes"),
        )

    def obter_por_demanda(self, id_demanda: int) -> List[Dict[str, Any]]:
        """
        Obtém todos os itens de uma demanda com dados enriquecidos.

        Retorna dicts com campos extras como categoria_nome.
        """
        resultados = self.executar_consulta(
            item_demanda_sql.OBTER_ITENS_POR_DEMANDA, (id_demanda,)
        )
        return [dict(resultado) for resultado in resultados]

    def obter_por_tipo_e_categoria(
        self, tipo: str, id_categoria: int
    ) -> List[Dict[str, Any]]:
        """
        Obtém itens de demanda de um determinado tipo e categoria.

        Usado por fornecedores para encontrar demandas compatíveis.
        """
        resultados = self.executar_consulta(
            item_demanda_sql.OBTER_POR_TIPO_E_CATEGORIA, (tipo, id_categoria)
        )
        return [dict(resultado) for resultado in resultados]

    def obter_demandas_compativeis_com_fornecedor(
        self, categorias_fornecedor: List[int]
    ) -> List[int]:
        """
        Retorna IDs de demandas que têm itens compatíveis com as categorias do fornecedor.

        Args:
            categorias_fornecedor: Lista de IDs de categorias que o fornecedor atende

        Returns:
            Lista de IDs de demandas compatíveis
        """
        if not categorias_fornecedor:
            return []

        # Criar placeholders para IN clause
        placeholders = ",".join(["?" for _ in categorias_fornecedor])
        query = item_demanda_sql.OBTER_DEMANDAS_COM_ITENS_COMPATIVEIS.format(
            categorias_placeholder=placeholders
        )

        # Executar query para cada tipo de fornecimento
        ids_demandas: set[int] = set()
        for tipo in TipoFornecimento:
            params = [tipo.value] + categorias_fornecedor
            resultados = self.executar_consulta(query, tuple(params))
            ids_demandas.update(row["id_demanda"] for row in resultados)

        return list(ids_demandas)

    def excluir_por_demanda(self, id_demanda: int) -> bool:
        """Exclui todos os itens de uma demanda"""
        return self.executar_comando(  # type: ignore[no-any-return]
            item_demanda_sql.EXCLUIR_ITENS_POR_DEMANDA, (id_demanda,)
        )

    def contar_por_demanda(self, id_demanda: int) -> int:
        """Conta quantos itens uma demanda possui"""
        resultado = self.executar_consulta(
            item_demanda_sql.CONTAR_POR_DEMANDA, (id_demanda,)
        )
        return resultado[0]["total"] if resultado else 0


# Instância singleton do repositório
item_demanda_repo = ItemDemandaRepo()
