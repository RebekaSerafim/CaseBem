from typing import Optional, List, Dict, Any
from util.database import obter_conexao
from sql.item_sql import *
from model.item_model import Item, TipoItem

def criar_tabela_item() -> bool:
    """Cria a tabela de itens se não existir"""
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_ITEM)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela item: {e}")
        return False

def inserir_item(item: Item) -> Optional[int]:
    """Insere um novo item e retorna seu ID"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERIR_ITEM, (
                item.id_fornecedor,
                item.tipo.value,
                item.nome,
                item.descricao,
                item.preco,
                item.observacoes,
                item.ativo
            ))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir item: {e}")
        return None

def atualizar_item(item: Item) -> bool:
    """Atualiza um item existente"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_ITEM, (
                item.tipo.value,
                item.nome,
                item.descricao,
                item.preco,
                item.observacoes,
                item.ativo,
                item.id,
                item.id_fornecedor
            ))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar item: {e}")
        return False

def excluir_item(id_item: int, id_fornecedor: int) -> bool:
    """Exclui um item (apenas o próprio fornecedor pode excluir)"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_ITEM, (id_item, id_fornecedor))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir item: {e}")
        return False

def obter_item_por_id(id_item: int) -> Optional[Item]:
    """Obtém um item pelo ID"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITEM_POR_ID, (id_item,))
            resultado = cursor.fetchone()

            if resultado:
                return Item(
                    id=resultado["id"],
                    id_fornecedor=resultado["id_fornecedor"],
                    tipo=TipoItem(resultado["tipo"]),
                    nome=resultado["nome"],
                    descricao=resultado["descricao"],
                    preco=resultado["preco"],
                    observacoes=resultado["observacoes"],
                    ativo=bool(resultado["ativo"]),
                    data_cadastro=resultado["data_cadastro"]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter item por ID: {e}")
        return None

def obter_itens_por_fornecedor(id_fornecedor: int) -> List[Item]:
    """Obtém todos os itens ativos de um fornecedor"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITENS_POR_FORNECEDOR, (id_fornecedor,))
            resultados = cursor.fetchall()

            return [Item(
                id=resultado["id"],
                id_fornecedor=resultado["id_fornecedor"],
                tipo=TipoItem(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter itens por fornecedor: {e}")
        return []

def obter_itens_por_tipo(tipo: TipoItem) -> List[Item]:
    """Obtém todos os itens ativos de um tipo específico"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITENS_POR_TIPO, (tipo.value,))
            resultados = cursor.fetchall()

            return [Item(
                id=resultado["id"],
                id_fornecedor=resultado["id_fornecedor"],
                tipo=TipoItem(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter itens por tipo: {e}")
        return []

def obter_itens_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Item]:
    """Obtém itens com paginação"""
    try:
        with obter_conexao() as conexao:
            limite = tamanho_pagina
            offset = (numero_pagina - 1) * tamanho_pagina
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITENS_POR_PAGINA, (limite, offset))
            resultados = cursor.fetchall()

            return [Item(
                id=resultado["id"],
                id_fornecedor=resultado["id_fornecedor"],
                tipo=TipoItem(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter itens por página: {e}")
        return []

def buscar_itens(termo_busca: str, numero_pagina: int = 1, tamanho_pagina: int = 20) -> List[Item]:
    """Busca itens por termo nos campos nome, descrição e observações"""
    try:
        with obter_conexao() as conexao:
            limite = tamanho_pagina
            offset = (numero_pagina - 1) * tamanho_pagina
            termo_like = f"%{termo_busca}%"
            cursor = conexao.cursor()
            cursor.execute(BUSCAR_ITENS, (termo_like, termo_like, termo_like, limite, offset))
            resultados = cursor.fetchall()

            return [Item(
                id=resultado["id"],
                id_fornecedor=resultado["id_fornecedor"],
                tipo=TipoItem(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao buscar itens: {e}")
        return []

def obter_produtos() -> List[Item]:
    """Obtém todos os produtos ativos"""
    return obter_itens_por_tipo(TipoItem.PRODUTO)

def obter_servicos() -> List[Item]:
    """Obtém todos os serviços ativos"""
    return obter_itens_por_tipo(TipoItem.SERVICO)

def obter_espacos() -> List[Item]:
    """Obtém todos os espaços ativos"""
    return obter_itens_por_tipo(TipoItem.ESPACO)

def contar_itens_por_fornecedor(id_fornecedor: int) -> int:
    """Conta quantos itens ativos um fornecedor possui"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CONTAR_ITENS_POR_FORNECEDOR, (id_fornecedor,))
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar itens por fornecedor: {e}")
        return 0

def obter_estatisticas_itens() -> List[Dict[str, Any]]:
    """Obtém estatísticas dos itens por tipo"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ESTATISTICAS_ITENS)
            resultados = cursor.fetchall()

            return [{
                "tipo": resultado["tipo"],
                "quantidade": resultado["quantidade"],
                "preco_medio": round(resultado["preco_medio"], 2) if resultado["preco_medio"] else 0,
                "preco_minimo": resultado["preco_minimo"],
                "preco_maximo": resultado["preco_maximo"]
            } for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter estatísticas de itens: {e}")
        return []

def ativar_item(id_item: int, id_fornecedor: int) -> bool:
    """Ativa um item"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE item SET ativo = 1 WHERE id = ? AND id_fornecedor = ?",
                         (id_item, id_fornecedor))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao ativar item: {e}")
        return False

def desativar_item(id_item: int, id_fornecedor: int) -> bool:
    """Desativa um item (soft delete)"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE item SET ativo = 0 WHERE id = ? AND id_fornecedor = ?",
                         (id_item, id_fornecedor))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao desativar item: {e}")
        return False