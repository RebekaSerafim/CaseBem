# Sistema de Toast - Case Bem

## Visão Geral

O sistema de toast foi implementado para substituir as mensagens de alerta inline da aplicação. Os toasts aparecem como notificações flutuantes na parte superior direita da tela, logo abaixo do cabeçalho, e são empilhados quando há múltiplas notificações.

## Características

- **Posicionamento**: Canto superior direito, abaixo do cabeçalho
- **Empilhamento**: Múltiplos toasts são exibidos em pilha
- **Tipos suportados**: `success`, `danger`, `warning`, `info`, `alert`
- **Auto-dismiss**: Configurável por tipo (5-7 segundos por padrão)
- **Bootstrap 5.3**: Utiliza exclusivamente classes nativas do Bootstrap

## Arquivos Criados/Modificados

### Novos Arquivos:
- `/static/js/toast-manager.js` - Gerenciador de toasts
- `/templates/components/toast-handler.html` - Handler automático de mensagens
- `/templates/components/toast-examples.html` - Página de teste/exemplo

### Arquivos Modificados:
- `/templates/fornecedor/base.html` - Removido alertas inline, adicionado toast system
- `/templates/noivo/base.html` - Removido alertas inline, adicionado toast system
- `/templates/admin/base.html` - Removido alertas inline, adicionado toast system
- `/templates/publico/base.html` - Adicionado toast system

## Como Usar

### 1. Frontend (JavaScript)

```javascript
// Métodos diretos (mais simples)
showSuccess('Operação realizada com sucesso!');
showError('Erro ao processar solicitação!');
showWarning('Atenção! Verifique os dados.');
showInfo('Processo pode levar alguns minutos.');
showAlert('Ação importante requerida!');

// Método genérico
showToast('Mensagem personalizada', 'success', 5000);

// Usando o manager diretamente (mais controle)
window.toastManager.success('Mensagem', 5000);
window.toastManager.error('Mensagem', 7000);
window.toastManager.warning('Mensagem', 6000);
window.toastManager.info('Mensagem', 5000);
window.toastManager.alert('Mensagem', 6000);

// Limpar todos os toasts
window.toastManager.clear();
```

### 2. Backend (Python)

O sistema automaticamente converte as variáveis de contexto em toasts:

```python
# Mensagem simples
return templates.TemplateResponse("template.html", {
    "request": request,
    "sucesso": "Operação realizada com sucesso!",
    "erro": "Algo deu errado!",
    "warning": "Cuidado com esta ação!",
    "info": "Informação importante para o usuário",
    "alert": "Alerta crítico!"
})

# Múltiplas mensagens
messages = [
    {"text": "Primeira mensagem", "type": "success"},
    {"text": "Segunda mensagem", "type": "info", "duration": 3000},
    {"text": "Terceira mensagem", "type": "warning"}
]

return templates.TemplateResponse("template.html", {
    "request": request,
    "messages": messages
})
```

## Tipos de Toast

| Tipo | Classe Bootstrap | Duração Padrão | Ícone | Uso |
|------|------------------|----------------|-------|-----|
| `success` | `text-bg-success` | 5s | ✓ | Operações bem-sucedidas |
| `danger` | `text-bg-danger` | 7s | ✕ | Erros e falhas |
| `warning` | `text-bg-warning` | 6s | ⚠ | Avisos e alertas |
| `info` | `text-bg-info` | 5s | ℹ | Informações gerais |
| `alert` | `text-bg-primary` | 6s | ! | Alertas importantes |

## Configuração

### Duração Personalizada
```javascript
// Toast que não desaparece automaticamente
showSuccess('Mensagem persistente', 0);

// Toast com duração personalizada (3 segundos)
showInfo('Mensagem rápida', 3000);
```

### Posicionamento
O container de toasts é criado automaticamente com as seguintes características:
- `position: fixed`
- `top: 0; right: 0`
- `margin-top: 80px` (abaixo do header)
- `z-index: 9999`

## Migração do Sistema Antigo

### Antes (Sistema Inline):
```html
{% if erro %}
<div class="alert alert-danger alert-dismissible fade show" role="alert">
    {{ erro }}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endif %}
```

### Depois (Sistema Toast):
```javascript
// Automaticamente convertido pelo toast-handler.html
// Não requer mudanças no código Python
```

## Compatibilidade

- **Bootstrap**: 5.3+
- **Browsers**: Todos os browsers modernos
- **Mobile**: Totalmente responsivo
- **Acessibilidade**: Compatível com screen readers (aria-live="assertive")

## Teste

Para testar o sistema, acesse `/templates/components/toast-examples.html` em um browser local ou implemente a rota correspondente.

## Vantagens do Novo Sistema

1. **Não invasivo**: Não ocupa espaço no layout principal
2. **Empilhamento**: Múltiplas mensagens são organizadas verticalmente
3. **Auto-dismiss**: Remove automaticamente após tempo configurado
4. **Responsivo**: Funciona bem em dispositivos móveis
5. **Consistente**: Visual uniforme em toda a aplicação
6. **Acessível**: Suporte a tecnologias assistivas
7. **Performático**: Reutiliza o mesmo container para todos os toasts