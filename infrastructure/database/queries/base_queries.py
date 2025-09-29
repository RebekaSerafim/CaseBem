"""
Queries SQL base que podem ser reutilizadas

Este módulo contém funções utilitárias para geração dinâmica de SQL,
reduzindo duplicação e centralizando a lógica de construção de queries.
"""

from typing import Dict, List


def gerar_create_table(nome_tabela: str, colunas: Dict[str, str]) -> str:
    """
    Gera SQL para CREATE TABLE de forma dinâmica

    Args:
        nome_tabela: Nome da tabela a ser criada
        colunas: Dict com {nome_coluna: definição_sql}

    Returns:
        SQL do CREATE TABLE formatado

    Example:
        >>> colunas = {
        ...     "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        ...     "nome": "TEXT NOT NULL",
        ...     "email": "TEXT UNIQUE NOT NULL"
        ... }
        >>> sql = gerar_create_table("usuario", colunas)
        >>> print(sql)
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """
    colunas_sql = ",\n        ".join([
        f"{nome} {definicao}" for nome, definicao in colunas.items()
    ])

    return f"""CREATE TABLE IF NOT EXISTS {nome_tabela} (
        {colunas_sql}
    );"""


def gerar_insert(nome_tabela: str, colunas: List[str]) -> str:
    """
    Gera SQL para INSERT

    Args:
        nome_tabela: Nome da tabela
        colunas: Lista com nomes das colunas

    Returns:
        SQL do INSERT com placeholders

    Example:
        >>> sql = gerar_insert("usuario", ["nome", "email"])
        >>> print(sql)
        INSERT INTO usuario (nome, email) VALUES (?, ?)
    """
    placeholders = ", ".join(["?" for _ in colunas])
    colunas_str = ", ".join(colunas)

    return f"INSERT INTO {nome_tabela} ({colunas_str}) VALUES ({placeholders})"


def gerar_update(nome_tabela: str, colunas: List[str], condicao: str = "id = ?") -> str:
    """
    Gera SQL para UPDATE

    Args:
        nome_tabela: Nome da tabela
        colunas: Lista com nomes das colunas a atualizar
        condicao: Condição WHERE (padrão: "id = ?")

    Returns:
        SQL do UPDATE

    Example:
        >>> sql = gerar_update("usuario", ["nome", "email"])
        >>> print(sql)
        UPDATE usuario SET nome = ?, email = ? WHERE id = ?
    """
    sets = ", ".join([f"{col} = ?" for col in colunas])
    return f"UPDATE {nome_tabela} SET {sets} WHERE {condicao}"


def gerar_select_all(nome_tabela: str, condicao: str = None, order_by: str = None) -> str:
    """
    Gera SQL para SELECT

    Args:
        nome_tabela: Nome da tabela
        condicao: Condição WHERE (opcional)
        order_by: Ordenação (opcional)

    Returns:
        SQL do SELECT

    Example:
        >>> sql = gerar_select_all("usuario", "ativo = 1", "nome ASC")
        >>> print(sql)
        SELECT * FROM usuario WHERE ativo = 1 ORDER BY nome ASC
    """
    sql = f"SELECT * FROM {nome_tabela}"

    if condicao:
        sql += f" WHERE {condicao}"

    if order_by:
        sql += f" ORDER BY {order_by}"

    return sql


def gerar_select_por_id(nome_tabela: str) -> str:
    """
    Gera SQL para SELECT por ID

    Args:
        nome_tabela: Nome da tabela

    Returns:
        SQL do SELECT por ID

    Example:
        >>> sql = gerar_select_por_id("usuario")
        >>> print(sql)
        SELECT * FROM usuario WHERE id = ?
    """
    return f"SELECT * FROM {nome_tabela} WHERE id = ?"


def gerar_delete(nome_tabela: str, condicao: str = "id = ?") -> str:
    """
    Gera SQL para DELETE

    Args:
        nome_tabela: Nome da tabela
        condicao: Condição WHERE (padrão: "id = ?")

    Returns:
        SQL do DELETE

    Example:
        >>> sql = gerar_delete("usuario")
        >>> print(sql)
        DELETE FROM usuario WHERE id = ?
    """
    return f"DELETE FROM {nome_tabela} WHERE {condicao}"


def gerar_select_paginado(nome_tabela: str, condicao: str = None, order_by: str = "id") -> str:
    """
    Gera SQL para SELECT com paginação

    Args:
        nome_tabela: Nome da tabela
        condicao: Condição WHERE (opcional)
        order_by: Campo para ordenação (padrão: "id")

    Returns:
        SQL do SELECT paginado

    Example:
        >>> sql = gerar_select_paginado("usuario", "ativo = 1")
        >>> print(sql)
        SELECT * FROM usuario WHERE ativo = 1 ORDER BY id LIMIT ? OFFSET ?
    """
    sql = f"SELECT * FROM {nome_tabela}"

    if condicao:
        sql += f" WHERE {condicao}"

    sql += f" ORDER BY {order_by} LIMIT ? OFFSET ?"

    return sql


def gerar_count(nome_tabela: str, condicao: str = None) -> str:
    """
    Gera SQL para COUNT

    Args:
        nome_tabela: Nome da tabela
        condicao: Condição WHERE (opcional)

    Returns:
        SQL do COUNT

    Example:
        >>> sql = gerar_count("usuario", "ativo = 1")
        >>> print(sql)
        SELECT COUNT(*) FROM usuario WHERE ativo = 1
    """
    sql = f"SELECT COUNT(*) FROM {nome_tabela}"

    if condicao:
        sql += f" WHERE {condicao}"

    return sql


# Queries comuns reutilizáveis
QUERIES_COMUNS = {
    'verificar_existencia': "SELECT COUNT(*) FROM {tabela} WHERE {condicao}",
    'soft_delete': "UPDATE {tabela} SET ativo = 0 WHERE id = ?",
    'soft_restore': "UPDATE {tabela} SET ativo = 1 WHERE id = ?",
    'buscar_ativos': "SELECT * FROM {tabela} WHERE ativo = 1 ORDER BY {order_by}",
    'contar_ativos': "SELECT COUNT(*) FROM {tabela} WHERE ativo = 1"
}