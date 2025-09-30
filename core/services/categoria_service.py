"""
Serviço de categorias - Lógica de negócio para gestão de categorias

Este serviço gerencia as regras de negócio relacionadas às categorias
de serviços e produtos do sistema.
"""

from typing import List, Optional
from util.exceptions import RegraDeNegocioError, ValidacaoError
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento
from util.logger import logger


class CategoriaService:
    """
    Serviço para operações de negócio com categorias

    Gerencia a criação, atualização e consulta de categorias,
    aplicando regras de negócio específicas do domínio.
    """

    def __init__(self):
        from core.repositories.categoria_repo import CategoriaRepo, categoria_repo
        self.repo: CategoriaRepo = categoria_repo

    def criar_categoria(self, dados: dict) -> int:
        """
        Cria uma nova categoria aplicando regras de negócio

        Args:
            dados: Dados da categoria

        Returns:
            ID da categoria criada

        Raises:
            RegraDeNegocioError: Se regra de negócio violada
            ValidacaoError: Se dados inválidos
        """
        # Verificar se já existe categoria com mesmo nome e tipo
        if self._categoria_nome_tipo_existe(dados['nome'], dados['tipo_fornecimento']):
            raise RegraDeNegocioError(
                f"Já existe uma categoria '{dados['nome']}' para {dados['tipo_fornecimento'].value}",
                regra="CATEGORIA_NOME_TIPO_UNICO"
            )

        # Criar categoria
        categoria = Categoria(
            id=0,
            nome=dados['nome'].strip().title(),  # Normalizar nome
            tipo_fornecimento=dados['tipo_fornecimento'],
            descricao=dados.get('descricao', '').strip(),
            ativo=True
        )

        id_categoria = self.repo.inserir(categoria)

        logger.info("Categoria criada",
            id_categoria=id_categoria,
            nome=categoria.nome,
            tipo=categoria.tipo_fornecimento.value
        )

        return id_categoria

    def listar_categorias_ativas(self, tipo_fornecimento: Optional[TipoFornecimento] = None) -> List[Categoria]:
        """
        Lista categorias ativas, opcionalmente filtradas por tipo

        Args:
            tipo_fornecimento: Tipo para filtrar (opcional)

        Returns:
            Lista de categorias ativas
        """
        if tipo_fornecimento:
            categorias = self.repo.obter_ativas_por_tipo(tipo_fornecimento)
        else:
            categorias = self.repo.listar_todos(ativo=True)

        return sorted(categorias, key=lambda c: c.nome)

    def obter_categoria_por_id(self, categoria_id: int) -> Categoria:
        """
        Obtém categoria por ID com validações

        Args:
            categoria_id: ID da categoria

        Returns:
            Categoria encontrada

        Raises:
            ValidacaoError: Se ID inválido
            RecursoNaoEncontradoError: Se categoria não encontrada
        """
        if categoria_id <= 0:
            raise ValidacaoError("ID da categoria deve ser positivo", "categoria_id", categoria_id)

        return self.repo.obter_por_id(categoria_id)

    def atualizar_categoria(self, categoria_id: int, dados: dict) -> bool:
        """
        Atualiza categoria aplicando validações de negócio

        Args:
            categoria_id: ID da categoria
            dados: Dados a atualizar

        Returns:
            True se atualizada com sucesso

        Raises:
            RecursoNaoEncontradoError: Se categoria não encontrada
            RegraDeNegocioError: Se violação de regra
        """
        categoria = self.repo.obter_por_id(categoria_id)

        # Verificar se mudança de nome/tipo não conflita
        if 'nome' in dados or 'tipo_fornecimento' in dados:
            novo_nome = dados.get('nome', categoria.nome)
            novo_tipo = dados.get('tipo_fornecimento', categoria.tipo_fornecimento)

            # Só verificar se realmente mudou
            if novo_nome != categoria.nome or novo_tipo != categoria.tipo_fornecimento:
                if self._categoria_nome_tipo_existe(novo_nome, novo_tipo, exceto_id=categoria_id):
                    raise RegraDeNegocioError(
                        f"Já existe uma categoria '{novo_nome}' para {novo_tipo.value}",
                        regra="CATEGORIA_NOME_TIPO_UNICO"
                    )

        # Aplicar mudanças
        if 'nome' in dados:
            categoria.nome = dados['nome'].strip().title()
        if 'descricao' in dados:
            categoria.descricao = dados['descricao'].strip()
        if 'tipo_fornecimento' in dados:
            categoria.tipo_fornecimento = dados['tipo_fornecimento']

        resultado = self.repo.atualizar(categoria)

        if resultado:
            logger.info("Categoria atualizada",
                categoria_id=categoria_id,
                nome=categoria.nome
            )

        return resultado

    def desativar_categoria(self, categoria_id: int, admin_id: int) -> bool:
        """
        Desativa categoria (soft delete) com validações de negócio

        Args:
            categoria_id: ID da categoria
            admin_id: ID do admin

        Returns:
            True se desativada

        Raises:
            RegraDeNegocioError: Se categoria tem itens ativos
        """
        categoria = self.repo.obter_por_id(categoria_id)

        # Verificar se categoria tem itens ativos (regra de negócio)
        if self._categoria_tem_itens_ativos(categoria_id):
            raise RegraDeNegocioError(
                "Não é possível desativar categoria com itens ativos",
                regra="CATEGORIA_COM_ITENS_ATIVA"
            )

        categoria.ativo = False
        resultado = self.repo.atualizar(categoria)

        if resultado:
            logger.info("Categoria desativada",
                categoria_id=categoria_id,
                admin_id=admin_id
            )

        return resultado

    def _categoria_nome_tipo_existe(self, nome: str, tipo: TipoFornecimento, exceto_id: Optional[int] = None) -> bool:
        """
        Verifica se já existe categoria com mesmo nome e tipo

        Args:
            nome: Nome da categoria
            tipo: Tipo de fornecimento
            exceto_id: ID para excluir da verificação (para updates)

        Returns:
            True se existe, False caso contrário
        """
        categoria_existente = self.repo.obter_por_nome(nome.strip().title(), tipo)
        if categoria_existente:
            # Se está fazendo update, ignorar a própria categoria
            return categoria_existente.id != exceto_id if exceto_id else True
        return False

    def _categoria_tem_itens_ativos(self, categoria_id: int) -> bool:
        """
        Verifica se categoria tem itens ativos vinculados

        Args:
            categoria_id: ID da categoria

        Returns:
            True se tem itens ativos
        """
        # Verificar se categoria tem itens ativos
        try:
            from core.repositories.item_repo import item_repo
            count = item_repo.contar_registros("id_categoria = ? AND ativo = 1", (categoria_id,))
            return count > 0
        except:
            # Se erro, assumir que tem itens por segurança
            return True


# Instância global do serviço
categoria_service = CategoriaService()