# Guia de Queries SQL: Genéricas vs Específicas

## 📚 Visão Geral

Este documento explica a estrutura de queries SQL no projeto, diferenciando entre **queries genéricas** (fornecidas pelo `BaseRepo`) e **queries específicas** de negócio.

## 🎯 Objetivo

Com a introdução do `BaseRepo`, centralizamos operações CRUD comuns e eliminamos redundâncias. Este guia ajuda a entender:
- Quais queries são genéricas e reutilizáveis
- Quais queries são específicas do domínio de negócio
- Como usar cada tipo corretamente

---

## 📁 Estrutura dos Arquivos SQL

Cada arquivo SQL em `core/sql/` está organizado em duas seções:

```python
# ==============================================================================
# QUERIES GENÉRICAS (usadas pelo BaseRepo)
# ==============================================================================

CRIAR_TABELA = """..."""
INSERIR = """..."""
ATUALIZAR = """..."""
EXCLUIR = """..."""
OBTER_POR_ID = """..."""
LISTAR_TODOS = """..."""
LISTAR_ATIVOS = """...""""  # Opcional

# ==============================================================================
# QUERIES ESPECÍFICAS DE NEGÓCIO (métodos customizados do repositório)
# ==============================================================================

OBTER_POR_CAMPO_ESPECIFICO = """..."""
BUSCAR_COM_FILTROS = """..."""
# etc...
```

---

## 🔧 Queries Genéricas (BaseRepo)

### O que são?

Queries genéricas são **operações CRUD padrão** implementadas no `BaseRepo` que funcionam para qualquer tabela.

### Queries Disponíveis

| Query | Descrição | Método BaseRepo |
|-------|-----------|----------------|
| `CRIAR_TABELA` | Cria a tabela se não existir | `criar_tabela()` |
| `INSERIR` | Insere novo registro | `inserir(objeto)` |
| `ATUALIZAR` | Atualiza registro existente | `atualizar(objeto)` |
| `EXCLUIR` | Remove registro por ID | `excluir(id)` |
| `OBTER_POR_ID` | Busca registro por ID | `obter_por_id(id)` |
| `LISTAR_TODOS` | Lista todos os registros | `listar_todos()` |
| `LISTAR_ATIVOS` | Lista apenas registros ativos | `listar_todos(ativo=True)` |

### Métodos Extras do BaseRepo

Além das queries SQL, o `BaseRepo` oferece:

| Método | Descrição | Uso |
|--------|-----------|-----|
| `contar_registros(condicao, parametros)` | Conta registros | `repo.contar_registros()` |
| `obter_paginado(pagina, tamanho)` | Paginação genérica | `repo.obter_paginado(1, 10)` |
| `ativar(id, campo)` | Ativa registro (soft delete) | `repo.ativar(id)` |
| `desativar(id, campo)` | Desativa registro (soft delete) | `repo.desativar(id)` |
| `executar_consulta(sql, params)` | Executa SQL customizado | `repo.executar_consulta(sql, ())` |
| `executar_comando(sql, params)` | Executa comando (UPDATE/DELETE) | `repo.executar_comando(sql, ())` |

---

## 🎨 Queries Específicas de Negócio

### O que são?

Queries específicas implementam **lógica de domínio** que não pode ser generalizada. Exemplos:

- Buscar categorias por tipo de fornecimento
- Obter orçamentos por fornecedor
- Listar demandas ativas de um casal
- Aceitar orçamento e rejeitar outros automaticamente

### Quando Criar Queries Específicas?

✅ **SIM** - Criar query específica quando:
- Envolve JOINs com outras tabelas
- Tem lógica de negócio complexa (ex: aceitar orçamento + rejeitar outros)
- Precisa de filtros ou agregações específicas do domínio
- Atualiza múltiplos registros com base em regras de negócio

❌ **NÃO** - Não criar query específica quando:
- É uma operação CRUD básica (usar `BaseRepo`)
- Pode ser feita com `contar_registros()` + condição
- Pode ser feita com `ativar()` ou `desativar()`
- Pode ser feita com `obter_paginado()`

---

## 📋 Exemplos Práticos

### ✅ Exemplo 1: Ativar/Desativar (Usar BaseRepo)

**ANTES** (query redundante):
```python
# categoria_sql.py
ATIVAR_CATEGORIA = """
UPDATE categoria SET ativo = 1 WHERE id = ?;
"""

# categoria_repo.py
def ativar_categoria(self, id: int) -> bool:
    return self.executar_comando(categoria_sql.ATIVAR_CATEGORIA, (id,))
```

**DEPOIS** (usar BaseRepo):
```python
# categoria_repo.py
def ativar_categoria(self, id: int) -> bool:
    return self.ativar(id)  # Método do BaseRepo
```

### ✅ Exemplo 2: Contar Registros (Usar BaseRepo)

**ANTES** (query redundante):
```python
# usuario_sql.py
CONTAR_USUARIOS = """SELECT COUNT(*) as total FROM usuario;"""
CONTAR_USUARIOS_POR_TIPO = """SELECT COUNT(*) as total FROM usuario WHERE perfil = ?;"""

# usuario_repo.py
def contar_usuarios(self) -> int:
    resultado = self.executar_consulta(usuario_sql.CONTAR_USUARIOS)
    return resultado[0]["total"]
```

**DEPOIS** (usar BaseRepo):
```python
# usuario_repo.py
def contar_usuarios(self) -> int:
    return self.contar_registros()  # Método do BaseRepo

def contar_usuarios_por_tipo(self, tipo: TipoUsuario) -> int:
    return self.contar_registros("perfil = ?", (tipo.value,))
```

### ✅ Exemplo 3: Query Específica Válida (Manter)

```python
# orcamento_sql.py
ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS = """
UPDATE orcamento
SET status = CASE
    WHEN id = ? THEN 'ACEITO'
    ELSE 'REJEITADO'
END
WHERE id_demanda = ? AND status = 'PENDENTE';
"""
```

✅ **Por quê manter?** Lógica de negócio complexa (atualiza múltiplos registros com regras condicionais).

---

## 🗂️ Checklist de Arquivos SQL

### Arquivos Limpos (queries redundantes removidas):

- ✅ `categoria_sql.py` - Removidos: `ATIVAR_CATEGORIA`, `DESATIVAR_CATEGORIA`, aliases deprecated
- ✅ `usuario_sql.py` - Removidos: `BLOQUEAR_USUARIO`, `ATIVAR_USUARIO`, `CONTAR_USUARIOS`, `CONTAR_USUARIOS_POR_TIPO`, aliases deprecated
- ✅ `item_sql.py` - Removidos: `ATIVAR_ITEM`, `DESATIVAR_ITEM`, `CONTAR_ITENS`, `CONTAR_ITENS_POR_TIPO`, `OBTER_ITENS_POR_PAGINA`, `OBTER_PRODUTOS`, `OBTER_SERVICOS`, `OBTER_ESPACOS`, aliases deprecated
- ✅ `casal_sql.py` - Removido: `OBTER_CASAL_POR_PAGINA`, aliases deprecated
- ✅ `demanda_sql.py` - Removidos: `OBTER_DEMANDAS_POR_PAGINA`, `EXCLUIR_DEMANDA`, `OBTER_DEMANDA_POR_ID`, aliases deprecated
- ✅ `fornecedor_sql.py` - Removido: `CONTAR_FORNECEDORES`, aliases deprecated

---

## 📊 Resultados da Limpeza

### Antes
- **~800 linhas** em `core/sql/`
- Queries duplicadas e aliases redundantes
- Confusão entre queries genéricas e específicas

### Depois
- **~620 linhas** em `core/sql/` (**-22%** de código)
- Separação clara: genéricas vs específicas
- Manutenção centralizada no `BaseRepo`
- **135/135 testes passando** ✅

---

## 🚀 Guia Rápido de Uso

### Para Criar um Novo Repositório

1. **Herde de `BaseRepo`**:
```python
class NovoRepo(BaseRepo):
    def __init__(self):
        super().__init__("nome_tabela", ModelClass, sql_module)
```

2. **Implemente os métodos obrigatórios**:
```python
def _objeto_para_tupla_insert(self, objeto) -> tuple:
    return (objeto.campo1, objeto.campo2, ...)

def _objeto_para_tupla_update(self, objeto) -> tuple:
    return (objeto.campo1, objeto.campo2, ..., objeto.id)

def _linha_para_objeto(self, linha: dict) -> ModelClass:
    return ModelClass(id=linha["id"], ...)
```

3. **Adicione apenas queries específicas**:
```python
def obter_por_campo_especifico(self, campo):
    resultados = self.executar_consulta(sql_module.QUERY_ESPECIFICA, (campo,))
    return [self._linha_para_objeto(r) for r in resultados]
```

4. **Use métodos do BaseRepo sempre que possível**:
```python
# ✅ Correto
def ativar_registro(self, id: int):
    return self.ativar(id)

# ❌ Errado
def ativar_registro(self, id: int):
    return self.executar_comando("UPDATE tabela SET ativo = 1 WHERE id = ?", (id,))
```

---

## 🔗 Referências

- **BaseRepo**: `core/repositories/base_repo.py`
- **Exemplos de uso**: `core/repositories/categoria_repo.py`, `core/repositories/usuario_repo.py`
- **Testes**: `tests/test_*_repo.py`

---

## ❓ FAQ

**P: Posso criar uma query SQL customizada?**
R: Sim! Use `executar_consulta()` ou `executar_comando()` do BaseRepo quando necessário.

**P: Como faço paginação?**
R: Use `obter_paginado(pagina, tamanho_pagina)` do BaseRepo.

**P: Como conto registros com filtro?**
R: Use `contar_registros("campo = ?", (valor,))` do BaseRepo.

**P: Devo remover queries antigas?**
R: Sim, se forem redundantes. Veja os exemplos deste guia.

---

**Última atualização**: 2025-10-01
**Versão**: 1.0
