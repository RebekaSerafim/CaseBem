from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemOrcamento:
    """
    Representa um item do orçamento vinculado a um item da demanda.

    IMPORTANTE (V2): ItemOrcamento agora vincula:
    - id_orcamento: O orçamento sendo criado
    - id_item_demanda: O item específico da demanda que está sendo atendido
    - id_item: O item do catálogo do fornecedor que atende a demanda

    Isso permite que um fornecedor:
    1. Atenda múltiplos itens de uma demanda
    2. Ofereça múltiplas opções para o mesmo item_demanda
    3. Mantenha rastreabilidade do que está sendo atendido

    IMPORTANTE (V3): ItemOrcamento agora possui status individual:
    - PENDENTE: Aguardando decisão do noivo
    - ACEITO: Noivo aceitou este item
    - REJEITADO: Noivo rejeitou este item

    O status do orçamento é derivado dos status dos itens.
    """
    id: int
    id_orcamento: int
    id_item_demanda: int
    id_item: int
    quantidade: int
    preco_unitario: float
    observacoes: Optional[str] = None
    desconto: Optional[float] = None
    status: str = "PENDENTE"  # PENDENTE, ACEITO, REJEITADO

    @property
    def preco_total(self) -> float:
        """Calcula o preço total do item considerando quantidade e desconto"""
        subtotal = self.quantidade * self.preco_unitario
        if self.desconto:
            return subtotal - self.desconto
        return subtotal