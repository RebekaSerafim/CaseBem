# Guia de Uso das Test Factories

## Visão Geral

O sistema de Test Factories implementado na Fase 4 fornece uma maneira limpa, flexível e manutenível de criar dados de teste. Este guia mostra como usar todas as funcionalidades disponíveis.

## Factories Disponíveis

### 1. UsuarioFactory

```python
# Uso básico
usuario = usuario_factory.criar(nome="João Silva", email="joao@teste.com")

# Shortcuts para tipos específicos
admin = usuario_factory.criar_admin()
noivo = usuario_factory.criar_noivo()
fornecedor = usuario_factory.criar_fornecedor_usuario()

# Criar lista de usuários variados
usuarios = usuario_factory.criar_lista(5)  # 5 usuários com tipos diferentes

# Criar lista com parâmetros base
noivos = usuario_factory.criar_lista(3, perfil=TipoUsuario.NOIVO)
```

### 2. FornecedorFactory

```python
# Fornecedor básico
fornecedor = fornecedor_factory.criar()

# Fornecedor customizado
fornecedor = fornecedor_factory.criar(
    nome_empresa="Empresa Teste",
    verificado=True
)

# Lista de fornecedores
fornecedores = fornecedor_factory.criar_lista(5)
```

### 3. CategoriaFactory

```python
# Categoria básica
categoria = categoria_factory.criar()

# Categoria específica
categoria = categoria_factory.criar(
    nome="Fotografia",
    tipo_fornecimento=TipoFornecimento.SERVICO
)
```

### 4. ItemFactory

```python
# Item básico
item = item_factory.criar()

# Item customizado
item = item_factory.criar(
    nome="Pacote Premium",
    preco=1500.0,
    id_fornecedor=1
)
```

## TestDataBuilder - Cenários Complexos

Para testes de integração que precisam de dados relacionados:

```python
def test_cenario_completo(self, test_db, test_data_builder):
    # Criar builder
    builder = test_data_builder()

    # Compor dados relacionados
    dados = builder\
        .com_usuarios(5)\
        .com_fornecedores(3)\
        .com_categorias(5)\
        .com_itens(10)\
        .construir()

    # Acessar os dados
    usuarios = dados['usuarios']
    fornecedores = dados['fornecedores']
    categorias = dados['categorias']
    itens = dados['itens']
```

## Test Helpers - Validações

### Funções de Validação

```python
from tests.test_helpers import (
    assert_usuario_valido,
    assert_fornecedor_valido,
    assert_categoria_valida,
    assert_item_valido
)

# Validar objetos individuais
assert_usuario_valido(usuario)
assert_fornecedor_valido(fornecedor)
```

### AssertHelper - Validações de Lista

```python
from tests.test_helpers import AssertHelper

# Verificar listas
AssertHelper.lista_nao_vazia(usuarios, "lista de usuários")
AssertHelper.emails_unicos(usuarios, "usuários")
AssertHelper.ids_unicos(items, "itens")
```

## Padrões de Teste Recomendados

### 1. Teste Simples com Factory

```python
def test_inserir_usuario(self, test_db, usuario_factory):
    # Arrange
    usuario_repo.criar_tabela_usuarios()
    usuario = usuario_factory.criar(email="teste@email.com")

    # Act
    id_inserido = usuario_repo.inserir_usuario(usuario)

    # Assert
    usuario_db = usuario_repo.obter_usuario_por_id(id_inserido)
    assert_usuario_valido(usuario_db)
    assert usuario_db.email == "teste@email.com"
```

### 2. Teste com Lista

```python
def test_listar_usuarios(self, test_db, usuario_factory):
    # Arrange
    usuario_repo.criar_tabela_usuarios()
    usuarios = usuario_factory.criar_lista(10)

    # Inserir todos
    for usuario in usuarios:
        usuario_repo.inserir_usuario(usuario)

    # Act
    resultado = usuario_repo.obter_usuarios_por_pagina(1, 20)

    # Assert
    assert len(resultado) == 10
    AssertHelper.emails_unicos(resultado, "usuários listados")
    for usuario in resultado:
        assert_usuario_valido(usuario)
```

### 3. Teste de Integração

```python
def test_cenario_completo(self, test_db, test_data_builder):
    # Arrange
    builder = test_data_builder()
    dados = builder.com_usuarios(5).com_fornecedores(3).construir()

    # Setup database
    usuario_repo.criar_tabela_usuarios()
    fornecedor_repo.criar_tabela_fornecedores()

    # Act - Inserir dados relacionados
    for usuario in dados['usuarios']:
        usuario_repo.inserir_usuario(usuario)

    for fornecedor in dados['fornecedores']:
        fornecedor_repo.inserir_fornecedor(fornecedor)

    # Assert - Verificar integridade
    todos_usuarios = usuario_repo.obter_usuarios_por_pagina(1, 10)
    todos_fornecedores = fornecedor_repo.obter_fornecedores_por_pagina(1, 10)

    assert len(todos_usuarios) == 5
    assert len(todos_fornecedores) == 3
```

## Migrations de Testes Existentes

### Antes (fixtures hardcoded)

```python
def test_inserir_usuario(self, test_db, usuario_exemplo):
    usuario_repo.criar_tabela_usuarios()
    id_inserido = usuario_repo.inserir_usuario(usuario_exemplo)

    usuario_db = usuario_repo.obter_usuario_por_id(id_inserido)
    assert usuario_db.nome == "Usuário Teste"  # hardcoded
    assert usuario_db.email == "usuario@email.com"  # hardcoded
```

### Depois (com factories)

```python
def test_inserir_usuario(self, test_db, usuario_factory):
    usuario_repo.criar_tabela_usuarios()
    usuario = usuario_factory.criar(nome="João", email="joao@teste.com")
    id_inserido = usuario_repo.inserir_usuario(usuario)

    usuario_db = usuario_repo.obter_usuario_por_id(id_inserido)
    assert usuario_db.nome == "João"  # flexível
    assert usuario_db.email == "joao@teste.com"  # flexível
    assert_usuario_valido(usuario_db)  # helper de validação
```

## Vantagens do Novo Sistema

### ✅ Flexibilidade
- Dados customizáveis por teste
- Não mais hardcoded values

### ✅ Manutenibilidade
- Mudanças no modelo refletidas automaticamente
- Factory centralizada

### ✅ Realismo
- Faker gera dados realistas
- Testes mais próximos da realidade

### ✅ Reutilização
- Factories utilizadas em múltiplos testes
- TestDataBuilder para cenários complexos

### ✅ Legibilidade
- Test helpers tornam assertions mais claras
- Código de teste mais expressivo

## Fixtures de Compatibilidade

O sistema mantém compatibilidade com testes existentes através de fixtures em `conftest.py`:

```python
# Estas fixtures ainda funcionam (mas use factories para novos testes)
usuario_exemplo
lista_usuarios_exemplo
fornecedor_exemplo
# etc...
```

## Próximos Passos

1. ✅ Use factories em todos os novos testes
2. 🔄 Migre testes existentes gradualmente
3. 📖 Consulte este guia quando em dúvida
4. 🧹 Remova fixtures antigas quando não mais necessárias