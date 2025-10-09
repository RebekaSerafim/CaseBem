from typing import Optional, List
from core.repositories.base_repo import BaseRepo
from infrastructure.logging import logger
from core.sql import item_orcamento_sql
from core.models.item_orcamento_model import ItemOrcamento


class ItemOrcamentoRepo(BaseRepo):
    """
    Repositório para operações com item_orcamento.

    V2: Agora usa id auto-increment como PK, não mais chave composta.
    Vincula orçamento -> item_demanda -> item do catálogo.
    """

    def __init__(self):
        super().__init__(
            nome_tabela="item_orcamento",
            model_class=ItemOrcamento,
            sql_module=item_orcamento_sql,
        )

    def _objeto_para_tupla_insert(self, item_orcamento: ItemOrcamento) -> tuple:
        """Converte objeto ItemOrcamento em tupla para INSERT"""
        return (
            item_orcamento.id_orcamento,
            item_orcamento.id_item_demanda,
            item_orcamento.id_item,
            item_orcamento.quantidade,
            item_orcamento.preco_unitario,
            item_orcamento.observacoes,
            item_orcamento.desconto,
            item_orcamento.status,
            item_orcamento.motivo_rejeicao,
        )

    def _objeto_para_tupla_update(self, item_orcamento: ItemOrcamento) -> tuple:
        """Converte objeto ItemOrcamento em tupla para UPDATE"""
        return (
            item_orcamento.id_item_demanda,
            item_orcamento.id_item,
            item_orcamento.quantidade,
            item_orcamento.preco_unitario,
            item_orcamento.observacoes,
            item_orcamento.desconto,
            item_orcamento.status,
            item_orcamento.motivo_rejeicao,
            item_orcamento.id,
        )

    def _linha_para_objeto(self, linha: dict) -> ItemOrcamento:
        """Converte linha do banco em objeto ItemOrcamento"""
        return ItemOrcamento(
            id=linha["id"],
            id_orcamento=linha["id_orcamento"],
            id_item_demanda=linha["id_item_demanda"],
            id_item=linha["id_item"],
            quantidade=linha["quantidade"],
            preco_unitario=linha["preco_unitario"],
            observacoes=self._safe_get(linha, "observacoes"),
            desconto=self._safe_get(linha, "desconto"),
            status=self._safe_get(linha, "status", "PENDENTE"),
            motivo_rejeicao=self._safe_get(linha, "motivo_rejeicao"),
        )

    def obter_por_orcamento(self, id_orcamento: int) -> List[dict]:
        """
        Obtém todos os itens de um orçamento com dados enriquecidos.

        Retorna dicts com informações do item, item_demanda e categoria.
        """
        resultados = self.executar_consulta(
            item_orcamento_sql.OBTER_ITENS_POR_ORCAMENTO, (id_orcamento,)
        )
        return [dict(resultado) for resultado in resultados]

    def obter_por_item_demanda(self, id_orcamento: int, id_item_demanda: int) -> List[dict]:
        """
        Obtém todos os itens de orçamento para um item_demanda específico.

        Usado para mostrar múltiplas opções do fornecedor para o mesmo item solicitado.
        """
        resultados = self.executar_consulta(
            item_orcamento_sql.OBTER_ITENS_POR_ITEM_DEMANDA,
            (id_orcamento, id_item_demanda)
        )
        return [dict(resultado) for resultado in resultados]

    def verificar_item_ja_usado(
        self, id_orcamento: int, id_item_demanda: int, id_item: int
    ) -> bool:
        """
        Verifica se um item já foi usado para um item_demanda específico no orçamento.

        Evita duplicatas: mesmo item não pode ser proposto duas vezes para o mesmo item_demanda.
        """
        resultados = self.executar_consulta(
            item_orcamento_sql.VERIFICAR_ITEM_JA_USADO,
            (id_orcamento, id_item_demanda, id_item)
        )
        return resultados[0]["count"] > 0 if resultados else False

    def obter_itens_usados(self, id_orcamento: int, id_item_demanda: int) -> List[int]:
        """
        Retorna lista de IDs de itens já usados para um item_demanda no orçamento.

        Usado para filtrar select e impedir seleção de itens duplicados.
        """
        resultados = self.executar_consulta(
            item_orcamento_sql.OBTER_ITENS_USADOS_PARA_ITEM_DEMANDA,
            (id_orcamento, id_item_demanda)
        )
        return [row["id_item"] for row in resultados]

    def obter_total_orcamento(self, id_orcamento: int) -> float:
        """Calcula o total de um orçamento"""
        resultados = self.executar_consulta(
            item_orcamento_sql.OBTER_TOTAL_ORCAMENTO, (id_orcamento,)
        )
        if resultados and resultados[0]["total"]:
            return resultados[0]["total"]  # type: ignore[no-any-return]
        return 0.0

    def excluir_por_orcamento(self, id_orcamento: int) -> bool:
        """Exclui todos os itens de um orçamento"""
        return self.executar_comando(  # type: ignore[no-any-return]
            item_orcamento_sql.EXCLUIR_ITENS_POR_ORCAMENTO, (id_orcamento,)
        )

    def atualizar_status_item(self, id_item_orcamento: int, status: str, motivo_rejeicao: Optional[str] = None) -> bool:
        """
        Atualiza o status de um item do orçamento.

        Args:
            id_item_orcamento: ID do item
            status: Novo status (PENDENTE, ACEITO, REJEITADO)
            motivo_rejeicao: Motivo da rejeição (obrigatório se status = REJEITADO)

        Returns:
            bool: True se atualizado com sucesso
        """
        if motivo_rejeicao:
            # Atualizar com motivo
            return self.executar_comando(  # type: ignore[no-any-return]
                item_orcamento_sql.ATUALIZAR_STATUS_COM_MOTIVO,
                (status, motivo_rejeicao, id_item_orcamento)
            )
        else:
            # Atualizar apenas status
            return self.executar_comando(  # type: ignore[no-any-return]
                item_orcamento_sql.ATUALIZAR_STATUS_ITEM, (status, id_item_orcamento)
            )

    def obter_por_status(self, id_orcamento: int, status: str) -> List[dict]:
        """Obtém todos os itens de um orçamento com status específico"""
        resultados = self.executar_consulta(
            item_orcamento_sql.OBTER_ITENS_POR_STATUS, (id_orcamento, status)
        )
        return [dict(resultado) for resultado in resultados]

    def contar_por_status(self, id_orcamento: int, status: str) -> int:
        """Conta quantos itens de um orçamento têm um status específico"""
        resultados = self.executar_consulta(
            item_orcamento_sql.CONTAR_ITENS_POR_STATUS, (id_orcamento, status)
        )
        return resultados[0]["total"] if resultados else 0

    def contar_por_item_demanda(self, id_item_demanda: int) -> int:
        """Conta quantos item_orcamento existem para um item_demanda específico"""
        resultados = self.executar_consulta(
            "SELECT COUNT(*) as total FROM item_orcamento WHERE id_item_demanda = ?",
            (id_item_demanda,)
        )
        return resultados[0]["total"] if resultados else 0

    def verificar_item_demanda_ja_aceito(self, id_item_demanda: int) -> bool:
        """
        Verifica se já existe um item aceito para este item_demanda.

        REGRA DE NEGÓCIO: Não pode aceitar dois orçamentos para o mesmo item_demanda.
        Um noivo pode aceitar itens de diferentes fornecedores, mas apenas um item
        por item_demanda.
        """
        resultados = self.executar_consulta(
            item_orcamento_sql.VERIFICAR_ITEM_DEMANDA_JA_ACEITO, (id_item_demanda,)
        )
        return (resultados[0]["count"] > 0) if resultados else False


# Instância singleton do repositório
item_orcamento_repo = ItemOrcamentoRepo()
