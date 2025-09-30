# Guia de Estilo - CaseBem

## Princípios Gerais

1. **Clareza sobre Brevidade**: Código claro é melhor que código curto
2. **Consistência**: Siga os padrões estabelecidos  
3. **Simplicidade**: KISS (Keep It Simple, Stupid)
4. **DRY**: Don't Repeat Yourself
5. **Type Safety**: Use type hints em tudo

## Nomenclatura

- **Arquivos**: snake_case (usuario_service.py)
- **Classes**: PascalCase (UsuarioService)
- **Funções**: snake_case (criar_usuario)
- **Variáveis**: snake_case (id_usuario)
- **Constantes**: UPPER_SNAKE_CASE (TAMANHO_PAGINA)

## Type Hints Obrigatórios

```python
def criar_usuario(nome: str, email: str) -> int:
    pass

def buscar_usuario(id: int) -> Optional[Usuario]:
    pass
```

## Docstrings (Google Style)

```python
def criar_usuario(dados: dict) -> int:
    """
    Cria um novo usuário no sistema.

    Args:
        dados: Dicionário com dados do usuário

    Returns:
        ID do usuário criado

    Raises:
        RegraDeNegocioError: Se email já existe
    """
```

## Organização de Imports

1. Bibliotecas padrão Python
2. Bibliotecas de terceiros
3. Imports do projeto (core/)
4. Imports do projeto (util/)

## Tratamento de Exceções

- Seja específico nas exceções
- Nunca use `except Exception` sem reraiser
- Use exceções customizadas (RegraDeNegocioError, etc)

## Logging

```python
logger.info(f"Usuário criado: {id}", extra={'nome': nome})
```

---

**Versão**: 1.0 | **Última atualização**: Setembro 2025
