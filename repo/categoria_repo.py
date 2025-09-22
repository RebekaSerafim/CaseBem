from typing import Optional, List
from util.database import obter_conexao
from sql.categoria_sql import *
from model.categoria_model import Categoria
from model.item_model import TipoItem

def criar_tabela_categorias() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_CATEGORIA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categoria: {e}")
        return False

def inserir_categoria(categoria: Categoria) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_CATEGORIA,
            (categoria.nome, categoria.tipo_fornecimento.value, categoria.descricao, categoria.ativo))
        return cursor.lastrowid

def atualizar_categoria(categoria: Categoria) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_CATEGORIA,
            (categoria.nome, categoria.tipo_fornecimento.value, categoria.descricao, categoria.ativo, categoria.id))
        return (cursor.rowcount > 0)

def excluir_categoria(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXCLUIR_CATEGORIA, (id,))
        return (cursor.rowcount > 0)

def obter_categoria_por_id(id: int) -> Optional[Categoria]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CATEGORIA_POR_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Categoria(
                id=resultado["id"],
                nome=resultado["nome"],
                tipo_fornecimento=TipoItem(resultado["tipo_fornecimento"]),
                descricao=resultado["descricao"],
                ativo=bool(resultado["ativo"]))
    return None

def obter_categorias_por_tipo(tipo_fornecimento: TipoItem) -> List[Categoria]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CATEGORIAS_POR_TIPO, (tipo_fornecimento.value,))
        resultados = cursor.fetchall()
        return [Categoria(
            id=resultado["id"],
            nome=resultado["nome"],
            tipo_fornecimento=TipoItem(resultado["tipo_fornecimento"]),
            descricao=resultado["descricao"],
            ativo=bool(resultado["ativo"])
        ) for resultado in resultados]

def obter_categorias() -> List[Categoria]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_TODAS_CATEGORIAS)
        resultados = cursor.fetchall()
        return [Categoria(
            id=resultado["id"],
            nome=resultado["nome"],
            tipo_fornecimento=TipoItem(resultado["tipo_fornecimento"]),
            descricao=resultado["descricao"],
            ativo=bool(resultado["ativo"])
        ) for resultado in resultados]

def obter_categorias_ativas() -> List[Categoria]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CATEGORIAS_ATIVAS)
        resultados = cursor.fetchall()
        return [Categoria(
            id=resultado["id"],
            nome=resultado["nome"],
            tipo_fornecimento=TipoItem(resultado["tipo_fornecimento"]),
            descricao=resultado["descricao"],
            ativo=bool(resultado["ativo"])
        ) for resultado in resultados]

def obter_categorias_por_tipo_ativas(tipo_fornecimento: TipoItem) -> List[Categoria]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CATEGORIAS_POR_TIPO_ATIVAS, (tipo_fornecimento.value,))
        resultados = cursor.fetchall()
        return [Categoria(
            id=resultado["id"],
            nome=resultado["nome"],
            tipo_fornecimento=TipoItem(resultado["tipo_fornecimento"]),
            descricao=resultado["descricao"],
            ativo=bool(resultado["ativo"])
        ) for resultado in resultados]

def contar_categorias() -> int:
    """Conta o total de categorias no sistema"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM categoria")
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar categorias: {e}")
        return 0

def obter_categoria_por_nome(nome: str, tipo_fornecimento: TipoItem) -> Optional[Categoria]:
    """Busca uma categoria pelo nome e tipo de fornecimento"""
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CATEGORIA_POR_NOME, (nome, tipo_fornecimento.value))
        resultado = cursor.fetchone()
        if resultado:
            return Categoria(
                id=resultado["id"],
                nome=resultado["nome"],
                tipo_fornecimento=TipoItem(resultado["tipo_fornecimento"]),
                descricao=resultado["descricao"],
                ativo=bool(resultado["ativo"]))
    return None

def buscar_categorias(busca: str = "", tipo_fornecimento: str = "", status: str = "") -> List[Categoria]:
    """Busca categorias com filtros"""
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        # Preparar parâmetros para busca LIKE
        busca_like = f"%{busca}%" if busca else ""

        cursor.execute(BUSCAR_CATEGORIAS, (
            busca, busca_like, busca_like,  # busca por nome/descrição
            tipo_fornecimento, tipo_fornecimento,  # filtro por tipo
            status, status, status  # filtro por status
        ))

        resultados = cursor.fetchall()
        return [Categoria(
            id=resultado["id"],
            nome=resultado["nome"],
            tipo_fornecimento=TipoItem(resultado["tipo_fornecimento"]),
            descricao=resultado["descricao"],
            ativo=bool(resultado["ativo"])
        ) for resultado in resultados]

def ativar_categoria(id: int) -> bool:
    """Ativa uma categoria"""
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATIVAR_CATEGORIA, (id,))
        return (cursor.rowcount > 0)

def desativar_categoria(id: int) -> bool:
    """Desativa uma categoria"""
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DESATIVAR_CATEGORIA, (id,))
        return (cursor.rowcount > 0)