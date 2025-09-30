from typing import Optional, List, Union
from datetime import datetime
from util.base_repo import BaseRepo
from util.exceptions import RecursoNaoEncontradoError
from util.logger import logger
from core.sql import demanda_sql
from core.models.demanda_model import Demanda, StatusDemanda

class DemandaRepo(BaseRepo):
    """Repositório para operações com demandas"""

    def __init__(self):
        super().__init__('demanda', Demanda, demanda_sql)

    def _objeto_para_tupla_insert(self, demanda: Demanda) -> tuple:
        """Prepara dados da demanda para inserção"""
        return (
            demanda.id_casal,
            demanda.id_categoria,
            demanda.titulo,
            demanda.descricao,
            demanda.orcamento_min,
            demanda.orcamento_max,
            demanda.prazo_entrega,
            demanda.observacoes
        )

    def _objeto_para_tupla_update(self, demanda: Demanda) -> tuple:
        """Prepara dados da demanda para atualização"""
        return (
            demanda.titulo,
            demanda.descricao,
            demanda.orcamento_min,
            demanda.orcamento_max,
            demanda.prazo_entrega,
            demanda.observacoes,
            demanda.id
        )

    def _linha_para_objeto(self, linha: dict) -> Demanda:
        """Converte linha do banco em objeto Demanda"""
        return Demanda(
            id=linha["id"],
            id_casal=linha["id_casal"],
            id_categoria=linha["id_categoria"],
            titulo=linha["titulo"],
            descricao=linha["descricao"],
            orcamento_min=linha["orcamento_min"],
            orcamento_max=linha["orcamento_max"],
            prazo_entrega=linha["prazo_entrega"],
            status=linha["status"],
            data_criacao=linha["data_criacao"],
            observacoes=linha["observacoes"]
        )

    def atualizar_status(self, id_demanda: int, status: StatusDemanda) -> bool:
        """Atualiza o status de uma demanda"""
        return self.executar_comando(demanda_sql.ATUALIZAR_STATUS_DEMANDA, (status.value, id_demanda))

    def obter_por_casal(self, id_casal: int) -> List[Demanda]:
        """Obtém todas as demandas de um casal"""
        resultados = self.executar_query(demanda_sql.OBTER_DEMANDAS_POR_CASAL, (id_casal,))
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_ativas(self) -> List[Demanda]:
        """Obtém todas as demandas ativas"""
        resultados = self.executar_query(demanda_sql.OBTER_DEMANDAS_ATIVAS)
        return [self._linha_para_objeto(row) for row in resultados]

    def buscar(self, termo: str) -> List[Demanda]:
        """Busca demandas por termo no título ou descrição"""
        termo_like = f"%{termo}%"
        resultados = self.executar_query(demanda_sql.BUSCAR_DEMANDAS, (termo_like, termo_like))
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_por_status(self, status: Union[str, StatusDemanda]) -> List[Demanda]:
        """Obtém todas as demandas com um status específico"""
        # Converter para string se for enum
        if isinstance(status, StatusDemanda):
            status_str = status.value
        else:
            status_str = status.upper()

        # Validar status usando o enum StatusDemanda
        valid_statuses = [s.value for s in StatusDemanda]

        if status_str not in valid_statuses:
            logger.warning(f"Status inválido: {status}. Status válidos: {valid_statuses}")
            return []

        resultados = self.executar_query(demanda_sql.OBTER_DEMANDAS_POR_STATUS, (status_str,))
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Demanda]:
        """Obtém demandas com paginação"""
        demandas, _ = self.obter_paginado(numero_pagina, tamanho_pagina)
        return demandas

# Instância singleton do repositório
demanda_repo = DemandaRepo()