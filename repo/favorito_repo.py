from typing import Optional, List
from util.base_repo import BaseRepo
from sql import favorito_sql
from model.favorito_model import Favorito

class FavoritoRepo(BaseRepo):
    """Repositório para operações com favoritos"""

    def __init__(self):
        super().__init__('favorito', Favorito, favorito_sql)

    def _objeto_para_tupla_insert(self, favorito: Favorito) -> tuple:
        """Prepara dados do favorito para inserção"""
        return (favorito.id_noivo, favorito.id_item)

    def _objeto_para_tupla_update(self, favorito: Favorito) -> tuple:
        """Prepara dados do favorito para atualização"""
        return (favorito.id_noivo, favorito.id_item, favorito.id)

    def _linha_para_objeto(self, linha: dict) -> Favorito:
        """Converte linha do banco em objeto Favorito"""
        linha_dict = dict(linha) if hasattr(linha, 'keys') else linha

        return Favorito(
            id=linha_dict["id"],
            id_noivo=linha_dict["id_noivo"],
            id_item=linha_dict["id_item"],
            data_adicao=linha_dict.get("data_adicao")
        )

# Instância global do repositório
favorito_repo = FavoritoRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_favoritos() -> bool:
    return favorito_repo.criar_tabela()

def adicionar_favorito(id_noivo: int, id_item: int) -> bool:
    """Adiciona um item aos favoritos do noivo"""
    favorito = Favorito(id=0, id_noivo=id_noivo, id_item=id_item)
    resultado = favorito_repo.inserir(favorito)
    return resultado is not None

def remover_favorito(id_noivo: int, id_item: int) -> bool:
    """Remove um item dos favoritos do noivo"""
    return favorito_repo.executar_comando(favorito_sql.EXCLUIR_FAVORITO, (id_noivo, id_item))

def obter_favoritos_por_noivo(id_noivo: int) -> List[dict]:
    """Obtém todos os favoritos de um noivo com dados dos itens"""
    resultados = favorito_repo.executar_query(favorito_sql.OBTER_FAVORITOS_POR_NOIVO, (id_noivo,))
    return [dict(resultado) for resultado in resultados]

def verificar_favorito(id_noivo: int, id_item: int) -> bool:
    """Verifica se um item está nos favoritos do noivo"""
    resultados = favorito_repo.executar_query(favorito_sql.VERIFICAR_FAVORITO, (id_noivo, id_item))
    return resultados[0]["count"] > 0 if resultados else False

def contar_favoritos_por_noivo(id_noivo: int) -> int:
    """Conta o total de favoritos de um noivo"""
    resultados = favorito_repo.executar_query(favorito_sql.CONTAR_FAVORITOS_POR_NOIVO, (id_noivo,))
    return resultados[0]["total"] if resultados else 0

# Funções BaseRepo básicas
def inserir_favorito(favorito: Favorito) -> Optional[int]:
    return favorito_repo.inserir(favorito)

def atualizar_favorito(favorito: Favorito) -> bool:
    return favorito_repo.atualizar(favorito)

def excluir_favorito(id: int) -> bool:
    return favorito_repo.excluir(id)

def obter_favorito_por_id(id: int) -> Optional[Favorito]:
    return favorito_repo.obter_por_id(id)

def listar_favoritos() -> List[Favorito]:
    return favorito_repo.listar_todos()