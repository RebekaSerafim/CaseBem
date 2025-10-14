"""
Testes para o modelo ItemOrcamento
"""
import pytest
from core.models.item_orcamento_model import ItemOrcamento


class TestItemOrcamentoModel:
    def test_preco_total_sem_desconto(self):
        """Testa cálculo de preço_total quando desconto é None"""
        # Arrange
        item = ItemOrcamento(
            id=1,
            id_orcamento=1,
            id_item_demanda=1,
            id_item=1,
            quantidade=3,
            preco_unitario=50.0,
            desconto=None
        )
        # Act
        preco_total = item.preco_total
        # Assert
        assert preco_total == 150.0, "Preço total deveria ser 3 * 50 = 150"

    def test_preco_total_com_desconto(self):
        """Testa cálculo de preço_total quando há desconto"""
        # Arrange
        item = ItemOrcamento(
            id=1,
            id_orcamento=1,
            id_item_demanda=1,
            id_item=1,
            quantidade=2,
            preco_unitario=50.0,
            desconto=10.0
        )
        # Act
        preco_total = item.preco_total
        # Assert
        assert preco_total == 90.0, "Preço total deveria ser 2 * 50 - 10 = 90"

    def test_preco_total_com_desconto_zero(self):
        """Testa cálculo de preço_total quando desconto é zero"""
        # Arrange
        item = ItemOrcamento(
            id=1,
            id_orcamento=1,
            id_item_demanda=1,
            id_item=1,
            quantidade=4,
            preco_unitario=25.0,
            desconto=0.0
        )
        # Act
        preco_total = item.preco_total
        # Assert
        assert preco_total == 100.0, "Preço total deveria ser 4 * 25 = 100"

    def test_status_padrao(self):
        """Testa que o status padrão é PENDENTE"""
        # Arrange & Act
        item = ItemOrcamento(
            id=1,
            id_orcamento=1,
            id_item_demanda=1,
            id_item=1,
            quantidade=1,
            preco_unitario=100.0
        )
        # Assert
        assert item.status == "PENDENTE", "Status padrão deveria ser PENDENTE"

    def test_motivo_rejeicao_opcional(self):
        """Testa que motivo_rejeicao é opcional"""
        # Arrange & Act
        item = ItemOrcamento(
            id=1,
            id_orcamento=1,
            id_item_demanda=1,
            id_item=1,
            quantidade=1,
            preco_unitario=100.0,
            status="REJEITADO"
        )
        # Assert
        assert item.motivo_rejeicao is None, "Motivo de rejeição deveria ser None por padrão"

    def test_observacoes_opcional(self):
        """Testa que observacoes é opcional"""
        # Arrange & Act
        item = ItemOrcamento(
            id=1,
            id_orcamento=1,
            id_item_demanda=1,
            id_item=1,
            quantidade=1,
            preco_unitario=100.0
        )
        # Assert
        assert item.observacoes is None, "Observações deveriam ser None por padrão"
