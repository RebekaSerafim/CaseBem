"""
Serviço de itens - Lógica de negócio centralizada

Este serviço concentra todas as regras de negócio relacionadas aos itens,
incluindo cadastro, validação, busca e operações relacionadas.
"""

from typing import Optional, List
from util.exceptions import RegraDeNegocioError, RecursoNaoEncontradoError
from core.models.item_model import Item
from core.models.tipo_fornecimento_model import TipoFornecimento
from infrastructure.logging import logger


class ItemService:
    """
    Serviço para operações de negócio com itens

    Centraliza toda a lógica de negócio relacionada aos itens,
    aplicando validações, regras de domínio e orquestrando operações.
    """

    def __init__(self):
        from core.repositories.item_repo import ItemRepo, item_repo
        from core.repositories.categoria_repo import CategoriaRepo, categoria_repo
        from core.repositories.fornecedor_repo import FornecedorRepo, fornecedor_repo

        self.repo: ItemRepo = item_repo
        self.categoria_repo: CategoriaRepo = categoria_repo
        self.fornecedor_repo: FornecedorRepo = fornecedor_repo

    def criar_item(self, dados: dict) -> int:
        """
        Cria um novo item aplicando regras de negócio

        Args:
            dados: Dados validados do item

        Returns:
            ID do item criado

        Raises:
            RegraDeNegocioError: Se regra de negócio for violada
        """
        # Validar fornecedor existe
        try:
            self.fornecedor_repo.obter_por_id(dados['id_fornecedor'])
        except RecursoNaoEncontradoError:
            raise RegraDeNegocioError(f"Fornecedor {dados['id_fornecedor']} não encontrado")

        # Validar categoria existe e é do tipo correto
        categoria = self.categoria_repo.obter_por_id(dados['id_categoria'])

        if dados['tipo'] != categoria.tipo_fornecimento:
            raise RegraDeNegocioError(
                f"Tipo do item ({dados['tipo'].value}) não corresponde ao tipo da categoria ({categoria.tipo_fornecimento.value})"
            )

        # Validar preço
        if dados.get('preco') and dados['preco'] < 0:
            raise RegraDeNegocioError("Preço não pode ser negativo")

        # Criar item
        item = Item(**dados)
        id_item = self.repo.inserir(item)

        if not id_item:
            raise RegraDeNegocioError("Falha ao criar item")

        logger.info(f"Item criado: {id_item}", extra={
            'nome': dados['nome'],
            'tipo': dados['tipo'].value
        })

        return id_item

    def atualizar_item(self, id_item: int, dados: dict) -> bool:
        """
        Atualiza dados de um item

        Args:
            id_item: ID do item
            dados: Dados a serem atualizados

        Returns:
            True se atualizado com sucesso
        """
        # Buscar item existente
        item = self.repo.obter_por_id(id_item)

        # Se alterar categoria, validar tipo
        if 'id_categoria' in dados and dados['id_categoria'] != item.id_categoria:
            categoria = self.categoria_repo.obter_por_id(dados['id_categoria'])
            if item.tipo != categoria.tipo_fornecimento:
                raise RegraDeNegocioError(
                    f"Tipo do item ({item.tipo.value}) não corresponde ao tipo da nova categoria ({categoria.tipo_fornecimento.value})"
                )

        # Validar preço se fornecido
        if 'preco' in dados and dados['preco'] < 0:
            raise RegraDeNegocioError("Preço não pode ser negativo")

        # Atualizar campos permitidos
        campos_atualizaveis = ['nome', 'descricao', 'preco', 'id_categoria', 'observacoes', 'ativo']
        for campo in campos_atualizaveis:
            if campo in dados:
                setattr(item, campo, dados[campo])

        # Salvar
        sucesso = self.repo.atualizar(item)

        if sucesso:
            logger.info(f"Item atualizado: {id_item}")

        return sucesso

    def obter_item(self, id_item: int) -> Item:
        """
        Obtém um item por ID

        Args:
            id_item: ID do item

        Returns:
            Item encontrado
        """
        return self.repo.obter_por_id(id_item)  # type: ignore[no-any-return]

    def listar_itens(self, pagina: int = 1, tamanho: int = 10,
                     id_fornecedor: Optional[int] = None,
                     tipo: Optional[TipoFornecimento] = None) -> List[Item]:
        """
        Lista itens com paginação e filtros

        Args:
            pagina: Número da página
            tamanho: Tamanho da página
            id_fornecedor: Filtrar por fornecedor
            tipo: Filtrar por tipo

        Returns:
            Lista de itens
        """
        if id_fornecedor:
            return self.repo.obter_itens_por_fornecedor(id_fornecedor)

        if tipo:
            return self.repo.obter_itens_por_tipo(tipo)

        return self.repo.obter_itens_por_pagina(pagina, tamanho)

    def buscar_itens(self, termo: str, pagina: int = 1, tamanho: int = 20) -> List[Item]:
        """
        Busca itens por termo

        Args:
            termo: Termo de busca
            pagina: Número da página
            tamanho: Tamanho da página

        Returns:
            Lista de itens encontrados
        """
        return self.repo.buscar_itens(termo, pagina, tamanho)

    def ativar_item(self, id_item: int, id_fornecedor: int) -> bool:
        """
        Ativa um item

        Args:
            id_item: ID do item
            id_fornecedor: ID do fornecedor (validação de propriedade)

        Returns:
            True se ativado com sucesso
        """
        sucesso = self.repo.ativar_item(id_item, id_fornecedor)

        if sucesso:
            logger.info(f"Item ativado: {id_item}")

        return sucesso

    def desativar_item(self, id_item: int, id_fornecedor: int) -> bool:
        """
        Desativa um item

        Args:
            id_item: ID do item
            id_fornecedor: ID do fornecedor (validação de propriedade)

        Returns:
            True se desativado com sucesso
        """
        sucesso = self.repo.desativar_item(id_item, id_fornecedor)

        if sucesso:
            logger.info(f"Item desativado: {id_item}")

        return sucesso

    def excluir_item(self, id_item: int) -> bool:
        """
        Exclui um item (soft delete via desativação)

        Args:
            id_item: ID do item

        Returns:
            True se excluído com sucesso
        """
        # Verificar se existe
        self.repo.obter_por_id(id_item)

        # Excluir (ou desativar)
        sucesso = self.repo.excluir(id_item)

        if sucesso:
            logger.info(f"Item excluído: {id_item}")

        return sucesso  # type: ignore[no-any-return]


# Instância singleton do serviço
item_service = ItemService()