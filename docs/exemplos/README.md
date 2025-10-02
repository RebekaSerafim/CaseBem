# Exemplos e Código de Referência

Este diretório contém código de exemplo e referências que **não estão ativas no sistema**, mas são mantidos para consulta futura.

## 📁 Conteúdo

### `security_middleware_exemplo.py`

**Status**: ❌ Não usado no projeto

**O que é**: Middleware avançado de segurança com funcionalidades como:
- Bloqueio de IP após tentativas falhadas de login
- Controle de timeout de sessão
- Limite de sessões simultâneas por usuário
- Detecção de mudanças suspeitas de IP
- Logs detalhados de eventos de segurança

**Por que está aqui**:
- Nunca foi ativado no sistema
- Implementa funcionalidades que podem ser úteis no futuro
- Serve como referência para implementação de segurança

**Como usar** (se precisar no futuro):
1. Mover para `infrastructure/security/`
2. Refatorar para usar banco de dados (SQLite) ao invés de memória
3. Registrar em `main.py`:
   ```python
   from infrastructure.security.security_middleware import security_middleware
   app.add_middleware(security_middleware())
   ```

**Limitações do código atual**:
- ❌ Usa dicionários em memória (dados perdidos ao reiniciar)
- ❌ Não persiste no banco de dados
- ❌ Complexidade desnecessária para o projeto atual
- ❌ Precisa de Redis ou banco para produção

**Recomendação**: Se precisar de segurança adicional, reimplementar de forma mais simples usando o banco de dados SQLite do projeto.

---

## 📝 Histórico

- **2025-10-01**: Movido `security_middleware.py` de `infrastructure/security/` para cá (código não usado)
- **2025-10-01**: Removido `middleware/flash_middleware.py` completamente (redundante)
