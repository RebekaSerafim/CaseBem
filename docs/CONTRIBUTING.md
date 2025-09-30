# Guia de Contribuição - CaseBem

## Como Contribuir

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Padrões de Código

- Siga o [STYLE_GUIDE.md](./STYLE_GUIDE.md)
- Use type hints em todas as funções
- Escreva docstrings para funções públicas
- Mantenha linhas com máximo 100 caracteres

## Testes

- Todos os PRs devem incluir testes
- Execute `pytest tests/` antes de commitar
- Mantenha cobertura de testes acima de 80%
- Use factories para criar dados de teste

## Commit Messages

Formato: `<tipo>: <descrição>`

Tipos:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `docs`: Documentação
- `style`: Formatação de código

Exemplos:
```
feat: adiciona endpoint de busca de usuários
fix: corrige validação de CPF em usuario_dto
refactor: reorganiza estrutura de diretórios
test: adiciona testes para categoria_service
docs: atualiza documentação da API
```

## Estrutura de PR

1. **Título**: Descrição clara e concisa
2. **Descrição**: Explique o que foi feito e por quê
3. **Testes**: Liste os testes adicionados/modificados
4. **Checklist**:
   - [ ] Código segue o style guide
   - [ ] Testes passando
   - [ ] Documentação atualizada
   - [ ] Sem conflitos com main

## Processo de Review

- Pelo menos 1 aprovação necessária
- Todos os testes devem passar
- Code review focado em:
  - Lógica de negócio
  - Segurança
  - Performance
  - Legibilidade

## Adicionando Nova Entidade

1. Criar model em `core/models/`
2. Criar SQL em `core/sql/`
3. Criar repository em `core/repositories/`
4. Criar service em `core/services/`
5. Criar DTOs em `api/dtos/`
6. Criar routes em `routes/`
7. Adicionar testes
8. Atualizar documentação

## Dúvidas?

Abra uma issue ou entre em contato com os maintainers.

---

**Versão**: 1.0 | **Última atualização**: Setembro 2025
