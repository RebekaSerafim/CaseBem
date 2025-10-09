"""
Serviço de orçamentos - Lógica de negócio centralizada

IMPORTANTE (V3): Orçamentos têm status individual por item.
O status do orçamento é derivado dos status dos itens.
"""

from typing import Optional, List, Dict, Any
from util.exceptions import RegraDeNegocioError
from core.models.orcamento_model import Orcamento
from core.models.item_orcamento_model import ItemOrcamento
from infrastructure.logging import logger


class OrcamentoService:
    """Serviço para operações de negócio com orçamentos"""

    def __init__(self):
        from core.repositories.orcamento_repo import OrcamentoRepo, orcamento_repo
        from core.repositories.demanda_repo import DemandaRepo, demanda_repo
        from core.repositories.fornecedor_repo import FornecedorRepo, fornecedor_repo
        from core.repositories.item_orcamento_repo import ItemOrcamentoRepo, item_orcamento_repo
        from core.repositories.item_demanda_repo import ItemDemandaRepo, item_demanda_repo
        from core.repositories.item_repo import ItemRepo, item_repo

        self.repo: OrcamentoRepo = orcamento_repo
        self.demanda_repo: DemandaRepo = demanda_repo
        self.fornecedor_repo: FornecedorRepo = fornecedor_repo
        self.item_orcamento_repo: ItemOrcamentoRepo = item_orcamento_repo
        self.item_demanda_repo: ItemDemandaRepo = item_demanda_repo
        self.item_repo: ItemRepo = item_repo

    def criar_orcamento(self, dados: dict) -> int:
        """Cria um novo orçamento"""
        # Validar demanda existe
        self.demanda_repo.obter_por_id(dados['id_demanda'])

        # Validar fornecedor existe
        self.fornecedor_repo.obter_por_id(dados['id_fornecedor_prestador'])

        # Validar valor total
        if dados.get('valor_total') and dados['valor_total'] < 0:
            raise RegraDeNegocioError("Valor total não pode ser negativo")

        orcamento = Orcamento(**dados)
        id_orcamento = self.repo.inserir(orcamento)

        logger.info(f"Orçamento criado: {id_orcamento}")
        return id_orcamento  # type: ignore[no-any-return]

    def atualizar_orcamento(self, id_orcamento: int, dados: dict) -> bool:
        """Atualiza um orçamento"""
        orcamento = self.repo.obter_por_id(id_orcamento)

        if 'valor_total' in dados and dados['valor_total'] < 0:
            raise RegraDeNegocioError("Valor total não pode ser negativo")

        campos_atualizaveis = ['data_hora_validade', 'status', 'observacoes', 'valor_total']
        for campo in campos_atualizaveis:
            if campo in dados:
                setattr(orcamento, campo, dados[campo])

        sucesso = self.repo.atualizar(orcamento)
        if sucesso:
            logger.info(f"Orçamento atualizado: {id_orcamento}")
        return sucesso  # type: ignore[no-any-return]

    def obter_orcamento(self, id_orcamento: int) -> Orcamento:
        """Obtém um orçamento por ID"""
        return self.repo.obter_por_id(id_orcamento)  # type: ignore[no-any-return]

    def listar_orcamentos(self, id_demanda: Optional[int] = None,
                         id_fornecedor: Optional[int] = None,
                         pagina: int = 1, tamanho: int = 10) -> List[Orcamento]:
        """Lista orçamentos com filtros"""
        if id_demanda:
            return self.repo.obter_por_demanda(id_demanda)
        if id_fornecedor:
            return self.repo.obter_por_fornecedor_prestador(id_fornecedor)
        return self.repo.obter_por_pagina(pagina, tamanho)

    def excluir_orcamento(self, id_orcamento: int) -> bool:
        """Exclui um orçamento"""
        self.repo.obter_por_id(id_orcamento)
        sucesso = self.repo.excluir(id_orcamento)
        if sucesso:
            logger.info(f"Orçamento excluído: {id_orcamento}")
        return sucesso  # type: ignore[no-any-return]

    def aceitar_item_orcamento(self, id_item_orcamento: int, id_orcamento: int) -> bool:
        """
        Aceita um item individual do orçamento.

        REGRA DE NEGÓCIO: Não pode aceitar dois itens para o mesmo item_demanda.
        Um noivo pode aceitar itens de diferentes fornecedores, mas apenas um item
        por item_demanda.

        Returns:
            bool: True se aceitou com sucesso
        Raises:
            RegraDeNegocioError: Se já existe item aceito para o mesmo item_demanda
        """
        # Buscar o item do orçamento
        item_orcamento = self.item_orcamento_repo.obter_por_id(id_item_orcamento)
        if not item_orcamento:
            raise RegraDeNegocioError("Item de orçamento não encontrado")

        # Verificar se o item pertence ao orçamento correto
        if item_orcamento.id_orcamento != id_orcamento:
            raise RegraDeNegocioError("Item não pertence a este orçamento")

        # Verificar se já existe um item aceito para o mesmo item_demanda
        if self.item_orcamento_repo.verificar_item_demanda_ja_aceito(item_orcamento.id_item_demanda):
            raise RegraDeNegocioError(
                "Já existe um item aceito para esta solicitação. "
                "Você não pode aceitar dois orçamentos para o mesmo item."
            )

        # Aceitar o item
        sucesso = self.item_orcamento_repo.atualizar_status_item(id_item_orcamento, "ACEITO")

        if sucesso:
            # Atualizar status derivado do orçamento
            self.repo.atualizar_status_derivado(id_orcamento)

            # Atualizar valor total do orçamento (soma apenas itens aceitos)
            valor_total = self.item_orcamento_repo.obter_total_orcamento(id_orcamento)
            self.repo.atualizar_valor_total(id_orcamento, valor_total)

            logger.info(
                f"Item de orçamento aceito com sucesso",
                item_orcamento_id=id_item_orcamento,
                orcamento_id=id_orcamento
            )

        return sucesso

    def rejeitar_item_orcamento(
        self,
        id_item_orcamento: int,
        id_orcamento: int,
        motivo_rejeicao: Optional[str] = None
    ) -> bool:
        """
        Rejeita um item individual do orçamento.

        Args:
            id_item_orcamento: ID do item a ser rejeitado
            id_orcamento: ID do orçamento
            motivo_rejeicao: Motivo opcional da rejeição

        Returns:
            bool: True se rejeitou com sucesso
        Raises:
            RegraDeNegocioError: Se item não pertence ao orçamento
        """
        # Buscar o item do orçamento
        item_orcamento = self.item_orcamento_repo.obter_por_id(id_item_orcamento)
        if not item_orcamento:
            raise RegraDeNegocioError("Item de orçamento não encontrado")

        # Verificar se o item pertence ao orçamento correto
        if item_orcamento.id_orcamento != id_orcamento:
            raise RegraDeNegocioError("Item não pertence a este orçamento")

        # Rejeitar o item com motivo
        sucesso = self.item_orcamento_repo.atualizar_status_item(
            id_item_orcamento,
            "REJEITADO",
            motivo_rejeicao
        )

        if sucesso:
            # Atualizar status derivado do orçamento
            self.repo.atualizar_status_derivado(id_orcamento)

            # Atualizar valor total do orçamento (soma apenas itens aceitos)
            valor_total = self.item_orcamento_repo.obter_total_orcamento(id_orcamento)
            self.repo.atualizar_valor_total(id_orcamento, valor_total)

            logger.info(
                f"Item de orçamento rejeitado com sucesso",
                item_orcamento_id=id_item_orcamento,
                orcamento_id=id_orcamento,
                motivo=motivo_rejeicao or "Não informado"
            )

        return sucesso

    def criar_orcamento_com_itens(
        self,
        id_demanda: int,
        id_fornecedor: int,
        observacoes: Optional[str],
        itens: List[Dict[str, Any]]
    ) -> int:
        """
        Cria um orçamento completo com seus itens.

        Args:
            id_demanda: ID da demanda
            id_fornecedor: ID do fornecedor
            observacoes: Observações gerais do orçamento
            itens: Lista de dicts com dados dos itens:
                - id_item_demanda: ID do item_demanda sendo atendido
                - id_item: ID do item do catálogo do fornecedor
                - quantidade: Quantidade oferecida
                - preco_unitario: Preço unitário
                - desconto: Desconto (opcional)
                - observacoes: Observações do item (opcional)

        Returns:
            int: ID do orçamento criado

        Raises:
            RegraDeNegocioError: Se validações falharem
        """
        from datetime import datetime

        # Validar demanda existe
        demanda = self.demanda_repo.obter_por_id(id_demanda)
        if not demanda:
            raise RegraDeNegocioError("Demanda não encontrada")

        # Validar fornecedor existe
        self.fornecedor_repo.obter_por_id(id_fornecedor)

        # Validar que pelo menos 1 item foi fornecido
        if not itens or len(itens) == 0:
            raise RegraDeNegocioError("Adicione pelo menos um item ao orçamento")

        # Calcular valor total
        valor_total = 0.0
        for item_data in itens:
            qtd = item_data.get('quantidade', 1)
            preco = item_data.get('preco_unitario', 0)
            desc = item_data.get('desconto', 0) or 0
            subtotal = (qtd * preco) - desc
            valor_total += subtotal

        # Criar orçamento
        novo_orcamento = Orcamento(
            id=0,
            id_demanda=id_demanda,
            id_fornecedor_prestador=id_fornecedor,
            data_hora_cadastro=datetime.now(),
            data_hora_validade=None,
            status="PENDENTE",
            observacoes=observacoes,
            valor_total=valor_total,
        )

        # Inserir orçamento no banco
        id_orcamento = self.repo.inserir(novo_orcamento)

        if not id_orcamento:
            raise RegraDeNegocioError("Erro ao criar orçamento no banco de dados")

        # Inserir itens do orçamento
        itens_inseridos = 0
        for item_data in itens:
            try:
                id_item_demanda = item_data.get('id_item_demanda')
                id_item = item_data.get('id_item')

                if not id_item_demanda or not id_item:
                    continue

                # Validar que o item pertence à categoria do item_demanda
                item_obj = self.item_repo.obter_por_id(id_item)
                itens_demanda_list = self.item_demanda_repo.obter_por_demanda(id_demanda)
                item_demanda_obj = next(
                    (item for item in itens_demanda_list if item.get("id") == id_item_demanda),
                    None
                )

                if not item_obj or not item_demanda_obj:
                    logger.warning(
                        f"Item #{id_item} ou ItemDemanda #{id_item_demanda} não encontrado"
                    )
                    continue

                if item_obj.id_categoria != item_demanda_obj.get("id_categoria"):
                    logger.warning(
                        f"Item '{item_obj.nome}' não pertence à categoria do item solicitado"
                    )
                    continue

                # Verificar se item já foi usado para este item_demanda
                if self.item_orcamento_repo.verificar_item_ja_usado(
                    id_orcamento, id_item_demanda, id_item
                ):
                    logger.warning(f"Item '{item_obj.nome}' já foi adicionado para este item da demanda")
                    continue

                # Criar item_orcamento
                item_orcamento = ItemOrcamento(
                    id=0,
                    id_orcamento=id_orcamento,
                    id_item_demanda=id_item_demanda,
                    id_item=id_item,
                    quantidade=item_data.get('quantidade', 1),
                    preco_unitario=item_data.get('preco_unitario', 0),
                    observacoes=item_data.get('observacoes'),
                    desconto=item_data.get('desconto', 0.0),
                    status="PENDENTE",
                    motivo_rejeicao=None
                )
                self.item_orcamento_repo.inserir(item_orcamento)
                itens_inseridos += 1

            except Exception as e:
                logger.error(f"Erro ao inserir item do orçamento: {e}", orcamento_id=id_orcamento)

        if itens_inseridos == 0:
            # Reverter criação do orçamento se nenhum item foi inserido
            self.repo.excluir(id_orcamento)
            raise RegraDeNegocioError("Nenhum item válido foi adicionado ao orçamento")

        logger.info(
            f"Orçamento criado com sucesso",
            orcamento_id=id_orcamento,
            demanda_id=id_demanda,
            fornecedor_id=id_fornecedor,
            total_itens=itens_inseridos,
            valor_total=valor_total
        )

        return id_orcamento  # type: ignore[no-any-return]


orcamento_service = OrcamentoService()