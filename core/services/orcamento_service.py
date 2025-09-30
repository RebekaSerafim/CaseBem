"""
Serviço de orçamentos - Lógica de negócio centralizada
"""

from typing import Optional, List
from util.exceptions import RegraDeNegocioError
from core.models.orcamento_model import Orcamento
from util.logger import logger


class OrcamentoService:
    """Serviço para operações de negócio com orçamentos"""

    def __init__(self):
        from core.repositories import orcamento_repo, demanda_repo, fornecedor_repo

        self.repo = orcamento_repo
        self.demanda_repo = demanda_repo
        self.fornecedor_repo = fornecedor_repo

    def criar_orcamento(self, dados: dict) -> int:
        """Cria um novo orçamento"""
        # Validar demanda existe
        self.demanda_repo.obter_demanda_por_id(dados['id_demanda'])

        # Validar fornecedor existe
        self.fornecedor_repo.obter_fornecedor_por_id(dados['id_fornecedor_prestador'])

        # Validar valor total
        if dados.get('valor_total') and dados['valor_total'] < 0:
            raise RegraDeNegocioError("Valor total não pode ser negativo")

        orcamento = Orcamento(**dados)
        id_orcamento = self.repo.inserir_orcamento(orcamento)

        logger.info(f"Orçamento criado: {id_orcamento}")
        return id_orcamento

    def atualizar_orcamento(self, id_orcamento: int, dados: dict) -> bool:
        """Atualiza um orçamento"""
        orcamento = self.repo.obter_orcamento_por_id(id_orcamento)

        if 'valor_total' in dados and dados['valor_total'] < 0:
            raise RegraDeNegocioError("Valor total não pode ser negativo")

        campos_atualizaveis = ['data_hora_validade', 'status', 'observacoes', 'valor_total']
        for campo in campos_atualizaveis:
            if campo in dados:
                setattr(orcamento, campo, dados[campo])

        sucesso = self.repo.atualizar_orcamento(orcamento)
        if sucesso:
            logger.info(f"Orçamento atualizado: {id_orcamento}")
        return sucesso

    def obter_orcamento(self, id_orcamento: int) -> Orcamento:
        """Obtém um orçamento por ID"""
        return self.repo.obter_orcamento_por_id(id_orcamento)

    def listar_orcamentos(self, id_demanda: Optional[int] = None,
                         id_fornecedor: Optional[int] = None,
                         pagina: int = 1, tamanho: int = 10) -> List[Orcamento]:
        """Lista orçamentos com filtros"""
        if id_demanda:
            return self.repo.obter_orcamentos_por_demanda(id_demanda)
        if id_fornecedor:
            return self.repo.obter_orcamentos_por_fornecedor(id_fornecedor)
        return self.repo.obter_orcamentos_por_pagina(pagina, tamanho)

    def excluir_orcamento(self, id_orcamento: int) -> bool:
        """Exclui um orçamento"""
        self.repo.obter_orcamento_por_id(id_orcamento)
        sucesso = self.repo.excluir_orcamento(id_orcamento)
        if sucesso:
            logger.info(f"Orçamento excluído: {id_orcamento}")
        return sucesso


orcamento_service = OrcamentoService()