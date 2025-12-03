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

    def test_obter_por_orcamento(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa obtenção de itens por orçamento (linhas 72-75)"""
        # Arrange
        dados = setup_test_data()
        # Criar 2 item_demandas diferentes
        item_demanda1 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 1")
        item_demanda2 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 2")
        id_item_demanda1 = item_demanda_repo.inserir(item_demanda1)
        id_item_demanda2 = item_demanda_repo.inserir(item_demanda2)
        # Criar 2 item_orcamento com diferentes item_demanda
        item_orc1 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda1, id_item=dados["id_item"])
        item_orc2 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda2, id_item=dados["id_item"])
        item_orcamento_repo.inserir(item_orc1)
        item_orcamento_repo.inserir(item_orc2)
        # Act
        itens = item_orcamento_repo.obter_por_orcamento(dados["id_orcamento"])
        # Assert
        assert len(itens) == 2, "Deveria retornar 2 itens"
        assert all(isinstance(item, dict) for item in itens)

    def test_obter_por_item_demanda(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa obtenção de itens por item_demanda (linhas 83-87)"""
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        item_orc = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=dados["id_item"])
        item_orcamento_repo.inserir(item_orc)
        # Act
        itens = item_orcamento_repo.obter_por_item_demanda(dados["id_orcamento"], id_item_demanda)
        # Assert
        assert len(itens) == 1, "Deveria retornar 1 item"
        assert itens[0]["id_item_demanda"] == id_item_demanda

    def test_verificar_item_ja_usado(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa verificação de item já usado (linhas 97-101)"""
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        item_orc = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=dados["id_item"])
        item_orcamento_repo.inserir(item_orc)
        # Act
        ja_usado = item_orcamento_repo.verificar_item_ja_usado(dados["id_orcamento"], id_item_demanda, dados["id_item"])
        nao_usado = item_orcamento_repo.verificar_item_ja_usado(dados["id_orcamento"], id_item_demanda, 999)
        # Assert
        assert ja_usado is True, "Item deveria estar marcado como já usado"
        assert nao_usado is False, "Item inexistente não deveria estar usado"

    def test_obter_itens_usados(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa obtenção de lista de itens usados (linhas 109-113)"""
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        item_orc = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=dados["id_item"])
        item_orcamento_repo.inserir(item_orc)
        # Act
        ids_usados = item_orcamento_repo.obter_itens_usados(dados["id_orcamento"], id_item_demanda)
        # Assert
        assert len(ids_usados) == 1, "Deveria retornar 1 ID de item usado"
        assert dados["id_item"] in ids_usados, "ID do item deveria estar na lista"

    def test_obter_total_orcamento(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa cálculo de total do orçamento (linhas 117-122)"""
        # Arrange
        dados = setup_test_data()
        # Criar 2 item_demandas diferentes para evitar UNIQUE constraint
        item_demanda1 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 1")
        item_demanda2 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 2")
        id_item_demanda1 = item_demanda_repo.inserir(item_demanda1)
        id_item_demanda2 = item_demanda_repo.inserir(item_demanda2)
        # IMPORTANTE: obter_total_orcamento só soma itens com status='ACEITO'
        item_orc1 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda1, id_item=dados["id_item"], quantidade=2, preco_unitario=50.0, desconto=10.0, status="ACEITO")
        item_orc2 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda2, id_item=dados["id_item"], quantidade=1, preco_unitario=30.0, desconto=None, status="ACEITO")
        item_orcamento_repo.inserir(item_orc1)
        item_orcamento_repo.inserir(item_orc2)
        # Act
        total = item_orcamento_repo.obter_total_orcamento(dados["id_orcamento"])
        # Assert
        # item1: 2*50-10=90, item2: 1*30=30, total=120
        assert total == 120.0, f"Total deveria ser 120.0, mas foi {total}"

    def test_excluir_por_orcamento(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa exclusão de todos os itens de um orçamento (linha 126)"""
        # Arrange
        dados = setup_test_data()
        # Criar 2 item_demandas diferentes para evitar UNIQUE constraint
        item_demanda1 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 1")
        item_demanda2 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 2")
        id_item_demanda1 = item_demanda_repo.inserir(item_demanda1)
        id_item_demanda2 = item_demanda_repo.inserir(item_demanda2)
        item_orc1 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda1, id_item=dados["id_item"])
        item_orc2 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda2, id_item=dados["id_item"])
        item_orcamento_repo.inserir(item_orc1)
        item_orcamento_repo.inserir(item_orc2)
        # Act
        resultado = item_orcamento_repo.excluir_por_orcamento(dados["id_orcamento"])
        # Assert
        assert resultado is True, "Exclusão deveria retornar True"
        itens_restantes = item_orcamento_repo.obter_por_orcamento(dados["id_orcamento"])
        assert len(itens_restantes) == 0, "Não deveria haver itens após exclusão"

    def test_atualizar_status_item_sem_motivo(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa atualização de status sem motivo (linhas 148-152)"""
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        item_orc = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=dados["id_item"], status="PENDENTE")
        id_inserido = item_orcamento_repo.inserir(item_orc)
        # Act
        resultado = item_orcamento_repo.atualizar_status_item(id_inserido, "ACEITO")
        # Assert
        assert resultado is True, "Atualização deveria retornar True"
        item_db = item_orcamento_repo.obter_por_id(id_inserido)
        assert item_db.status == "ACEITO", "Status deveria ser ACEITO"

    def test_atualizar_status_item_com_motivo(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa atualização de status com motivo (linhas 142-147)"""
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        item_orc = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=dados["id_item"], status="PENDENTE")
        id_inserido = item_orcamento_repo.inserir(item_orc)
        # Act
        resultado = item_orcamento_repo.atualizar_status_item(id_inserido, "REJEITADO", "Preço muito alto")
        # Assert
        assert resultado is True, "Atualização deveria retornar True"
        item_db = item_orcamento_repo.obter_por_id(id_inserido)
        assert item_db.status == "REJEITADO", "Status deveria ser REJEITADO"
        assert item_db.motivo_rejeicao == "Preço muito alto", "Motivo deveria ser gravado"

    def test_obter_por_status(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa obtenção de itens por status (linhas 156-159)"""
        # Arrange
        dados = setup_test_data()
        # Criar 2 item_demandas diferentes para evitar UNIQUE constraint
        item_demanda1 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 1")
        item_demanda2 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 2")
        id_item_demanda1 = item_demanda_repo.inserir(item_demanda1)
        id_item_demanda2 = item_demanda_repo.inserir(item_demanda2)
        item_orc1 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda1, id_item=dados["id_item"], status="ACEITO")
        item_orc2 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda2, id_item=dados["id_item"], status="PENDENTE")
        item_orcamento_repo.inserir(item_orc1)
        item_orcamento_repo.inserir(item_orc2)
        # Act
        itens_aceitos = item_orcamento_repo.obter_por_status(dados["id_orcamento"], "ACEITO")
        # Assert
        assert len(itens_aceitos) == 1, "Deveria retornar 1 item aceito"
        assert all(item["status"] == "ACEITO" for item in itens_aceitos)

    def test_contar_por_status(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa contagem de itens por status (linhas 163-166)"""
        # Arrange
        dados = setup_test_data()
        # Criar 3 item_demandas diferentes para evitar UNIQUE constraint
        item_demanda1 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 1")
        item_demanda2 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 2")
        item_demanda3 = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1, descricao="Item Demanda 3")
        id_item_demanda1 = item_demanda_repo.inserir(item_demanda1)
        id_item_demanda2 = item_demanda_repo.inserir(item_demanda2)
        id_item_demanda3 = item_demanda_repo.inserir(item_demanda3)
        item_orc1 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda1, id_item=dados["id_item"], status="ACEITO")
        item_orc2 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda2, id_item=dados["id_item"], status="ACEITO")
        item_orc3 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda3, id_item=dados["id_item"], status="REJEITADO")
        item_orcamento_repo.inserir(item_orc1)
        item_orcamento_repo.inserir(item_orc2)
        item_orcamento_repo.inserir(item_orc3)
        # Act
        total_aceitos = item_orcamento_repo.contar_por_status(dados["id_orcamento"], "ACEITO")
        # Assert
        assert total_aceitos == 2, "Deveria contar 2 itens aceitos"

    def test_contar_por_item_demanda(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa contagem de itens por item_demanda (linhas 170-174)"""
        # Arrange
        dados = setup_test_data()
        # Criar 1 item_demanda e 2 itens diferentes do catálogo para evitar UNIQUE constraint
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        # Criar um segundo item do catálogo
        from core.models.item_model import Item
        item2 = Item(id=0, id_fornecedor=dados["id_fornecedor"], id_categoria=1, nome="Item Teste 2", descricao="Descrição do item teste 2", tipo=TipoFornecimento.PRODUTO, preco=Decimal("150.0"))
        id_item2 = item_repo.inserir(item2)
        # Criar 2 item_orcamento com o mesmo item_demanda mas itens diferentes
        item_orc1 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=dados["id_item"])
        item_orc2 = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=id_item2)
        item_orcamento_repo.inserir(item_orc1)
        item_orcamento_repo.inserir(item_orc2)
        # Act
        total = item_orcamento_repo.contar_por_item_demanda(id_item_demanda)
        # Assert
        assert total == 2, "Deveria contar 2 itens para este item_demanda"

    def test_verificar_item_demanda_ja_aceito(self, test_db, item_orcamento_factory, item_demanda_factory):
        """Testa verificação de item_demanda já aceito (linhas 184-187)"""
        # Arrange
        dados = setup_test_data()
        item_demanda = item_demanda_factory.criar(id=0, id_demanda=dados["id_demanda"], id_categoria=1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        item_orc = item_orcamento_factory.criar(id_orcamento=dados["id_orcamento"], id_item_demanda=id_item_demanda, id_item=dados["id_item"], status="ACEITO")
        item_orcamento_repo.inserir(item_orc)
        # Act
        ja_aceito = item_orcamento_repo.verificar_item_demanda_ja_aceito(id_item_demanda)
        nao_aceito = item_orcamento_repo.verificar_item_demanda_ja_aceito(999)
        # Assert
        assert ja_aceito is True, "Item_demanda deveria estar aceito"
        assert nao_aceito is False, "Item_demanda inexistente não deveria estar aceito"

    def test_obter_total_orcamento_sem_itens_aceitos(self, test_db):
        """Testa cálculo de total quando não há itens aceitos (linha 122)"""
        # Arrange
        dados = setup_test_data()
        # Act
        total = item_orcamento_repo.obter_total_orcamento(dados["id_orcamento"])
        # Assert
        assert total == 0.0, "Total deveria ser 0.0 quando não há itens aceitos"
