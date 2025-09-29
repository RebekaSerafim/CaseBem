from typing import Optional, List
from util.base_repo import BaseRepo
from sql import casal_sql
from model.casal_model import Casal

class CasalRepo(BaseRepo):
    """Repositório para operações com casais"""

    def __init__(self):
        super().__init__('casal', Casal, casal_sql)

    def _objeto_para_tupla_insert(self, casal: Casal) -> tuple:
        """Prepara dados do casal para inserção"""
        return (
            casal.id_noivo1,
            casal.id_noivo2,
            casal.data_casamento,
            casal.local_previsto,
            casal.orcamento_estimado,
            casal.numero_convidados
        )

    def _objeto_para_tupla_update(self, casal: Casal) -> tuple:
        """Prepara dados do casal para atualização"""
        return (
            casal.data_casamento,
            casal.local_previsto,
            casal.orcamento_estimado,
            casal.numero_convidados,
            casal.id
        )

    def _linha_para_objeto(self, linha: dict) -> Casal:
        """Converte linha do banco em objeto Casal"""
        linha_dict = dict(linha) if hasattr(linha, 'keys') else linha

        return Casal(
            id=linha_dict["id"],
            id_noivo1=linha_dict["id_noivo1"],
            id_noivo2=linha_dict.get("id_noivo2"),
            data_casamento=linha_dict.get("data_casamento"),
            local_previsto=linha_dict.get("local_previsto"),
            orcamento_estimado=linha_dict.get("orcamento_estimado"),
            numero_convidados=linha_dict.get("numero_convidados"),
            data_cadastro=linha_dict.get("data_cadastro")
        )

    def obter_casal_por_noivo(self, id_noivo: int) -> Optional[Casal]:
        """Obtém casal pelo ID de um dos noivos"""
        resultados = self.executar_query(casal_sql.OBTER_CASAL_POR_NOIVO, (id_noivo, id_noivo))
        return self._linha_para_objeto(resultados[0]) if resultados else None

    def obter_casais_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Casal]:
        """Lista casais com paginação"""
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        resultados = self.executar_query(casal_sql.OBTER_CASAL_POR_PAGINA, (limite, offset))
        return [self._linha_para_objeto(row) for row in resultados]

# Instância global do repositório
casal_repo = CasalRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_casal() -> bool:
    return casal_repo.criar_tabela()

def inserir_casal(casal: Casal) -> Optional[int]:
    return casal_repo.inserir(casal)

def atualizar_casal(casal: Casal) -> bool:
    return casal_repo.atualizar(casal)

def excluir_casal(id: int) -> bool:
    return casal_repo.excluir(id)

def obter_casal_por_id(id: int) -> Optional[Casal]:
    """Obtém casal por ID com dados dos noivos carregados"""
    casal = casal_repo.obter_por_id(id)
    if casal:
        # Carrega dados dos noivos para compatibilidade
        from repo import usuario_repo
        casal.noivo1 = usuario_repo.obter_usuario_por_id(casal.id_noivo1)
        if casal.id_noivo2:
            casal.noivo2 = usuario_repo.obter_usuario_por_id(casal.id_noivo2)
    return casal

def obter_casais_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Casal]:
    return casal_repo.obter_casais_por_pagina(numero_pagina, tamanho_pagina)

def obter_casal_por_noivo(id_noivo: int) -> Optional[Casal]:
    return casal_repo.obter_casal_por_noivo(id_noivo)

def listar_casais() -> List[Casal]:
    return casal_repo.listar_todos()
