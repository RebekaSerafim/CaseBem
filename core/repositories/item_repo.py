from typing import Optional, List, Dict, Any
from util.base_repo import BaseRepo
from sql import item_sql
from sql.item_sql import CONTAR_ITENS_PUBLICOS_FILTRADOS, OBTER_ITENS_PUBLICOS_FILTRADOS
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

    def obter_itens_publicos(self, tipo: Optional[str] = None, busca: Optional[str] = None,
                           categoria: Optional[int] = None, pagina: int = 1, tamanho_pagina: int = 12) -> tuple[List[dict], int]:
        """Obtém itens públicos com filtros opcionais e paginação"""
        try:
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
            total_resultado = self.executar_query(CONTAR_ITENS_PUBLICOS_FILTRADOS, (
                tipo_param, tipo_param,
                busca, busca_like, busca_like, busca_like,
                categoria, categoria
            ))
            total = total_resultado[0]["total"] if total_resultado else 0

            # Buscar itens da página
            resultados = self.executar_query(OBTER_ITENS_PUBLICOS_FILTRADOS, (
                tipo_param, tipo_param,
                busca, busca_like, busca_like, busca_like,
                categoria, categoria,
                tamanho_pagina, offset
            ))

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

    def obter_item_publico_por_id(self, id_item: int) -> Optional[dict]:
        """Obtém um item específico com informações do fornecedor para exibição pública"""
        try:
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
            resultados = self.executar_query(query, (id_item,))

            if resultados:
                resultado = resultados[0]
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

    def ativar_item(self, id_item: int, id_fornecedor: int) -> bool:
        """Ativa um item"""
        return self.executar_comando("UPDATE item SET ativo = 1 WHERE id = ? AND id_fornecedor = ?", (id_item, id_fornecedor))

    def desativar_item(self, id_item: int, id_fornecedor: int) -> bool:
        """Desativa um item (soft delete)"""
        return self.executar_comando("UPDATE item SET ativo = 0 WHERE id = ? AND id_fornecedor = ?", (id_item, id_fornecedor))

    def obter_itens_paginado_repo(self, pagina: int, tamanho_pagina: int) -> tuple[List[Item], int]:
        """Obtém itens paginados com total"""
        try:
            total = self.contar_itens()
            itens = self.obter_itens_por_pagina(pagina, tamanho_pagina)
            return itens, total
        except Exception as e:
            print(f"Erro ao obter itens paginados: {e}")
            return [], 0

    def buscar_itens_paginado_repo(self, busca: str = "", tipo_item: str = "", status: str = "", categoria_id: str = "", pagina: int = 1, tamanho_pagina: int = 10) -> tuple[List[Item], int]:
        """Busca itens paginados com filtros"""
        try:
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
            total_resultado = self.executar_query(sql_count, parametros_count)
            total = total_resultado[0]["total"] if total_resultado else 0

            # Buscar itens da página
            offset = (pagina - 1) * tamanho_pagina
            sql_select = f"SELECT * FROM item {where_clause} ORDER BY id DESC LIMIT ? OFFSET ?"
            parametros.extend([tamanho_pagina, offset])
            resultados = self.executar_query(sql_select, parametros)

            itens = [self._linha_para_objeto(resultado) for resultado in resultados]
            return itens, total
        except Exception as e:
            print(f"Erro ao buscar itens paginados: {e}")
            return [], 0

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
    return item_repo.obter_itens_por_pagina(numero_pagina, tamanho_pagina)

def buscar_itens(termo_busca: str, numero_pagina: int = 1, tamanho_pagina: int = 20) -> List[Item]:
    return item_repo.buscar_itens(termo_busca, numero_pagina, tamanho_pagina)

def obter_produtos() -> List[Item]:
    return item_repo.obter_produtos()

def obter_servicos() -> List[Item]:
    return item_repo.obter_servicos()

def obter_espacos() -> List[Item]:
    return item_repo.obter_espacos()

def contar_itens_por_fornecedor(id_fornecedor: int) -> int:
    return item_repo.contar_itens_por_fornecedor(id_fornecedor)

def obter_estatisticas_itens() -> List[Dict[str, Any]]:
    return item_repo.obter_estatisticas_itens()

def obter_itens_publicos(tipo: Optional[str] = None, busca: Optional[str] = None,
                        categoria: Optional[int] = None, pagina: int = 1, tamanho_pagina: int = 12) -> tuple[List[dict], int]:
    return item_repo.obter_itens_publicos(tipo, busca, categoria, pagina, tamanho_pagina)

def obter_item_publico_por_id(id_item: int) -> Optional[dict]:
    return item_repo.obter_item_publico_por_id(id_item)

def ativar_item(id_item: int, id_fornecedor: int) -> bool:
    return item_repo.ativar_item(id_item, id_fornecedor)

def desativar_item(id_item: int, id_fornecedor: int) -> bool:
    return item_repo.desativar_item(id_item, id_fornecedor)
def contar_itens() -> int:
    return item_repo.contar_itens()

def contar_itens_por_tipo(tipo: TipoFornecimento) -> int:
    return item_repo.contar_itens_por_tipo(tipo)

def obter_itens_paginado(pagina: int, tamanho_pagina: int) -> tuple[List[Item], int]:
    """Obtém itens paginados e retorna lista de itens e total"""
    return item_repo.obter_itens_paginado_repo(pagina, tamanho_pagina)

def buscar_itens_paginado(busca: str = "", tipo_item: str = "", status: str = "", categoria_id: str = "", pagina: int = 1, tamanho_pagina: int = 10) -> tuple[List[Item], int]:
    """Busca itens paginados com filtros e retorna lista de itens e total"""
    return item_repo.buscar_itens_paginado_repo(busca, tipo_item, status, categoria_id, pagina, tamanho_pagina)
