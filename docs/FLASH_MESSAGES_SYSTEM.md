# Sistema de Flash Messages - Case Bem

## Visão Geral

O sistema de flash messages permite exibir mensagens através de redirects usando sessões do FastAPI. As mensagens são automaticamente convertidas em toasts flutuantes usando o sistema de toast existente.

## Arquivos Implementados

### Novos Arquivos:
- `/util/flash_messages.py` - Utilitário principal de mensagens flash
- `/util/template_helpers.py` - Helper para incluir flash messages nos templates
- `/middleware/flash_middleware.py` - Middleware (opcional, para futuras extensões)

### Arquivos Modificados:
- `/templates/components/toast-handler.html` - Adicionado suporte a flash messages
- **Rotas atualizadas:**
  - `/routes/fornecedor_routes.py` - 5 rotas de operações com itens + orçamentos
  - `/routes/admin_routes.py` - Rotas de usuários e verificação de fornecedores
  - `/routes/noivo_routes.py` - Rotas de orçamentos (aceitar/rejeitar)
  - `/routes/public_routes.py` - Cadastros e login

## Como Usar

### 1. Nas Rotas (Backend)

```python
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso

# Antes do redirect
informar_sucesso(request, "Operação realizada com sucesso!")
return RedirectResponse("/destino", status_code=status.HTTP_303_SEE_OTHER)

# Exemplo específico
@router.post("/criar-item")
async def criar_item(request: Request, ...):
    # ... lógica da criação ...
    if item_criado:
        informar_sucesso(request, "Item criado com sucesso!")
        return RedirectResponse("/itens", status_code=status.HTTP_303_SEE_OTHER)
    else:
        informar_erro(request, "Erro ao criar item!")
        return RedirectResponse("/itens/novo", status_code=status.HTTP_303_SEE_OTHER)
```

### 2. Funções Disponíveis

```python
# Funções por tipo de mensagem (em português)
informar_sucesso(request, "Mensagem de sucesso")
informar_erro(request, "Mensagem de erro")
informar_aviso(request, "Mensagem de aviso")
informar_info(request, "Mensagem informativa")
informar_alerta(request, "Mensagem de alerta")

# Função genérica
flash(request, "Mensagem", "tipo")

# Funções utilitárias
get_flashed_messages(request)  # Recupera e remove mensagens
has_flashed_messages(request)  # Verifica se há mensagens
```

### 3. Helper de Template

Para templates que precisam de flash messages:

```python
from util.template_helpers import template_response_with_flash

# Substituir
return templates.TemplateResponse("template.html", context)

# Por
return template_response_with_flash(templates, "template.html", context)
```

## Funcionamento Técnico

### 1. Armazenamento na Sessão
```python
# As mensagens são armazenadas em request.session["flash_messages"]
{
    "flash_messages": [
        {"text": "Mensagem", "type": "success"},
        {"text": "Outra mensagem", "type": "error"}
    ]
}
```

### 2. Exibição Automática
```javascript
// No toast-handler.html
{% if flash_messages %}
{% for flash_message in flash_messages %}
window.showToast(`{{ flash_message.text|escapejs }}`, `{{ flash_message.type }}`);
{% endfor %}
{% endif %}
```

### 3. Auto-limpeza
- As mensagens são automaticamente removidas da sessão após serem recuperadas
- Evita re-exibição em reloads de página

## Mapeamento de Tipos

| Função | Tipo | Toast Exibido | Duração |
|--------|------|---------------|---------|
| `informar_sucesso()` | success | Verde ✓ | 5s |
| `informar_erro()` | danger | Vermelho ✕ | 7s |
| `informar_aviso()` | warning | Amarelo ⚠ | 6s |
| `informar_info()` | info | Azul ℹ | 5s |
| `informar_alerta()` | alert | Azul escuro ! | 6s |

## Rotas Atualizadas

### Fornecedor:
- ✅ Criar item → "Item criado com sucesso!"
- ✅ Atualizar item → "Item atualizado com sucesso!"
- ✅ Excluir item → "Item excluído com sucesso!"
- ✅ Ativar item → "Item ativado com sucesso!"
- ✅ Desativar item → "Item desativado com sucesso!"
- ✅ Criar orçamento → "Orçamento enviado com sucesso!"

### Admin:
- ✅ Bloquear usuário → "Usuário bloqueado com sucesso!"
- ✅ Ativar usuário → "Usuário ativado com sucesso!"
- ✅ Aprovar fornecedor → "Fornecedor aprovado com sucesso!"

### Noivo:
- ✅ Aceitar orçamento → "Orçamento aceito com sucesso!"
- ✅ Rejeitar orçamento → "Orçamento rejeitado com sucesso!"

### Público:
- ✅ Cadastro noivos → "Cadastro realizado com sucesso! Faça login para continuar."
- ✅ Cadastro fornecedor → "Cadastro realizado com sucesso! Faça login para continuar."

## Vantagens

1. **Persistência entre redirects**: Mensagens sobrevivem ao redirect
2. **Integração perfeita**: Usa o sistema de toasts existente
3. **Auto-limpeza**: Não há mensagens duplicadas
4. **API simples**: Fácil de usar em qualquer rota
5. **Tipagem forte**: Funções específicas por tipo de mensagem
6. **Compatibilidade**: Funciona com sistema de templates atual

## Compatibilidade

- ✅ **Sistema existente**: Variáveis `erro`/`sucesso` continuam funcionando
- ✅ **Flash messages**: Novas mensagens via redirect
- ✅ **Múltiplas mensagens**: Suporta várias mensagens por requisição
- ✅ **Todos templates**: Funciona em todas as áreas (admin, fornecedor, noivo, público)

## Exemplo Completo

```python
@router.post("/exemplo")
async def exemplo_acao(request: Request):
    try:
        # Realizar operação
        sucesso = realizar_operacao()

        if sucesso:
            informar_sucesso(request, "Operação realizada com sucesso!")
        else:
            informar_erro(request, "Falha na operação!")

        return RedirectResponse("/pagina-destino", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        informar_erro(request, "Erro interno do sistema!")
        return RedirectResponse("/pagina-erro", status_code=status.HTTP_303_SEE_OTHER)
```

O sistema está totalmente integrado e funcional, proporcionando uma experiência de usuário consistente em toda a aplicação!