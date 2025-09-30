"""
Serviço de demandas - Lógica de negócio centralizada
"""

from typing import Optional, List
from util.exceptions import RegraDeNegocioError
from core.models.demanda_model import Demanda, StatusDemanda
from util.logger import logger


class DemandaService:
    """Serviço para operações de negócio com demandas"""

    def __init__(self):
        from core.repositories import demanda_repo, casal_repo, categoria_repo

        self.repo = demanda_repo
        self.casal_repo = casal_repo
        self.categoria_repo = categoria_repo

    def criar_demanda(self, dados: dict) -> int:
        """Cria uma nova demanda"""
        # Validar casal existe
        self.casal_repo.obter_por_id(dados['id_casal'])

        # Validar categoria existe
        self.categoria_repo.obter_por_id(dados['id_categoria'])

        # Validar orçamentos
        if dados.get('orcamento_min') and dados.get('orcamento_max'):
            if dados['orcamento_min'] > dados['orcamento_max']:
                raise RegraDeNegocioError("Orçamento mínimo não pode ser maior que o máximo")

        demanda = Demanda(**dados)
        id_demanda = self.repo.inserir(demanda)

        logger.info(f"Demanda criada: {id_demanda}")
        return id_demanda

    def atualizar_demanda(self, id_demanda: int, dados: dict) -> bool:
        """Atualiza uma demanda"""
        demanda = self.repo.obter_por_id(id_demanda)

        campos_atualizaveis = ['titulo', 'descricao', 'orcamento_min', 'orcamento_max', 'prazo_entrega', 'observacoes']
        for campo in campos_atualizaveis:
            if campo in dados:
                setattr(demanda, campo, dados[campo])

        sucesso = self.repo.atualizar(demanda)
        if sucesso:
            logger.info(f"Demanda atualizada: {id_demanda}")
        return sucesso

    def atualizar_status(self, id_demanda: int, status: StatusDemanda) -> bool:
        """Atualiza o status de uma demanda"""
        sucesso = self.repo.atualizar_status_demanda(id_demanda, status)
        if sucesso:
            logger.info(f"Status da demanda {id_demanda} atualizado para {status.value}")
        return sucesso

    def obter_demanda(self, id_demanda: int) -> Demanda:
        """Obtém uma demanda por ID"""
        return self.repo.obter_por_id(id_demanda)

    def listar_demandas(self, pagina: int = 1, tamanho: int = 10,
                       id_casal: Optional[int] = None,
                       status: Optional[StatusDemanda] = None) -> List[Demanda]:
        """Lista demandas com filtros"""
        if id_casal:
            return self.repo.obter_demandas_por_casal(id_casal)
        if status:
            return self.repo.obter_demandas_por_status(status)
        return self.repo.obter_demandas_por_pagina(pagina, tamanho)

    def buscar_demandas(self, termo: str) -> List[Demanda]:
        """Busca demandas por termo"""
        return self.repo.buscar_demandas(termo)

    def excluir_demanda(self, id_demanda: int) -> bool:
        """Exclui uma demanda"""
        self.repo.obter_por_id(id_demanda)
        sucesso = self.repo.excluir(id_demanda)
        if sucesso:
            logger.info(f"Demanda excluída: {id_demanda}")
        return sucesso


demanda_service = DemandaService()