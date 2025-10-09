"""
Testes para ItemDemandaRepo (V2).

IMPORTANTE: ItemDemanda agora tem PK própria (id auto-increment).
Não é mais chave composta (id_demanda, id_item).
Representa descrições livres do que o noivo quer.
"""
import pytest
from core.models.item_demanda_model import ItemDemanda
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.models.casal_model import Casal
from core.repositories.item_demanda_repo import item_demanda_repo
from core.repositories.demanda_repo import demanda_repo
from core.repositories.categoria_repo import categoria_repo
from core.repositories.casal_repo import casal_repo
from core.repositories.usuario_repo import usuario_repo
from util.exceptions import RecursoNaoEncontradoError


class TestItemDemandaRepo:
    def test_criar_tabela_item_demanda(self, test_db):
        # Arrange & Act
        resultado = item_demanda_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_item_demanda(self, test_db, item_demanda_factory, demanda_factory, categoria_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Criar usuários e casal (foreign keys)
        usuario1 = usuario_factory.criar()
        id_usuario1 = usuario_repo.inserir(usuario1)
        usuario2 = usuario_factory.criar()
        id_usuario2 = usuario_repo.inserir(usuario2)
        casal = Casal(0, id_usuario1, id_usuario2)
        id_casal = casal_repo.inserir(casal)
        # Criar categoria e demanda primeiro (foreign keys)
        categoria = categoria_factory.criar()
        id_categoria = categoria_repo.inserir(categoria)
        demanda = demanda_factory.criar(id_casal=id_casal)
        id_demanda = demanda_repo.inserir(demanda)
        item_demanda = item_demanda_factory.criar(id_demanda=id_demanda, id_categoria=id_categoria)
        # Act
        id_inserido = item_demanda_repo.inserir(item_demanda)
        # Assert
        assert id_inserido > 0, "A inserção deveria retornar um ID válido"
        item_demanda_db = item_demanda_repo.obter_por_id(id_inserido)
        assert item_demanda_db is not None, "O item_demanda inserido não deveria ser None"
        assert item_demanda_db.id_demanda == item_demanda.id_demanda
        assert item_demanda_db.tipo == item_demanda.tipo
        assert item_demanda_db.id_categoria == item_demanda.id_categoria
        assert item_demanda_db.descricao == item_demanda.descricao

    def test_obter_item_demanda_existente(self, test_db, item_demanda_factory, demanda_factory, categoria_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Criar usuários e casal (foreign keys)
        usuario1 = usuario_factory.criar()
        id_usuario1 = usuario_repo.inserir(usuario1)
        usuario2 = usuario_factory.criar()
        id_usuario2 = usuario_repo.inserir(usuario2)
        casal = Casal(0, id_usuario1, id_usuario2)
        id_casal = casal_repo.inserir(casal)
        categoria = categoria_factory.criar()
        id_categoria = categoria_repo.inserir(categoria)
        demanda = demanda_factory.criar(id_casal=id_casal)
        id_demanda = demanda_repo.inserir(demanda)
        item_demanda = item_demanda_factory.criar(id_demanda=id_demanda, id_categoria=id_categoria, quantidade=2)
        id_inserido = item_demanda_repo.inserir(item_demanda)
        # Act
        item_demanda_db = item_demanda_repo.obter_por_id(id_inserido)
        # Assert
        assert item_demanda_db is not None
        assert item_demanda_db.id == id_inserido
        assert item_demanda_db.id_demanda == item_demanda.id_demanda
        assert item_demanda_db.quantidade == item_demanda.quantidade

    def test_obter_item_demanda_inexistente(self, test_db):
        # Arrange
        item_demanda_repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            item_demanda_repo.obter_por_id(999)

    def test_atualizar_item_demanda(self, test_db, item_demanda_factory, demanda_factory, categoria_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Criar usuários e casal (foreign keys)
        usuario1 = usuario_factory.criar()
        id_usuario1 = usuario_repo.inserir(usuario1)
        usuario2 = usuario_factory.criar()
        id_usuario2 = usuario_repo.inserir(usuario2)
        casal = Casal(0, id_usuario1, id_usuario2)
        id_casal = casal_repo.inserir(casal)
        categoria = categoria_factory.criar()
        id_categoria = categoria_repo.inserir(categoria)
        demanda = demanda_factory.criar(id_casal=id_casal)
        id_demanda = demanda_repo.inserir(demanda)
        item_demanda = item_demanda_factory.criar(id_demanda=id_demanda, id_categoria=id_categoria)
        id_inserido = item_demanda_repo.inserir(item_demanda)
        item_demanda.id = id_inserido
        item_demanda.quantidade = 5
        item_demanda.preco_maximo = 200.0
        # Act
        resultado = item_demanda_repo.atualizar(item_demanda)
        # Assert
        assert resultado == True
        item_demanda_db = item_demanda_repo.obter_por_id(id_inserido)
        assert item_demanda_db.quantidade == 5
        assert item_demanda_db.preco_maximo == 200.0

    def test_excluir_item_demanda(self, test_db, item_demanda_factory, demanda_factory, categoria_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Criar usuários e casal (foreign keys)
        usuario1 = usuario_factory.criar()
        id_usuario1 = usuario_repo.inserir(usuario1)
        usuario2 = usuario_factory.criar()
        id_usuario2 = usuario_repo.inserir(usuario2)
        casal = Casal(0, id_usuario1, id_usuario2)
        id_casal = casal_repo.inserir(casal)
        categoria = categoria_factory.criar()
        id_categoria = categoria_repo.inserir(categoria)
        demanda = demanda_factory.criar(id_casal=id_casal)
        id_demanda = demanda_repo.inserir(demanda)
        item_demanda = item_demanda_factory.criar(id_demanda=id_demanda, id_categoria=id_categoria)
        id_inserido = item_demanda_repo.inserir(item_demanda)
        # Act
        resultado = item_demanda_repo.excluir(id_inserido)
        # Assert
        assert resultado == True
        with pytest.raises(RecursoNaoEncontradoError):
            item_demanda_repo.obter_por_id(id_inserido)

    def test_obter_itens_por_demanda(self, test_db, item_demanda_factory, demanda_factory, categoria_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Criar usuários e casal (foreign keys)
        usuario1 = usuario_factory.criar()
        id_usuario1 = usuario_repo.inserir(usuario1)
        usuario2 = usuario_factory.criar()
        id_usuario2 = usuario_repo.inserir(usuario2)
        casal = Casal(0, id_usuario1, id_usuario2)
        id_casal = casal_repo.inserir(casal)
        categoria = categoria_factory.criar()
        id_categoria = categoria_repo.inserir(categoria)
        # Criar 2 demandas
        demanda1 = demanda_factory.criar(id_casal=id_casal)
        id_demanda1 = demanda_repo.inserir(demanda1)
        demanda2 = demanda_factory.criar(id_casal=id_casal)
        id_demanda2 = demanda_repo.inserir(demanda2)
        # Criar 3 itens para demanda 1
        for i in range(3):
            item = item_demanda_factory.criar(id_demanda=id_demanda1, id_categoria=id_categoria)
            item_demanda_repo.inserir(item)
        # Criar 2 itens para demanda 2
        for i in range(2):
            item = item_demanda_factory.criar(id_demanda=id_demanda2, id_categoria=id_categoria)
            item_demanda_repo.inserir(item)
        # Act
        itens_demanda1 = item_demanda_repo.obter_por_demanda(id_demanda1)
        # Assert
        assert len(itens_demanda1) == 3
        assert all(item['id_demanda'] == id_demanda1 for item in itens_demanda1)

    def test_contar_itens_por_demanda(self, test_db, item_demanda_factory, demanda_factory, categoria_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Criar usuários e casal (foreign keys)
        usuario1 = usuario_factory.criar()
        id_usuario1 = usuario_repo.inserir(usuario1)
        usuario2 = usuario_factory.criar()
        id_usuario2 = usuario_repo.inserir(usuario2)
        casal = Casal(0, id_usuario1, id_usuario2)
        id_casal = casal_repo.inserir(casal)
        categoria = categoria_factory.criar()
        id_categoria = categoria_repo.inserir(categoria)
        demanda = demanda_factory.criar(id_casal=id_casal)
        id_demanda = demanda_repo.inserir(demanda)
        # Criar 5 itens para demanda 1
        for i in range(5):
            item = item_demanda_factory.criar(id_demanda=id_demanda, id_categoria=id_categoria)
            item_demanda_repo.inserir(item)
        # Act
        total = item_demanda_repo.contar_por_demanda(id_demanda)
        # Assert
        assert total == 5

    def test_excluir_itens_por_demanda(self, test_db, item_demanda_factory, demanda_factory, categoria_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Criar usuários e casal (foreign keys)
        usuario1 = usuario_factory.criar()
        id_usuario1 = usuario_repo.inserir(usuario1)
        usuario2 = usuario_factory.criar()
        id_usuario2 = usuario_repo.inserir(usuario2)
        casal = Casal(0, id_usuario1, id_usuario2)
        id_casal = casal_repo.inserir(casal)
        categoria = categoria_factory.criar()
        id_categoria = categoria_repo.inserir(categoria)
        demanda = demanda_factory.criar(id_casal=id_casal)
        id_demanda = demanda_repo.inserir(demanda)
        # Criar 3 itens para demanda 1
        for i in range(3):
            item = item_demanda_factory.criar(id_demanda=id_demanda, id_categoria=id_categoria)
            item_demanda_repo.inserir(item)
        # Act
        resultado = item_demanda_repo.excluir_por_demanda(id_demanda)
        # Assert
        assert resultado == True
        total = item_demanda_repo.contar_por_demanda(id_demanda)
        assert total == 0
