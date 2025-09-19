from model.prestador_servico_model import PrestadorServico
from repo import prestador_servico_repo, usuario_repo, servico_repo, profissional_repo

class TestPrestadorServicoRepo:
    def test_criar_tabela_prestador_servico(self, test_db):
        assert prestador_servico_repo.criar_tabela_prestador_servico() is True

    def test_inserir_prestador_servico(self, test_db, prestador_servico_exemplo, profissional_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        profissional_repo.criar_tabela_profissional()
        profissional_repo.inserir_profissional(profissional_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        
        # Act
        ids = prestador_servico_repo.inserir_prestador_servico(prestador_servico_exemplo)
        
        # Assert
        assert ids == (1, 1)

    def test_atualizar_prestador_servico(self, test_db, profissional_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        profissional_repo.criar_tabela_profissional()
        profissional_repo.inserir_profissional(profissional_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        
        ps = PrestadorServico(1, 1, "Observações iniciais", 100.0)
        prestador_servico_repo.inserir_prestador_servico(ps)
        
        # Act
        ps_atualizado = PrestadorServico(1, 1, "Observações atualizadas", 150.0)
        sucesso = prestador_servico_repo.atualizar_prestador_servico(ps_atualizado)
        
        # Assert
        assert sucesso is True
        ps_obtido = prestador_servico_repo.obter_prestador_servico_por_id(1, 1)
        assert ps_obtido.observacoes == "Observações atualizadas"
        assert ps_obtido.preco == 150.0

    def test_excluir_prestador_servico(self, test_db, prestador_servico_exemplo, profissional_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        profissional_repo.criar_tabela_profissional()
        profissional_repo.inserir_profissional(profissional_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        prestador_servico_repo.inserir_prestador_servico(prestador_servico_exemplo)
        
        # Act
        sucesso = prestador_servico_repo.excluir_prestador_servico(1, 1)
        
        # Assert
        assert sucesso is True
        assert prestador_servico_repo.obter_prestador_servico_por_id(1, 1) is None

    def test_obter_prestador_servico_por_id(self, test_db, prestador_servico_exemplo, profissional_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        profissional_repo.criar_tabela_profissional()
        profissional_repo.inserir_profissional(profissional_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        prestador_servico_repo.inserir_prestador_servico(prestador_servico_exemplo)
        
        # Act
        ps = prestador_servico_repo.obter_prestador_servico_por_id(1, 1)
        
        # Assert
        assert ps is not None
        assert ps.id_profissional == 1
        assert ps.id_servico == 1
        assert ps.observacoes == "Observações teste"
        assert ps.preco == 100.0

    def test_obter_prestadores_servico_por_pagina(self, test_db, profissional_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        profissional_repo.criar_tabela_profissional()
        profissional_repo.inserir_profissional(profissional_exemplo)
        for servico in lista_servicos_exemplo[:5]:
            servico_repo.inserir_servico(servico)
        
        # Inserir relações
        for i in range(1, 6):
            ps = PrestadorServico(1, i, f"Observações {i}", 100.0 * i)
            prestador_servico_repo.inserir_prestador_servico(ps)
        
        # Act
        pagina = prestador_servico_repo.obter_prestadores_servico_por_pagina(1, 3)
        
        # Assert
        assert len(pagina) == 3
        assert all(isinstance(ps, PrestadorServico) for ps in pagina)

    def test_obter_prestador_servico_inexistente(self, test_db):
        # Arrange
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        # Act
        ps = prestador_servico_repo.obter_prestador_servico_por_id(999, 999)
        
        # Assert
        assert ps is None

    def test_atualizar_prestador_servico_inexistente(self, test_db):
        # Arrange
        prestador_servico_repo.criar_tabela_prestador_servico()
        ps = PrestadorServico(999, 999, "Observações", 100.0)
        
        # Act
        sucesso = prestador_servico_repo.atualizar_prestador_servico(ps)
        
        # Assert
        assert sucesso is False

    def test_excluir_prestador_servico_inexistente(self, test_db, profissional_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        servico_repo.criar_tabela_servicos()
        prestador_servico_repo.criar_tabela_prestador_servico()
        
        # Criar usuário e serviço necessários para satisfazer foreign key
        profissional_repo.criar_tabela_profissional()
        profissional_repo.inserir_profissional(profissional_exemplo)
        servico_repo.inserir_servico(servico_exemplo)
        
        # Act
        sucesso = prestador_servico_repo.excluir_prestador_servico(999, 999)
        
        # Assert
        assert sucesso is False