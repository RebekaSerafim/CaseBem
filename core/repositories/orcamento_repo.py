from typing import Optional, List
from util.base_repo import BaseRepo
from util.exceptions import RecursoNaoEncontradoError
from datetime import datetime
from util.database import obter_conexao
from core.sql import orcamento_sql
from core.models.orcamento_model import Orcamento

class OrcamentoRepo(BaseRepo):
    """Repositório para operações com orçamentos"""

    def __init__(self):
        super().__init__('orcamento', Orcamento, orcamento_sql)

    def _objeto_para_tupla_insert(self, orcamento: Orcamento) -> tuple:
        """Prepara dados do orçamento para inserção"""
        return (
            orcamento.id_demanda,
            orcamento.id_fornecedor_prestador,
            orcamento.data_hora_cadastro,
            orcamento.data_hora_validade,
            orcamento.status,
            orcamento.observacoes,
            orcamento.valor_total
        )

    def _objeto_para_tupla_update(self, orcamento: Orcamento) -> tuple:
        """Prepara dados do orçamento para atualização"""
        return (
            orcamento.data_hora_validade,
            orcamento.status,
            orcamento.observacoes,
            orcamento.valor_total,
            orcamento.id
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
            valor_total=linha["valor_total"]
        )

    def atualizar_status(self, id_orcamento: int, status: str) -> bool:
        """Atualiza o status de um orçamento"""
        try:
            return self.executar_comando(orcamento_sql.ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento))
        except Exception as e:
            print(f"Erro ao atualizar status do orçamento: {e}")
            return False

    def atualizar_valor_total(self, id_orcamento: int, valor_total: float) -> bool:
        """Atualiza o valor total de um orçamento"""
        try:
            return self.executar_comando(orcamento_sql.ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id_orcamento))
        except Exception as e:
            print(f"Erro ao atualizar valor total do orçamento: {e}")
            return False

    def aceitar_e_rejeitar_outros(self, id_orcamento: int, id_demanda: int) -> bool:
        """Aceita um orçamento e rejeita os outros da mesma demanda"""
        try:
            return self.executar_comando(orcamento_sql.ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))
        except Exception as e:
            print(f"Erro ao aceitar orçamento: {e}")
            return False

    def rejeitar(self, id_orcamento: int) -> bool:
        """Rejeita um orçamento"""
        try:
            return self.executar_comando(orcamento_sql.REJEITAR_ORCAMENTO, (id_orcamento,))
        except Exception as e:
            print(f"Erro ao rejeitar orçamento: {e}")
            return False

    def obter_por_demanda(self, id_demanda: int) -> List[Orcamento]:
        """Obtém todos os orçamentos de uma demanda"""
        try:
            resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter orçamentos por demanda: {e}")
            return []

    def obter_por_fornecedor_prestador(self, id_fornecedor_prestador: int) -> List[Orcamento]:
        """Obtém todos os orçamentos de um fornecedor"""
        try:
            resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR, (id_fornecedor_prestador,))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter orçamentos por fornecedor: {e}")
            return []

    def obter_por_noivo(self, id_noivo: int) -> List[Orcamento]:
        """Obtém todos os orçamentos relacionados a um noivo"""
        try:
            resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_NOIVO, (id_noivo,))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter orçamentos por noivo: {e}")
            return []

    def obter_por_status(self, status: str) -> List[Orcamento]:
        """Obtém todos os orçamentos com um status específico"""
        try:
            resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_STATUS, (status,))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter orçamentos por status: {e}")
            return []

    def obter_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Orcamento]:
        """Obtém orçamentos com paginação"""
        try:
            limite = tamanho_pagina
            offset = (numero_pagina - 1) * tamanho_pagina
            resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_PAGINA, (limite, offset))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter orçamentos por página: {e}")
            return []

    def contar(self) -> int:
        """Conta o total de orçamentos"""
        try:
            resultados = self.executar_query("SELECT COUNT(*) as total FROM orcamento")
            return resultados[0]["total"] if resultados else 0
        except Exception as e:
            print(f"Erro ao contar orçamentos: {e}")
            return 0

# Instância singleton do repositório
orcamento_repo = OrcamentoRepo()