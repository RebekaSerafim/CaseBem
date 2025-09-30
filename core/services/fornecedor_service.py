"""
Serviço de fornecedores - Lógica de negócio centralizada

Este serviço concentra todas as regras de negócio relacionadas aos fornecedores,
incluindo cadastro, atualização, verificação e busca.
"""

from typing import Optional, List
from util.exceptions import RegraDeNegocioError, RecursoNaoEncontradoError
from core.models.fornecedor_model import Fornecedor
from core.models.usuario_model import TipoUsuario
from util.logger import logger


class FornecedorService:
    """
    Serviço para operações de negócio com fornecedores

    Centraliza toda a lógica de negócio relacionada aos fornecedores,
    aplicando validações, regras de domínio e orquestrando operações.
    """

    def __init__(self):
        from core.repositories import fornecedor_repo, usuario_repo
        from util.security import hash_password

        self.repo = fornecedor_repo
        self.usuario_repo = usuario_repo
        self.hash_password = hash_password

    def criar_fornecedor(self, dados: dict) -> int:
        """
        Cria um novo fornecedor aplicando regras de negócio

        Args:
            dados: Dados validados do fornecedor

        Returns:
            ID do fornecedor criado

        Raises:
            RegraDeNegocioError: Se regra de negócio for violada
        """
        # Validar dados obrigatórios
        if not dados.get('nome_empresa'):
            raise RegraDeNegocioError("Nome da empresa é obrigatório")

        if not dados.get('cnpj'):
            raise RegraDeNegocioError("CNPJ é obrigatório")

        # Validar CNPJ único
        try:
            fornecedor_existente = self.repo.obter_fornecedor_por_cnpj(dados['cnpj'])
            if fornecedor_existente:
                raise RegraDeNegocioError(f"CNPJ {dados['cnpj']} já cadastrado")
        except RecursoNaoEncontradoError:
            pass  # CNPJ não existe, pode prosseguir

        # Validar email único
        try:
            usuario_existente = self.usuario_repo.obter_usuario_por_email(dados['email'])
            if usuario_existente:
                raise RegraDeNegocioError(f"Email {dados['email']} já cadastrado")
        except RecursoNaoEncontradoError:
            pass  # Email não existe, pode prosseguir

        # Hash da senha
        dados['senha'] = self.hash_password(dados['senha'])
        dados['perfil'] = TipoUsuario.FORNECEDOR

        # Criar fornecedor
        fornecedor = Fornecedor(**dados)
        id_fornecedor = self.repo.inserir_fornecedor(fornecedor)

        logger.info(f"Fornecedor criado: {id_fornecedor}", extra={
            'nome_empresa': dados['nome_empresa'],
            'cnpj': dados['cnpj']
        })

        return id_fornecedor

    def atualizar_fornecedor(self, id_fornecedor: int, dados: dict) -> bool:
        """
        Atualiza dados de um fornecedor

        Args:
            id_fornecedor: ID do fornecedor
            dados: Dados a serem atualizados

        Returns:
            True se atualizado com sucesso
        """
        # Buscar fornecedor existente
        fornecedor = self.repo.obter_fornecedor_por_id(id_fornecedor)

        # Atualizar campos permitidos
        campos_atualizaveis = ['nome', 'telefone', 'nome_empresa', 'descricao', 'newsletter']
        for campo in campos_atualizaveis:
            if campo in dados:
                setattr(fornecedor, campo, dados[campo])

        # Salvar
        sucesso = self.repo.atualizar_fornecedor(fornecedor)

        if sucesso:
            logger.info(f"Fornecedor atualizado: {id_fornecedor}")

        return sucesso

    def verificar_fornecedor(self, id_fornecedor: int) -> bool:
        """
        Marca um fornecedor como verificado

        Args:
            id_fornecedor: ID do fornecedor

        Returns:
            True se verificado com sucesso
        """
        from datetime import datetime

        fornecedor = self.repo.obter_fornecedor_por_id(id_fornecedor)
        fornecedor.verificado = True
        fornecedor.data_verificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sucesso = self.repo.atualizar_fornecedor(fornecedor)

        if sucesso:
            logger.info(f"Fornecedor verificado: {id_fornecedor}")

        return sucesso

    def obter_fornecedor(self, id_fornecedor: int) -> Fornecedor:
        """
        Obtém um fornecedor por ID

        Args:
            id_fornecedor: ID do fornecedor

        Returns:
            Fornecedor encontrado
        """
        return self.repo.obter_fornecedor_por_id(id_fornecedor)

    def listar_fornecedores(self, pagina: int = 1, tamanho: int = 10,
                           verificado: Optional[bool] = None) -> List[Fornecedor]:
        """
        Lista fornecedores com paginação e filtros

        Args:
            pagina: Número da página
            tamanho: Tamanho da página
            verificado: Filtrar por status de verificação

        Returns:
            Lista de fornecedores
        """
        if verificado is not None:
            return self.repo.obter_fornecedores_verificados() if verificado else []

        return self.repo.obter_fornecedores_por_pagina(pagina, tamanho)

    def buscar_fornecedores(self, termo: str) -> List[Fornecedor]:
        """
        Busca fornecedores por termo

        Args:
            termo: Termo de busca

        Returns:
            Lista de fornecedores encontrados
        """
        return self.repo.buscar_fornecedores(termo)

    def excluir_fornecedor(self, id_fornecedor: int) -> bool:
        """
        Exclui um fornecedor (soft delete)

        Args:
            id_fornecedor: ID do fornecedor

        Returns:
            True se excluído com sucesso
        """
        # Verificar se existe
        self.repo.obter_fornecedor_por_id(id_fornecedor)

        # Excluir
        sucesso = self.repo.excluir_fornecedor(id_fornecedor)

        if sucesso:
            logger.info(f"Fornecedor excluído: {id_fornecedor}")

        return sucesso


# Instância singleton do serviço
fornecedor_service = FornecedorService()