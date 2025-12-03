from typing import List
from core.repositories.base_repo import BaseRepo
from core.sql import orcamento_sql
from core.models.orcamento_model import Orcamento


class OrcamentoRepo(BaseRepo):
    """Repositório para operações com orçamentos"""

    def __init__(self):
        super().__init__("orcamento", Orcamento, orcamento_sql)

    def _objeto_para_tupla_insert(self, orcamento: Orcamento) -> tuple:
        """Prepara dados do orçamento para inserção"""
        return (
            orcamento.id_demanda,
            orcamento.id_fornecedor_prestador,
            orcamento.data_hora_cadastro,
            orcamento.data_hora_validade,
            orcamento.status,
            orcamento.observacoes,
            orcamento.valor_total,
        )

    def _objeto_para_tupla_update(self, orcamento: Orcamento) -> tuple:
        """Prepara dados do orçamento para atualização"""
        return (
            orcamento.data_hora_validade,
            orcamento.status,
            orcamento.observacoes,
            orcamento.valor_total,
            orcamento.id,
        )

    def _linha_para_objeto(self, linha: dict) -> Orcamento:
        """Converte linha do banco em objeto Orcamento"""
        return Orcamento(
            id=linha["id"],
            id_demanda=linha["id_demanda"],
            id_fornecedor_prestador=linha["id_fornecedor_prestador"],
            data_hora_cadastro=linha["data_hora_cadastro"],
            data_hora_validade=linha["data_hora_validade"],
            status=linha["status"],
            observacoes=linha["observacoes"],
            valor_total=linha["valor_total"],
        )

    def atualizar_status(self, id_orcamento: int, status: str) -> bool:
        """Atualiza o status de um orçamento"""
        return self.executar_comando(  # type: ignore[no-any-return]
            orcamento_sql.ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento)
        )

    def atualizar_valor_total(self, id_orcamento: int, valor_total: float) -> bool:
        """Atualiza o valor total de um orçamento"""
        return self.executar_comando(  # type: ignore[no-any-return]
            orcamento_sql.ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id_orcamento)
        )

    def aceitar_e_rejeitar_outros(self, id_orcamento: int, id_demanda: int) -> bool:
        """Aceita um orçamento e rejeita os outros da mesma demanda"""
        return self.executar_comando(  # type: ignore[no-any-return]
            orcamento_sql.ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS,
            (id_orcamento, id_demanda),
        )

    def rejeitar(self, id_orcamento: int) -> bool:
        """Rejeita um orçamento"""
        return self.executar_comando(orcamento_sql.REJEITAR_ORCAMENTO, (id_orcamento,))  # type: ignore[no-any-return]

    def obter_por_demanda(self, id_demanda: int) -> List[Orcamento]:
        """Obtém todos os orçamentos de uma demanda"""
        resultados = self.executar_consulta(
            orcamento_sql.OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_por_fornecedor_prestador(
        self, id_fornecedor_prestador: int
    ) -> List[Orcamento]:
        """Obtém todos os orçamentos de um fornecedor"""
        resultados = self.executar_consulta(
            orcamento_sql.OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR,
            (id_fornecedor_prestador,),
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_por_noivo(self, id_noivo: int) -> List[Orcamento]:
        """Obtém todos os orçamentos relacionados a um noivo"""
        resultados = self.executar_consulta(
            orcamento_sql.OBTER_ORCAMENTOS_POR_NOIVO, (id_noivo, id_noivo)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_por_status(self, status: str) -> List[Orcamento]:
        """Obtém todos os orçamentos com um status específico"""
        resultados = self.executar_consulta(
            orcamento_sql.OBTER_ORCAMENTOS_POR_STATUS, (status,)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_por_pagina(
        self, numero_pagina: int, tamanho_pagina: int
    ) -> List[Orcamento]:
        """Obtém orçamentos com paginação"""
        orcamentos, _ = self.obter_paginado(numero_pagina, tamanho_pagina)
        return orcamentos  # type: ignore[no-any-return]

    def contar_por_demanda(self, id_demanda: int) -> int:
        """Conta quantos orçamentos uma demanda possui"""
        resultado = self.executar_consulta(
            "SELECT COUNT(*) as total FROM orcamento WHERE id_demanda = ?",
            (id_demanda,)
        )
        return resultado[0]["total"] if resultado else 0

    def contar_por_demanda_e_status(self, id_demanda: int, status: str) -> int:
        """Conta quantos orçamentos uma demanda possui com um status específico"""
        resultado = self.executar_consulta(
            "SELECT COUNT(*) as total FROM orcamento WHERE id_demanda = ? AND status = ?",
            (id_demanda, status)
        )
        return resultado[0]["total"] if resultado else 0

    def calcular_status_derivado(self, id_orcamento: int) -> str:
        """
        Calcula o status do orçamento baseado nos status dos seus itens.

        Regras:
        - PENDENTE: Todos os itens estão pendentes
        - ACEITO: Todos os itens estão aceitos
        - REJEITADO: Todos os itens estão rejeitados
        - PARCIALMENTE_ACEITO: Alguns itens aceitos, outros pendentes ou rejeitados

        Returns:
            str: Status calculado do orçamento
        """
        from core.repositories.item_orcamento_repo import item_orcamento_repo

        # Contar itens por status
        total_aceitos = item_orcamento_repo.contar_por_status(id_orcamento, "ACEITO")
        total_rejeitados = item_orcamento_repo.contar_por_status(id_orcamento, "REJEITADO")
        total_pendentes = item_orcamento_repo.contar_por_status(id_orcamento, "PENDENTE")

        total_itens = total_aceitos + total_rejeitados + total_pendentes

        # Se não há itens, mantém como PENDENTE
        if total_itens == 0:
            return "PENDENTE"

        # Todos aceitos
        if total_aceitos == total_itens:
            return "ACEITO"

        # Todos rejeitados
        if total_rejeitados == total_itens:
            return "REJEITADO"

        # Todos pendentes
        if total_pendentes == total_itens:
            return "PENDENTE"

        # Pelo menos um aceito e outros não aceitos
        if total_aceitos > 0:
            return "PARCIALMENTE_ACEITO"

        # Padrão: PENDENTE
        return "PENDENTE"

    def atualizar_status_derivado(self, id_orcamento: int) -> bool:
        """
        Atualiza o status do orçamento baseado nos status dos seus itens.

        Returns:
            bool: True se atualizou com sucesso
        """
        novo_status = self.calcular_status_derivado(id_orcamento)
        return self.atualizar_status(id_orcamento, novo_status)


# Instância singleton do repositório
orcamento_repo = OrcamentoRepo()
