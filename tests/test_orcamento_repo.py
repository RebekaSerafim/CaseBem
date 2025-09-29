from datetime import datetime, timedelta
from model.orcamento_model import Orcamento
from model.demanda_model import Demanda
from model.casal_model import Casal
from model.categoria_model import Categoria
from model.tipo_fornecimento_model import TipoFornecimento
from repo import orcamento_repo, demanda_repo, casal_repo, usuario_repo, categoria_repo

class TestOrcamentoRepo:
    def test_criar_tabela_orcamento(self, test_db):
        # Criar tabelas dependentes primeiro
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        # Agora criar tabela orcamento
        assert orcamento_repo.criar_tabela_orcamento() is True

    def test_inserir_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Criar orçamento
        orcamento = Orcamento(
            id=0,
            id_demanda=id_demanda,
            id_fornecedor_prestador=id_fornecedor,
            data_hora_cadastro=datetime.now(),
            data_hora_validade=datetime.now() + timedelta(days=30),
            status="PENDENTE",
            observacoes="Orçamento de teste",
            valor_total=1500.00
        )
        
        # Act
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Assert
        assert id_orcamento is not None
        orcamento_salvo = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_salvo is not None
        assert orcamento_salvo.id_demanda == id_demanda
        assert orcamento_salvo.id_fornecedor_prestador == id_fornecedor
        assert orcamento_salvo.status == "PENDENTE"
        assert orcamento_salvo.valor_total == 1500.00

    def test_atualizar_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), 
                            datetime.now() + timedelta(days=30), "PENDENTE", 
                            "Orçamento inicial", 1500.00)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamento_atualizado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        orcamento_atualizado.status = "ACEITO"
        orcamento_atualizado.valor_total = 2000.00
        orcamento_atualizado.observacoes = "Orçamento atualizado"
        sucesso = orcamento_repo.atualizar_orcamento(orcamento_atualizado)
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_verificado.status == "ACEITO"
        assert orcamento_verificado.valor_total == 2000.00
        assert orcamento_verificado.observacoes == "Orçamento atualizado"

    def test_atualizar_status_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        sucesso = orcamento_repo.atualizar_status_orcamento(id_orcamento, "ACEITO")
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_verificado.status == "ACEITO"

    def test_atualizar_valor_total_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 100.00)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        sucesso = orcamento_repo.atualizar_valor_total_orcamento(id_orcamento, 250.00)
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        assert orcamento_verificado.valor_total == 250.00

    def test_aceitar_orcamento_e_rejeitar_outros(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir múltiplos orçamentos
        ids_orcamentos = []
        for i, id_fornecedor in enumerate(ids_fornecedores):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            ids_orcamentos.append(orcamento_repo.inserir_orcamento(orcamento))
        
        # Act - Aceitar o segundo orçamento
        sucesso = orcamento_repo.aceitar_orcamento_e_rejeitar_outros(ids_orcamentos[1], id_demanda)
        
        # Assert
        assert sucesso is True
        # Verificar que o segundo foi aceito
        orcamento_aceito = orcamento_repo.obter_orcamento_por_id(ids_orcamentos[1])
        assert orcamento_aceito.status == "ACEITO"
        
        # Verificar que os outros foram rejeitados
        orcamento_rejeitado1 = orcamento_repo.obter_orcamento_por_id(ids_orcamentos[0])
        assert orcamento_rejeitado1.status == "REJEITADO"
        
        orcamento_rejeitado2 = orcamento_repo.obter_orcamento_por_id(ids_orcamentos[2])
        assert orcamento_rejeitado2.status == "REJEITADO"

    def test_excluir_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        sucesso = orcamento_repo.excluir_orcamento(id_orcamento)
        
        # Assert
        assert sucesso is True
        assert orcamento_repo.obter_orcamento_por_id(id_orcamento) is None

    def test_obter_orcamento_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Act
        orcamento = orcamento_repo.obter_orcamento_por_id(999)
        
        # Assert
        assert orcamento is None

    def test_obter_orcamentos_por_demanda(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir orçamentos
        for i, id_fornecedor in enumerate(ids_fornecedores):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamentos = orcamento_repo.obter_orcamentos_por_demanda(id_demanda)
        
        # Assert
        assert len(orcamentos) == 3
        assert all(o.id_demanda == id_demanda for o in orcamentos)

    def test_obter_orcamentos_por_fornecedor_prestador(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        
        # Criar múltiplas demandas
        ids_demandas = []
        for i in range(3):
            demanda = Demanda(
                id=0,
                id_casal=1,
                id_categoria=1,
                titulo="Demanda de teste",
                descricao="Descrição da demanda de teste"
            )
            ids_demandas.append(demanda_repo.inserir_demanda(demanda))
        
        # Inserir orçamentos do mesmo fornecedor
        for id_demanda in ids_demandas:
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", None, 100.00)
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamentos = orcamento_repo.obter_orcamentos_por_fornecedor_prestador(id_fornecedor)
        
        # Assert
        assert len(orcamentos) == 3
        assert all(o.id_fornecedor_prestador == id_fornecedor for o in orcamentos)

    def test_obter_orcamentos_por_status(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir orçamentos com status diferentes
        status_list = ["PENDENTE", "ACEITO", "PENDENTE"]
        for i, (id_fornecedor, status) in enumerate(zip(ids_fornecedores, status_list)):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                status, None, 100.00)
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        orcamentos_pendentes = orcamento_repo.obter_orcamentos_por_status("PENDENTE")
        orcamentos_aceitos = orcamento_repo.obter_orcamentos_por_status("ACEITO")
        
        # Assert
        assert len(orcamentos_pendentes) == 2
        assert all(o.status == "PENDENTE" for o in orcamentos_pendentes)
        assert len(orcamentos_aceitos) == 1
        assert all(o.status == "ACEITO" for o in orcamentos_aceitos)

    def test_obter_orcamentos_por_pagina(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:5]:
            ids_fornecedores.append(usuario_repo.inserir_usuario(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir_casal(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda de teste",
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        # Inserir 10 orçamentos
        for i in range(10):
            orcamento = Orcamento(0, id_demanda, ids_fornecedores[i % 5], datetime.now(), 
                                None, "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            orcamento_repo.inserir_orcamento(orcamento)
        
        # Act
        pagina1 = orcamento_repo.obter_orcamentos_por_pagina(1, 5)
        pagina2 = orcamento_repo.obter_orcamentos_por_pagina(2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 5
        assert all(isinstance(o, Orcamento) for o in pagina1)
        assert all(isinstance(o, Orcamento) for o in pagina2)