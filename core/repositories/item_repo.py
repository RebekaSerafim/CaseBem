from typing import Optional, List, Dict, Any
from core.repositories.base_repo import BaseRepo
from infrastructure.logging import logger
from core.sql import item_sql
from core.sql.item_sql import (
    CONTAR_ITENS_PUBLICOS_FILTRADOS,
    OBTER_ITENS_PUBLICOS_FILTRADOS,
)
from core.models.item_model import Item
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.repositories.categoria_repo import categoria_repo


def validar_categoria_para_tipo(tipo: TipoFornecimento, id_categoria: int) -> bool:
    """Valida se uma categoria pertence a um tipo específico"""
    categoria = categoria_repo.obter_por_id(id_categoria)
    if not categoria:
        return False
    return categoria.tipo_fornecimento == tipo  # type: ignore[no-any-return]


class ItemRepo(BaseRepo):
    """Repositório para operações com itens"""

    def __init__(self):
        super().__init__("item", Item, item_sql)

    def inserir(self, item: Item) -> Optional[int]:
        """Insere um novo item com validação de categoria (override do BaseRepo)"""
        # Validar se a categoria pertence ao tipo do item
        if not validar_categoria_para_tipo(item.tipo, item.id_categoria):
            raise ValueError(
                f"Categoria {item.id_categoria} não pertence ao tipo {item.tipo.value}"
            )

        # Chama o método base
        return super().inserir(item)  # type: ignore[no-any-return]

    def atualizar(self, item: Item) -> bool:
        """Atualiza um item com validação de categoria (override do BaseRepo)"""
        # Validar se a categoria pertence ao tipo do item
        if not validar_categoria_para_tipo(item.tipo, item.id_categoria):
            raise ValueError(
                f"Categoria {item.id_categoria} não pertence ao tipo {item.tipo.value}"
            )

        # Chama o método base
        return super().atualizar(item)  # type: ignore[no-any-return]

    def excluir_item_fornecedor(self, id_item: int, id_fornecedor: int) -> bool:
        """Exclui um item (apenas o próprio fornecedor pode excluir)"""
        return self.executar_comando(item_sql.EXCLUIR_ITEM, (id_item, id_fornecedor))  # type: ignore[no-any-return]

    def _objeto_para_tupla_insert(self, item: Item) -> tuple:
        """Prepara dados do item para inserção"""
        return (
            item.id_fornecedor,
            item.tipo.value,
            item.nome,
            item.descricao,
            float(item.preco),  # Converter Decimal para float (SQLite não suporta Decimal)
            item.id_categoria,
            item.observacoes,
            item.ativo,
        )

    def _objeto_para_tupla_update(self, item: Item) -> tuple:
        """Prepara dados do item para atualização (inclui id_fornecedor para validação)"""
        return (
            item.tipo.value,
            item.nome,
            item.descricao,
            float(item.preco),  # Converter Decimal para float (SQLite não suporta Decimal)
            item.id_categoria,
            item.observacoes,
            item.ativo,
            item.id,
            item.id_fornecedor,
        )

    def _linha_para_objeto(self, linha: Dict[str, Any]) -> Item:
        """Converte linha do banco em objeto Item"""
        return Item(
            id=int(self._safe_get(linha, "id", 0)),
            id_fornecedor=int(self._safe_get(linha, "id_fornecedor", 0)),
            tipo=TipoFornecimento(self._safe_get(linha, "tipo", "")),
            nome=str(self._safe_get(linha, "nome", "")),
            descricao=str(self._safe_get(linha, "descricao", "")),
            preco=self._safe_get(linha, "preco", 0),
            id_categoria=int(self._safe_get(linha, "id_categoria", 0)),
            observacoes=self._safe_get(linha, "observacoes"),
            ativo=bool(self._safe_get(linha, "ativo", True)),
            data_cadastro=self._safe_get(linha, "data_cadastro"),
        )

    def obter_itens_por_fornecedor(self, id_fornecedor: int) -> List[Item]:
        """Obtém todos os itens ativos de um fornecedor"""
        return [
            self._linha_para_objeto(row)
            for row in self.executar_consulta(
                item_sql.OBTER_ITENS_POR_FORNECEDOR, (id_fornecedor,)
            )
        ]

    def obter_itens_por_tipo(self, tipo: TipoFornecimento) -> List[Item]:
        """Obtém todos os itens ativos de um tipo específico"""
        return [
            self._linha_para_objeto(row)
            for row in self.executar_consulta(
                item_sql.OBTER_ITENS_POR_TIPO, (tipo.value,)
            )
        ]

    def obter_itens_por_pagina(
        self, numero_pagina: int, tamanho_pagina: int
    ) -> List[Item]:
        """Obtém itens com paginação"""
        itens, _ = self.obter_paginado(numero_pagina, tamanho_pagina)
        return itens  # type: ignore[no-any-return]

    def buscar_itens(
        self, termo_busca: str, numero_pagina: int = 1, tamanho_pagina: int = 20
    ) -> List[Item]:
        """Busca itens por termo"""
        busca = f"%{termo_busca}%"
        return [
            self._linha_para_objeto(row)
            for row in self.executar_consulta(
                item_sql.BUSCAR_ITENS,
                (
                    busca,
                    busca,
                    busca,
                    tamanho_pagina,
                    (numero_pagina - 1) * tamanho_pagina,
                ),
            )
        ]

    def obter_produtos(self) -> List[Item]:
        """Obtém todos os produtos ativos"""
        return self.obter_itens_por_tipo(TipoFornecimento.PRODUTO)

    def obter_servicos(self) -> List[Item]:
        """Obtém todos os serviços ativos"""
        return self.obter_itens_por_tipo(TipoFornecimento.SERVICO)

    def obter_espacos(self) -> List[Item]:
        """Obtém todos os espaços ativos"""
        return self.obter_itens_por_tipo(TipoFornecimento.ESPACO)

    def contar_por_fornecedor(self, id_fornecedor: int) -> int:
        """Conta itens ativos de um fornecedor"""
        return self.contar_registros(  # type: ignore[no-any-return]
            "id_fornecedor = ? AND ativo = 1", (id_fornecedor,)
        )

    def obter_estatisticas_itens(self) -> List[Dict[str, Any]]:
        """Obtém estatísticas de itens por tipo"""
        return self.executar_consulta(item_sql.OBTER_ESTATISTICAS_ITENS)  # type: ignore[no-any-return]

    def contar_itens(self) -> int:
        """Conta total de itens"""
        return self.contar_registros()  # type: ignore[no-any-return]

    def contar_itens_por_tipo(self, tipo: TipoFornecimento) -> int:
        """Conta itens de um tipo específico"""
        return self.contar_registros("tipo = ?", (tipo.value,))  # type: ignore[no-any-return]

    def obter_itens_publicos(
        self,
        tipo: Optional[str] = None,
        busca: Optional[str] = None,
        categoria: Optional[int] = None,
        pagina: int = 1,
        tamanho_pagina: int = 12,
    ) -> tuple[List[dict], int]:
        """Obtém itens públicos com filtros opcionais e paginação"""
        offset = (pagina - 1) * tamanho_pagina

        # Mapear tipos de URL para tipos do banco
        tipo_map = {"produto": "PRODUTO", "servico": "SERVIÇO", "espaco": "ESPAÇO"}
        tipo_param = tipo_map.get(tipo) if tipo else None
        # Converter busca vazia para None para funcionar corretamente com SQL
        busca = busca if busca and busca.strip() else None
        busca_like = f"%{busca}%" if busca else None

        # Contar total de itens
        total_resultado = self.executar_consulta(
            CONTAR_ITENS_PUBLICOS_FILTRADOS,
            (
                tipo_param,
                tipo_param,
                busca,
                busca_like,
                busca_like,
                busca_like,
                categoria,
                categoria,
            ),
        )
        total = total_resultado[0]["total"] if total_resultado else 0

        # Buscar itens da página
        resultados = self.executar_consulta(
            OBTER_ITENS_PUBLICOS_FILTRADOS,
            (
                tipo_param,
                tipo_param,
                busca,
                busca_like,
                busca_like,
                busca_like,
                categoria,
                categoria,
                tamanho_pagina,
                offset,
            ),
        )

        itens = [
            dict(resultado, ativo=bool(resultado["ativo"])) for resultado in resultados
        ]
        return itens, total

    def obter_item_publico_por_id(self, id_item: int) -> Optional[dict]:
        """Obtém um item específico com informações do fornecedor para exibição pública"""
        resultados = self.executar_consulta(
            item_sql.OBTER_ITEM_PUBLICO_POR_ID, (id_item,)
        )

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
                "categoria": (
                    {
                        "nome": resultado["categoria_nome"],
                        "descricao": resultado["categoria_descricao"],
                    }
                    if resultado["categoria_nome"]
                    else None
                ),
                "fornecedor": {
                    "nome": resultado["fornecedor_nome"],
                    "email": resultado["fornecedor_email"],
                    "telefone": resultado["fornecedor_telefone"],
                    "empresa": resultado["fornecedor_empresa"],
                    "descricao": resultado["fornecedor_descricao"],
                },
            }
        return None

    def ativar_item(self, id_item: int, id_fornecedor: int) -> bool:
        """Ativa um item (validando fornecedor)"""
        sql = "UPDATE item SET ativo = 1 WHERE id = ? AND id_fornecedor = ?"
        return self.executar_comando(sql, (id_item, id_fornecedor))  # type: ignore[no-any-return]

    def desativar_item(self, id_item: int, id_fornecedor: int) -> bool:
        """Desativa um item (soft delete) (validando fornecedor)"""
        sql = "UPDATE item SET ativo = 0 WHERE id = ? AND id_fornecedor = ?"
        return self.executar_comando(sql, (id_item, id_fornecedor))  # type: ignore[no-any-return]

    def ativar_item_admin(self, id_item: int) -> bool:
        """Ativa um item sem validar fornecedor (uso exclusivo do admin)"""
        sql = "UPDATE item SET ativo = 1 WHERE id = ?"
        return self.executar_comando(sql, (id_item,))  # type: ignore[no-any-return]

    def desativar_item_admin(self, id_item: int) -> bool:
        """Desativa um item sem validar fornecedor (uso exclusivo do admin)"""
        sql = "UPDATE item SET ativo = 0 WHERE id = ?"
        return self.executar_comando(sql, (id_item,))  # type: ignore[no-any-return]

    def obter_paginado_itens(
        self, pagina: int, tamanho_pagina: int
    ) -> tuple[List[Item], int]:
        """Obtém itens paginados com total"""
        return self.obter_paginado(pagina, tamanho_pagina)  # type: ignore[no-any-return]

    def buscar_paginado(
        self,
        busca: str = "",
        tipo_item: str = "",
        status: str = "",
        categoria_id: str = "",
        pagina: int = 1,
        tamanho_pagina: int = 10,
    ) -> tuple[List[Item], int]:
        """Busca itens paginados com filtros"""
        offset = (pagina - 1) * tamanho_pagina
        busca_param = f"%{busca}%" if busca else ""

        # Converter categoria_id para int ou "" se inválido
        categoria_id_param = ""
        if categoria_id:
            try:
                categoria_id_param = str(int(categoria_id))
            except ValueError:
                categoria_id_param = ""

        # Parâmetros: busca, busca_like*3, tipo*2, status*3, categoria*2, LIMIT, OFFSET
        parametros_count = [
            busca,
            busca_param,
            busca_param,
            busca_param,
            tipo_item,
            tipo_item,
            status,
            status,
            status,
            categoria_id_param,
            categoria_id_param,
        ]
        parametros_select = parametros_count + [tamanho_pagina, offset]

        # Contar total usando query parametrizada
        total_resultado = self.executar_consulta(
            item_sql.CONTAR_ITENS_FILTRADOS, parametros_count
        )
        total = total_resultado[0]["total"] if total_resultado else 0

        # Buscar itens usando query parametrizada
        resultados = self.executar_consulta(
            item_sql.BUSCAR_ITENS_FILTRADOS, parametros_select
        )
        itens = [self._linha_para_objeto(resultado) for resultado in resultados]

        return itens, total

    def obter_itens_ativos_por_categoria(self, id_categoria: int) -> List[Dict[str, Any]]:
        """Busca itens ativos de uma categoria específica (para AJAX/API)"""
        resultados = self.executar_consulta(
            item_sql.OBTER_ITENS_ATIVOS_POR_CATEGORIA, (id_categoria,)
        )
        return [
            {
                "id": r["id"],
                "nome": r["nome"],
                "descricao": r["descricao"],
                "preco": float(r["preco"]),
                "id_fornecedor": r["id_fornecedor"],
                "tipo": r["tipo"]
            }
            for r in resultados
        ]

    def obter_categorias_do_fornecedor(self, id_fornecedor: int) -> List[int]:
        """Retorna lista de IDs de categorias que o fornecedor oferece itens ativos"""
        resultados = self.executar_consulta(
            item_sql.OBTER_CATEGORIAS_DO_FORNECEDOR, (id_fornecedor,)
        )
        return [r["id_categoria"] for r in resultados]


# Instância singleton do repositório
item_repo = ItemRepo()
