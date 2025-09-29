from typing import Optional, List, Dict, Any
from util.base_repo import BaseRepo
from sql import item_sql
from model.item_model import Item
from model.tipo_fornecimento_model import TipoFornecimento
from repo.categoria_repo import obter_categoria_por_id

def validar_categoria_para_tipo(tipo: TipoFornecimento, id_categoria: int) -> bool:
    """Valida se uma categoria pertence a um tipo específico"""
    categoria = obter_categoria_por_id(id_categoria)
    if not categoria:
        return False
    return categoria.tipo_fornecimento == tipo

class ItemRepo(BaseRepo):
    """Repositório para operações com itens"""

    def __init__(self):
        super().__init__('item', Item, item_sql)

    def inserir(self, item: Item) -> Optional[int]:
        """Insere um novo item com validação de categoria (override do BaseRepo)"""
        try:
            # Validar se a categoria pertence ao tipo do item
            if not validar_categoria_para_tipo(item.tipo, item.id_categoria):
                raise ValueError(f"Categoria {item.id_categoria} não pertence ao tipo {item.tipo.value}")

            # Chama o método base
            return super().inserir(item)
        except Exception as e:
            print(f"Erro ao inserir item: {e}")
            return None

    def atualizar(self, item: Item) -> bool:
        """Atualiza um item com validação de categoria (override do BaseRepo)"""
        try:
            # Validar se a categoria pertence ao tipo do item
            if not validar_categoria_para_tipo(item.tipo, item.id_categoria):
                raise ValueError(f"Categoria {item.id_categoria} não pertence ao tipo {item.tipo.value}")

            # Chama o método base
            return super().atualizar(item)
        except Exception as e:
            print(f"Erro ao atualizar item: {e}")
            return False

    def excluir_item_fornecedor(self, id_item: int, id_fornecedor: int) -> bool:
        """Exclui um item (apenas o próprio fornecedor pode excluir)"""
        try:
            return self.executar_comando(item_sql.EXCLUIR_ITEM, (id_item, id_fornecedor))
        except Exception as e:
            print(f"Erro ao excluir item: {e}")
            return False

    def _objeto_para_tupla_insert(self, item: Item) -> tuple:
        """Prepara dados do item para inserção"""
        return (
            item.id_fornecedor,
            item.tipo.value,
            item.nome,
            item.descricao,
            item.preco,
            item.id_categoria,
            item.observacoes,
            item.ativo
        )

    def _objeto_para_tupla_update(self, item: Item) -> tuple:
        """Prepara dados do item para atualização (inclui id_fornecedor para validação)"""
        return (
            item.tipo.value,
            item.nome,
            item.descricao,
            item.preco,
            item.id_categoria,
            item.observacoes,
            item.ativo,
            item.id,
            item.id_fornecedor
        )

    def _linha_para_objeto(self, linha: dict) -> Item:
        """Converte linha do banco em objeto Item"""
        # Função helper para acessar dados de sqlite3.Row
        def safe_get(row, key, default=None):
            try:
                return row[key] if row[key] is not None else default
            except (KeyError, IndexError):
                return default

        return Item(
            id=linha["id"],
            id_fornecedor=linha["id_fornecedor"],
            tipo=TipoFornecimento(linha["tipo"]),
            nome=linha["nome"],
            descricao=linha["descricao"],
            preco=linha["preco"],
            id_categoria=linha["id_categoria"],
            observacoes=safe_get(linha, "observacoes"),
            ativo=bool(safe_get(linha, "ativo", True)),
            data_cadastro=safe_get(linha, "data_cadastro")
        )

    def obter_itens_por_fornecedor(self, id_fornecedor: int) -> List[Item]:
        """Obtém todos os itens ativos de um fornecedor"""
        try:
            resultados = self.executar_query(item_sql.OBTER_ITENS_POR_FORNECEDOR, (id_fornecedor,))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter itens por fornecedor: {e}")
            return []

    def obter_itens_por_tipo(self, tipo: TipoFornecimento) -> List[Item]:
        """Obtém todos os itens ativos de um tipo específico"""
        try:
            resultados = self.executar_query(item_sql.OBTER_ITENS_POR_TIPO, (tipo.value,))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter itens por tipo: {e}")
            return []

    def obter_itens_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Item]:
        """Obtém itens com paginação"""
        try:
            offset = (numero_pagina - 1) * tamanho_pagina
            resultados = self.executar_query(item_sql.OBTER_ITENS_POR_PAGINA, (tamanho_pagina, offset))
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter itens por página: {e}")
            return []

    def buscar_itens(self, termo_busca: str, numero_pagina: int = 1, tamanho_pagina: int = 20) -> List[Item]:
        """Busca itens por termo"""
        try:
            busca_param = f"%{termo_busca}%"
            offset = (numero_pagina - 1) * tamanho_pagina
            resultados = self.executar_query(
                item_sql.BUSCAR_ITENS,
                (busca_param, busca_param, busca_param, tamanho_pagina, offset)
            )
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao buscar itens: {e}")
            return []

    def obter_produtos(self) -> List[Item]:
        """Obtém todos os produtos ativos"""
        try:
            resultados = self.executar_query(item_sql.OBTER_PRODUTOS)
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter produtos: {e}")
            return []

    def obter_servicos(self) -> List[Item]:
        """Obtém todos os serviços ativos"""
        try:
            resultados = self.executar_query(item_sql.OBTER_SERVICOS)
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter serviços: {e}")
            return []

    def obter_espacos(self) -> List[Item]:
        """Obtém todos os espaços ativos"""
        try:
            resultados = self.executar_query(item_sql.OBTER_ESPACOS)
            return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao obter espaços: {e}")
            return []

    def contar_itens_por_fornecedor(self, id_fornecedor: int) -> int:
        """Conta itens ativos de um fornecedor"""
        try:
            resultados = self.executar_query(item_sql.CONTAR_ITENS_POR_FORNECEDOR, (id_fornecedor,))
            return resultados[0]["total"] if resultados else 0
        except Exception as e:
            print(f"Erro ao contar itens por fornecedor: {e}")
            return 0

    def obter_estatisticas_itens(self) -> List[Dict[str, Any]]:
        """Obtém estatísticas de itens por tipo"""
        try:
            resultados = self.executar_query(item_sql.OBTER_ESTATISTICAS_ITENS)
            return resultados
        except Exception as e:
            print(f"Erro ao obter estatísticas de itens: {e}")
            return []

    def contar_itens(self) -> int:
        """Conta total de itens"""
        try:
            resultados = self.executar_query(item_sql.CONTAR_ITENS)
            return resultados[0]["total"] if resultados else 0
        except Exception as e:
            print(f"Erro ao contar itens: {e}")
            return 0

    def contar_itens_por_tipo(self, tipo: TipoFornecimento) -> int:
        """Conta itens de um tipo específico"""
        try:
            resultados = self.executar_query(item_sql.CONTAR_ITENS_POR_TIPO, (tipo.value,))
            return resultados[0]["total"] if resultados else 0
        except Exception as e:
            print(f"Erro ao contar itens por tipo: {e}")
            return 0

item_repo = ItemRepo()

def criar_tabela_item() -> bool:
    return item_repo.criar_tabela()

def inserir_item(item: Item) -> Optional[int]:
    return item_repo.inserir(item)

def atualizar_item(item: Item) -> bool:
    return item_repo.atualizar(item)

def excluir_item(id_item: int, id_fornecedor: int) -> bool:
    return item_repo.excluir_item_fornecedor(id_item, id_fornecedor)

def obter_item_por_id(id_item: int) -> Optional[Item]:
    return item_repo.obter_por_id(id_item)

def obter_itens_por_fornecedor(id_fornecedor: int) -> List[Item]:
    return item_repo.obter_itens_por_fornecedor(id_fornecedor)

def obter_itens_por_tipo(tipo: TipoFornecimento) -> List[Item]:
    return item_repo.obter_itens_por_tipo(tipo)

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
                tipo=TipoFornecimento(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"],
                id_categoria=resultado["id_categoria"]
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
                tipo=TipoFornecimento(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"],
                id_categoria=resultado["id_categoria"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao buscar itens: {e}")
        return []

def obter_produtos() -> List[Item]:
    """Obtém todos os produtos ativos"""
    return obter_itens_por_tipo(TipoFornecimento.PRODUTO)

def obter_servicos() -> List[Item]:
    """Obtém todos os serviços ativos"""
    return obter_itens_por_tipo(TipoFornecimento.SERVICO)

def obter_espacos() -> List[Item]:
    """Obtém todos os espaços ativos"""
    return obter_itens_por_tipo(TipoFornecimento.ESPACO)

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

def obter_itens_publicos(tipo: Optional[str] = None, busca: Optional[str] = None,
                        categoria: Optional[int] = None, pagina: int = 1, tamanho_pagina: int = 12) -> tuple[List[dict], int]:
    """
    Obtém itens públicos com filtros opcionais e paginação

    Args:
        tipo: Filtro por tipo (produto, servico, espaco)
        busca: Termo de busca textual
        categoria: Filtro por categoria
        pagina: Número da página (começa em 1)
        tamanho_pagina: Quantidade de itens por página

    Returns:
        Tupla com (lista de itens, total de itens)
    """
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Preparar parâmetros para busca
            offset = (pagina - 1) * tamanho_pagina

            # Mapear tipos de URL para tipos do banco
            tipo_map = {
                'produto': 'PRODUTO',
                'servico': 'SERVIÇO',
                'espaco': 'ESPAÇO'
            }
            tipo_param = tipo_map.get(tipo) if tipo else None
            # Converter busca vazia para None para funcionar corretamente com SQL
            busca = busca if busca and busca.strip() else None
            busca_like = f"%{busca}%" if busca else None

            # Contar total de itens
            cursor.execute(CONTAR_ITENS_PUBLICOS_FILTRADOS, (
                tipo_param, tipo_param,
                busca, busca_like, busca_like, busca_like,
                categoria, categoria
            ))
            total = cursor.fetchone()["total"]

            # Buscar itens da página
            cursor.execute(OBTER_ITENS_PUBLICOS_FILTRADOS, (
                tipo_param, tipo_param,
                busca, busca_like, busca_like, busca_like,
                categoria, categoria,
                tamanho_pagina, offset
            ))
            resultados = cursor.fetchall()

            itens = []
            for resultado in resultados:
                item_dict = {
                    "id": resultado["id"],
                    "id_fornecedor": resultado["id_fornecedor"],
                    "tipo": resultado["tipo"],
                    "nome": resultado["nome"],
                    "descricao": resultado["descricao"],
                    "preco": resultado["preco"],
                    "observacoes": resultado["observacoes"],
                    "ativo": bool(resultado["ativo"]),
                    "data_cadastro": resultado["data_cadastro"],
                    "id_categoria": resultado["id_categoria"],
                    "categoria_nome": resultado["categoria_nome"],
                    "fornecedor_nome": resultado["fornecedor_nome"],
                    "fornecedor_empresa": resultado["fornecedor_empresa"]
                }
                itens.append(item_dict)

            return itens, total

    except Exception as e:
        print(f"Erro ao obter itens públicos: {e}")
        return [], 0

def obter_item_publico_por_id(id_item: int) -> Optional[dict]:
    """Obtém um item específico com informações do fornecedor para exibição pública"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            query = """
            SELECT i.id, i.id_fornecedor, i.tipo, i.nome, i.descricao, i.preco, i.observacoes, i.ativo, i.data_cadastro,
                   u.nome as fornecedor_nome, u.email as fornecedor_email, u.telefone as fornecedor_telefone,
                   f.nome_empresa as fornecedor_empresa, f.descricao as fornecedor_descricao,
                   c.nome as categoria_nome, c.descricao as categoria_descricao
            FROM item i
            JOIN usuario u ON i.id_fornecedor = u.id
            LEFT JOIN fornecedor f ON i.id_fornecedor = f.id
            LEFT JOIN categoria c ON i.id_categoria = c.id
            WHERE i.id = ? AND i.ativo = 1
            """
            cursor.execute(query, (id_item,))
            resultado = cursor.fetchone()

            if resultado:
                return {
                    "id": resultado["id"],
                    "id_fornecedor": resultado["id_fornecedor"],
                    "tipo": resultado["tipo"],
                    "nome": resultado["nome"],
                    "descricao": resultado["descricao"],
                    "preco": resultado["preco"],
                    "observacoes": resultado["observacoes"],
                    "ativo": bool(resultado["ativo"]),
                    "data_cadastro": resultado["data_cadastro"],
                    "categoria": {
                        "nome": resultado["categoria_nome"],
                        "descricao": resultado["categoria_descricao"]
                    } if resultado["categoria_nome"] else None,
                    "fornecedor": {
                        "nome": resultado["fornecedor_nome"],
                        "email": resultado["fornecedor_email"],
                        "telefone": resultado["fornecedor_telefone"],
                        "empresa": resultado["fornecedor_empresa"],
                        "descricao": resultado["fornecedor_descricao"]
                    }
                }
            return None
    except Exception as e:
        print(f"Erro ao obter item público por ID: {e}")
        return None

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
def contar_itens() -> int:
    return item_repo.contar_itens()

def contar_itens_por_tipo(tipo: TipoFornecimento) -> int:
    return item_repo.contar_itens_por_tipo(tipo)

def obter_itens_paginado(pagina: int, tamanho_pagina: int) -> tuple[List[Item], int]:
    """Obtém itens paginados e retorna lista de itens e total"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Contar total de itens
            cursor.execute("SELECT COUNT(*) as total FROM item")
            total = cursor.fetchone()["total"]

            # Buscar itens da página
            offset = (pagina - 1) * tamanho_pagina
            cursor.execute("SELECT * FROM item ORDER BY id DESC LIMIT ? OFFSET ?", (tamanho_pagina, offset))
            resultados = cursor.fetchall()

            itens = [Item(
                id=resultado["id"],
                id_fornecedor=resultado["id_fornecedor"],
                tipo=TipoFornecimento(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                id_categoria=resultado["id_categoria"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"]
            ) for resultado in resultados]

            return itens, total
    except Exception as e:
        print(f"Erro ao obter itens paginados: {e}")
        return [], 0

def buscar_itens_paginado(busca: str = "", tipo_item: str = "", status: str = "", categoria_id: str = "", pagina: int = 1, tamanho_pagina: int = 10) -> tuple[List[Item], int]:
    """Busca itens paginados com filtros e retorna lista de itens e total"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Construir consulta baseada nos filtros
            condicoes = []
            parametros = []
            parametros_count = []

            if busca:
                condicoes.append("(nome LIKE ? OR descricao LIKE ? OR observacoes LIKE ?)")
                busca_param = f"%{busca}%"
                parametros.extend([busca_param, busca_param, busca_param])
                parametros_count.extend([busca_param, busca_param, busca_param])

            if tipo_item:
                condicoes.append("tipo = ?")
                parametros.append(tipo_item)
                parametros_count.append(tipo_item)

            if status == "ativo":
                condicoes.append("ativo = 1")
            elif status == "inativo":
                condicoes.append("ativo = 0")

            if categoria_id:
                try:
                    categoria_id_int = int(categoria_id)
                    condicoes.append("id_categoria = ?")
                    parametros.append(categoria_id_int)
                    parametros_count.append(categoria_id_int)
                except ValueError:
                    pass

            where_clause = ""
            if condicoes:
                where_clause = "WHERE " + " AND ".join(condicoes)

            # Contar total
            sql_count = f"SELECT COUNT(*) as total FROM item {where_clause}"
            cursor.execute(sql_count, parametros_count)
            total = cursor.fetchone()["total"]

            # Buscar itens da página
            offset = (pagina - 1) * tamanho_pagina
            sql_select = f"SELECT * FROM item {where_clause} ORDER BY id DESC LIMIT ? OFFSET ?"
            parametros.extend([tamanho_pagina, offset])
            cursor.execute(sql_select, parametros)
            resultados = cursor.fetchall()

            itens = [Item(
                id=resultado["id"],
                id_fornecedor=resultado["id_fornecedor"],
                tipo=TipoFornecimento(resultado["tipo"]),
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                id_categoria=resultado["id_categoria"],
                observacoes=resultado["observacoes"],
                ativo=bool(resultado["ativo"]),
                data_cadastro=resultado["data_cadastro"]
            ) for resultado in resultados]

            return itens, total
    except Exception as e:
        print(f"Erro ao buscar itens paginados: {e}")
        return [], 0
