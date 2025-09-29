from typing import Optional, List
from datetime import datetime
from util.base_repo import BaseRepo
from sql import orcamento_sql
from model.orcamento_model import Orcamento

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
        linha_dict = dict(linha) if hasattr(linha, 'keys') else linha

        return Orcamento(
            id=linha_dict["id"],
            id_demanda=linha_dict["id_demanda"],
            id_fornecedor_prestador=linha_dict["id_fornecedor_prestador"],
            data_hora_cadastro=linha_dict["data_hora_cadastro"],
            data_hora_validade=linha_dict.get("data_hora_validade"),
            status=linha_dict.get("status", "PENDENTE"),
            observacoes=linha_dict.get("observacoes"),
            valor_total=linha_dict.get("valor_total")
        )

    def atualizar_status_orcamento(self, id: int, status: str) -> bool:
        """Atualiza apenas o status de um orçamento"""
        return self.executar_comando(orcamento_sql.ATUALIZAR_STATUS_ORCAMENTO, (status, id))

    def atualizar_valor_total_orcamento(self, id: int, valor_total: float) -> bool:
        """Atualiza apenas o valor total de um orçamento"""
        return self.executar_comando(orcamento_sql.ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id))

    def obter_orcamentos_por_demanda(self, id_demanda: int) -> List[Orcamento]:
        """Obtém todos os orçamentos de uma demanda"""
        resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,))
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_orcamentos_por_fornecedor(self, id_fornecedor: int) -> List[Orcamento]:
        """Obtém todos os orçamentos de um fornecedor"""
        resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR, (id_fornecedor,))
        return [self._linha_para_objeto(row) for row in resultados]

# Instância global do repositório
orcamento_repo = OrcamentoRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_orcamento() -> bool:
    return orcamento_repo.criar_tabela()

def inserir_orcamento(orcamento: Orcamento) -> Optional[int]:
    return orcamento_repo.inserir(orcamento)

def atualizar_orcamento(orcamento: Orcamento) -> bool:
    return orcamento_repo.atualizar(orcamento)

def excluir_orcamento(id: int) -> bool:
    return orcamento_repo.excluir(id)

def obter_orcamento_por_id(id: int) -> Optional[Orcamento]:
    return orcamento_repo.obter_por_id(id)

def listar_orcamentos() -> List[Orcamento]:
    return orcamento_repo.listar_todos()

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    return orcamento_repo.atualizar_status_orcamento(id_orcamento, status)

def atualizar_valor_total_orcamento(id_orcamento: int, valor_total: float) -> bool:
    return orcamento_repo.atualizar_valor_total_orcamento(id_orcamento, valor_total)

def obter_orcamentos_por_demanda(id_demanda: int) -> List[Orcamento]:
    return orcamento_repo.obter_orcamentos_por_demanda(id_demanda)

def obter_orcamentos_por_fornecedor_prestador(id_fornecedor: int) -> List[Orcamento]:
    return orcamento_repo.obter_orcamentos_por_fornecedor(id_fornecedor)

def obter_orcamentos_por_noivo(id_noivo: int) -> List[Orcamento]:
    """Obtém todos os orçamentos relacionados a um noivo através das demandas do seu casal"""
    resultados = orcamento_repo.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_NOIVO, (id_noivo,))
    return [orcamento_repo._linha_para_objeto(row) for row in resultados]

def obter_orcamentos_por_status(status: str) -> List[Orcamento]:
    """Obtém todos os orçamentos com um status específico"""
    resultados = orcamento_repo.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_STATUS, (status,))
    return [orcamento_repo._linha_para_objeto(row) for row in resultados]

def obter_orcamentos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Orcamento]:
    """Lista orçamentos com paginação"""
    limite = tamanho_pagina
    offset = (numero_pagina - 1) * tamanho_pagina
    resultados = orcamento_repo.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_PAGINA, (limite, offset))
    return [orcamento_repo._linha_para_objeto(row) for row in resultados]

def aceitar_orcamento_e_rejeitar_outros(id_orcamento: int, id_demanda: int) -> bool:
    """Aceita um orçamento específico e rejeita todos os outros da mesma demanda"""
    return orcamento_repo.executar_comando(orcamento_sql.ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))

def rejeitar_orcamento(id_orcamento: int) -> bool:
    """Rejeita um orçamento específico"""
    return orcamento_repo.executar_comando(orcamento_sql.REJEITAR_ORCAMENTO, (id_orcamento,))

def contar_orcamentos() -> int:
    """Conta o total de orçamentos no sistema"""
    return orcamento_repo.contar_registros()
