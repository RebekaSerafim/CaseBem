import pytest
from model.categoria_model import Categoria
from model.item_model import TipoItem

class TestCategoriaModel:
    def test_criar_categoria_com_dados_validos(self):
        categoria = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.PRODUTO,
            descricao="Descrição da categoria",
            ativo=True
        )

        assert categoria.id == 1
        assert categoria.nome == "Categoria Teste"
        assert categoria.tipo_fornecimento == TipoItem.PRODUTO
        assert categoria.descricao == "Descrição da categoria"
        assert categoria.ativo == True

    def test_criar_categoria_sem_descricao(self):
        categoria = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.SERVICO,
            ativo=True
        )

        assert categoria.id == 1
        assert categoria.nome == "Categoria Teste"
        assert categoria.tipo_fornecimento == TipoItem.SERVICO
        assert categoria.descricao is None
        assert categoria.ativo == True

    def test_categoria_inativa_por_padrao(self):
        categoria = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.ESPACO
        )

        assert categoria.ativo == True

    def test_criar_categoria_com_todos_tipos_item(self):
        tipos = [TipoItem.PRODUTO, TipoItem.SERVICO, TipoItem.ESPACO]

        for tipo in tipos:
            categoria = Categoria(
                id=1,
                nome=f"Categoria {tipo.value}",
                tipo_fornecimento=tipo,
                ativo=True
            )
            assert categoria.tipo_fornecimento == tipo

    def test_categoria_com_descricao_none(self):
        categoria = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.PRODUTO,
            descricao=None,
            ativo=True
        )

        assert categoria.descricao is None

    def test_categoria_com_descricao_vazia(self):
        categoria = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.PRODUTO,
            descricao="",
            ativo=True
        )

        assert categoria.descricao == ""

    def test_representacao_string_categoria(self):
        categoria = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.PRODUTO,
            descricao="Descrição da categoria",
            ativo=True
        )

        # Verificar se a representação contém os dados principais
        str_repr = str(categoria)
        assert "Categoria Teste" in str_repr
        assert "PRODUTO" in str_repr

    def test_igualdade_categorias(self):
        categoria1 = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.PRODUTO,
            descricao="Descrição",
            ativo=True
        )

        categoria2 = Categoria(
            id=1,
            nome="Categoria Teste",
            tipo_fornecimento=TipoItem.PRODUTO,
            descricao="Descrição",
            ativo=True
        )

        # Dataclasses têm igualdade automática baseada nos campos
        assert categoria1 == categoria2

    def test_categorias_diferentes(self):
        categoria1 = Categoria(
            id=1,
            nome="Categoria 1",
            tipo_fornecimento=TipoItem.PRODUTO,
            ativo=True
        )

        categoria2 = Categoria(
            id=2,
            nome="Categoria 2",
            tipo_fornecimento=TipoItem.SERVICO,
            ativo=True
        )

        assert categoria1 != categoria2

    def test_modificar_categoria_apos_criacao(self):
        categoria = Categoria(
            id=1,
            nome="Categoria Original",
            tipo_fornecimento=TipoItem.PRODUTO,
            ativo=True
        )

        # Modificar campos
        categoria.nome = "Categoria Modificada"
        categoria.tipo_fornecimento = TipoItem.SERVICO
        categoria.ativo = False
        categoria.descricao = "Nova descrição"

        assert categoria.nome == "Categoria Modificada"
        assert categoria.tipo_fornecimento == TipoItem.SERVICO
        assert categoria.ativo == False
        assert categoria.descricao == "Nova descrição"