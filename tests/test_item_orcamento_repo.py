import pytest
from decimal import Decimal
from core.models.item_orcamento_model import ItemOrcamento
from core.models.categoria_model import Categoria, TipoFornecimento
from core.models.usuario_model import Usuario, TipoUsuario
from core.models.fornecedor_model import Fornecedor
from core.models.casal_model import Casal
from core.models.demanda_model import Demanda
from core.models.orcamento_model import Orcamento
from core.models.item_model import Item
from core.repositories.item_orcamento_repo import item_orcamento_repo
from core.repositories.orcamento_repo import orcamento_repo
from core.repositories.item_repo import item_repo
from core.repositories.item_demanda_repo import item_demanda_repo
from core.repositories.demanda_repo import demanda_repo
from core.repositories.categoria_repo import categoria_repo
from core.repositories.usuario_repo import usuario_repo
from core.repositories.casal_repo import casal_repo
from core.repositories.fornecedor_repo import fornecedor_repo
from datetime import datetime


def setup_test_data():
    """Helper para criar dados de teste com todas as FK necessárias"""
    # Criar tabelas
    usuario_repo.criar_tabela()
    fornecedor_repo.criar_tabela()
    casal_repo.criar_tabela()
    categoria_repo.criar_tabela()
    demanda_repo.criar_tabela()
    item_repo.criar_tabela()
    item_demanda_repo.criar_tabela()
    orcamento_repo.criar_tabela()
    item_orcamento_repo.criar_tabela()

    # Criar dados
    usuario = Usuario(id=0, nome="Noivo Teste", cpf=None, data_nascimento=None, email="noivo@test.com", telefone="", senha="hash", perfil=TipoUsuario.NOIVO, token_redefinicao=None, data_token=None, data_cadastro=None)
    id_usuario = usuario_repo.inserir(usuario)

    usuario2 = Usuario(id=0, nome="Noivo2 Teste", cpf=None, data_nascimento=None, email="noivo2@test.com", telefone="", senha="hash", perfil=TipoUsuario.NOIVO, token_redefinicao=None, data_token=None, data_cadastro=None)
    id_usuario2 = usuario_repo.inserir(usuario2)

    fornecedor = Fornecedor(id=0, nome="Fornecedor Teste", cpf=None, data_nascimento=None, email="forn@test.com", telefone="", senha="hash", perfil=TipoUsuario.FORNECEDOR, token_redefinicao=None, data_token=None, data_cadastro=None, nome_empresa="Empresa Teste", cnpj=None)
    id_fornecedor = fornecedor_repo.inserir(fornecedor)
    assert id_fornecedor is not None, "id_fornecedor não deve ser None"

    casal = Casal(id=0, id_noivo1=id_usuario, id_noivo2=id_usuario2)
    id_casal = casal_repo.inserir(casal)

    categoria = Categoria(id=1, nome="Decoração", tipo_fornecimento=TipoFornecimento.PRODUTO)
    categoria_repo.inserir(categoria)

    demanda = Demanda(id=0, id_casal=id_casal, descricao="Demanda Teste")
    id_demanda = demanda_repo.inserir(demanda)

    item = Item(id=0, id_fornecedor=id_fornecedor, id_categoria=1, nome="Item Teste", descricao="Descrição do item teste", tipo=TipoFornecimento.PRODUTO, preco=Decimal("100.0"))
    id_item = item_repo.inserir(item)

    orcamento = Orcamento(id=0, id_demanda=id_demanda, id_fornecedor_prestador=id_fornecedor, data_hora_cadastro=datetime.now())
    id_orcamento = orcamento_repo.inserir(orcamento)

    return {
        "id_usuario": id_usuario,
        "id_fornecedor": id_fornecedor,
        "id_casal": id_casal,
        "id_demanda": id_demanda,
        "id_item": id_item,
        "id_orcamento": id_orcamento,
    }


class TestItemOrcamentoRepo:
    def test_criar_tabela_item_orcamento(self, test_db):
        # Arrange
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        demanda_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        # Act
        resultado = item_orcamento_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_item_orcamento(self, test_db, item_orcamento_factory, item_demanda_factory):
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)

        item_orcamento = item_orcamento_factory.criar(
            id_orcamento=dados["id_orcamento"],
            id_item_demanda=id_item_demanda,
            id_item=dados["id_item"]
        )
        # Act
        id_inserido = item_orcamento_repo.inserir(item_orcamento)
        # Assert
        assert id_inserido > 0, "A inserção deveria retornar um ID válido"
        item_orcamento_db = item_orcamento_repo.obter_por_id(id_inserido)
        assert item_orcamento_db is not None, "O item_orcamento inserido não deveria ser None"

    def test_obter_item_orcamento_existente(self, test_db, item_orcamento_factory, item_demanda_factory):
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)

        item_orcamento = item_orcamento_factory.criar(
            id_orcamento=dados["id_orcamento"],
            id_item_demanda=id_item_demanda,
            id_item=dados["id_item"],
            quantidade=2,
            preco_unitario=50.0
        )
        id_inserido = item_orcamento_repo.inserir(item_orcamento)
        # Act
        item_orcamento_db = item_orcamento_repo.obter_por_id(id_inserido)
        # Assert
        assert item_orcamento_db is not None
        assert item_orcamento_db.id_orcamento == item_orcamento.id_orcamento
        assert item_orcamento_db.id_item_demanda == item_orcamento.id_item_demanda
        assert item_orcamento_db.id_item == item_orcamento.id_item
        assert item_orcamento_db.quantidade == item_orcamento.quantidade
        assert item_orcamento_db.preco_unitario == item_orcamento.preco_unitario

    def test_preco_total_property(self, item_orcamento_factory):
        # Arrange
        item_orcamento = item_orcamento_factory.criar(quantidade=2, preco_unitario=50.0, desconto=10.0)
        # Act
        preco_total = item_orcamento.preco_total
        # Assert
        assert preco_total == 90.0, "Preço total deveria ser 2 * 50 - 10 = 90"

    def test_atualizar_item_orcamento(self, test_db, item_orcamento_factory, item_demanda_factory):
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)

        item_orcamento = item_orcamento_factory.criar(
            id_orcamento=dados["id_orcamento"],
            id_item_demanda=id_item_demanda,
            id_item=dados["id_item"]
        )
        id_inserido = item_orcamento_repo.inserir(item_orcamento)
        item_orcamento.id = id_inserido
        item_orcamento.quantidade = 3
        item_orcamento.preco_unitario = 75.0
        item_orcamento.desconto = 5.0
        # Act
        resultado = item_orcamento_repo.atualizar(item_orcamento)
        # Assert
        assert resultado == True
        item_orcamento_db = item_orcamento_repo.obter_por_id(id_inserido)
        assert item_orcamento_db.quantidade == 3
        assert item_orcamento_db.preco_unitario == 75.0
        assert item_orcamento_db.desconto == 5.0

    def test_excluir_item_orcamento(self, test_db, item_orcamento_factory, item_demanda_factory):
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)

        item_orcamento = item_orcamento_factory.criar(
            id_orcamento=dados["id_orcamento"],
            id_item_demanda=id_item_demanda,
            id_item=dados["id_item"]
        )
        id_inserido = item_orcamento_repo.inserir(item_orcamento)
        # Act
        resultado = item_orcamento_repo.excluir(id_inserido)
        # Assert
        assert resultado == True
        from util.exceptions import RecursoNaoEncontradoError
        with pytest.raises(RecursoNaoEncontradoError):
            item_orcamento_repo.obter_por_id(id_inserido)
