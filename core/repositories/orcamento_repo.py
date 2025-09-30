from typing import Optional, List
from core.repositories.base_repo import BaseRepo
from util.exceptions import RecursoNaoEncontradoError
from util.logger import logger
from datetime import datetime
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
        return self.executar_comando(
            orcamento_sql.ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento)
        )

    def atualizar_valor_total(self, id_orcamento: int, valor_total: float) -> bool:
        """Atualiza o valor total de um orçamento"""
        return self.executar_comando(
            orcamento_sql.ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id_orcamento)
        )

    def aceitar_e_rejeitar_outros(self, id_orcamento: int, id_demanda: int) -> bool:
        """Aceita um orçamento e rejeita os outros da mesma demanda"""
        return self.executar_comando(
            orcamento_sql.ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS,
            (id_orcamento, id_demanda),
        )

    def rejeitar(self, id_orcamento: int) -> bool:
        """Rejeita um orçamento"""
        return self.executar_comando(orcamento_sql.REJEITAR_ORCAMENTO, (id_orcamento,))

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
            orcamento_sql.OBTER_ORCAMENTOS_POR_NOIVO, (id_noivo,)
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
        return orcamentos


# Instância singleton do repositório
orcamento_repo = OrcamentoRepo()
