# 📧 Serviço de Email - CaseBem

## 📋 Visão Geral

O CaseBem utiliza o **MailerSend** como provedor de email através da biblioteca `mailersend-python`. O serviço está totalmente configurado e operacional.

## 🔧 Arquitetura

### Localização dos Arquivos
```
infrastructure/email/
├── email_service.py       # Serviço principal de envio
├── email_config.py        # Configurações centralizadas
└── email_examples.py      # Exemplos de uso

templates/emails/
├── base_layout.html       # Layout base para emails
├── boas_vindas.html       # Template de boas-vindas
├── recuperacao_senha.html # Template de reset de senha
└── notificacao_orcamento.html # Template de notificação
```

## 🚀 Funcionalidades Implementadas

### 1. Email de Boas-Vindas ✅
**Status:** Implementado e em uso

**Quando é enviado:**
- Cadastro de novos noivos (ambos recebem)
- Cadastro de novos fornecedores

**Localização:**
- `routes/public_routes.py:300-312` (noivos)
- `routes/public_routes.py:436-442` (fornecedores)

**Função:**
```python
from infrastructure.email.email_service import enviar_email_boas_vindas

enviar_email_boas_vindas(email_destinatario, nome_destinatario)
```

### 2. Email de Recuperação de Senha ✅
**Status:** Implementado e em uso

**Quando é enviado:**
- Usuário solicita recuperação de senha via `/esqueci-senha`
- Email contém link com token de 24h de validade

**Localização:**
- `routes/public_routes.py:577-628` (solicitação)
- `routes/public_routes.py:631-794` (reset com token)

**Função:**
```python
from infrastructure.email.email_service import enviar_email_recuperacao_senha

enviar_email_recuperacao_senha(email, nome, token_reset)
```

### 3. Notificação de Orçamento 🔄
**Status:** Pronto para uso (aguardando integração)

**Função disponível:**
```python
from infrastructure.email.email_service import enviar_notificacao_orcamento

enviar_notificacao_orcamento(email_noivo, nome_noivo, nome_fornecedor, item_nome, valor)
```

## ⚙️ Configuração

### Variáveis de Ambiente Obrigatórias

```bash
# API Token do MailerSend (OBRIGATÓRIO)
MAILERSEND_TOKEN=mlsn.your_token_here
```

### Variáveis de Ambiente Opcionais

```bash
# Configuração de Remetentes (usa fallback se não definido)
DEFAULT_SENDER_EMAIL=noreply@casebem.com.br
DEFAULT_SENDER_NAME=Case Bem

SUPPORT_SENDER_EMAIL=suporte@casebem.com.br
SUPPORT_SENDER_NAME=Case Bem - Suporte

NOTIFICATIONS_SENDER_EMAIL=notificacoes@casebem.com.br
NOTIFICATIONS_SENDER_NAME=Case Bem - Notificações

# URLs da Aplicação
BASE_URL=https://casebem.com.br

# Templates do MailerSend (opcional - usa templates HTML locais se vazio)
MAILERSEND_TEMPLATE_WELCOME=
MAILERSEND_TEMPLATE_PASSWORD_RESET=
MAILERSEND_TEMPLATE_NEW_QUOTE=
MAILERSEND_TEMPLATE_QUOTE_ACCEPTED=
MAILERSEND_TEMPLATE_NEW_LEAD=

# Configurações de Comportamento
EMAIL_MAX_RETRIES=3
EMAIL_TIMEOUT_SECONDS=30
EMAIL_DEBUG=true
EMAIL_LOG_EMAILS=true
EMAIL_SEND_EMAILS=true      # Mudar para true em produção
EMAIL_FAKE_SEND=false        # Mudar para false em produção
```

## 📝 Modo de Operação Atual

### Templates Locais (Atual) ✅
- **Vantagem:** Controle total sobre HTML e estilos
- **Desvantagem:** Mudanças requerem deploy
- **Uso:** Todos os emails usam templates da pasta `templates/emails/`

### Templates MailerSend (Opcional) 🔄
- **Vantagem:** Edição sem deploy via dashboard MailerSend
- **Desvantagem:** Requer configuração inicial dos templates
- **Uso:** Defina os IDs dos templates nas variáveis `MAILERSEND_TEMPLATE_*`

## 🛠️ Como Adicionar Novos Emails

### 1. Criar Template HTML
```html
<!-- templates/emails/meu_email.html -->
{% extends "emails/base_layout.html" %}

{% block content %}
<h2>Olá, {{ nome_usuario }}!</h2>
<p>Seu conteúdo aqui...</p>
{% endblock %}
```

### 2. Criar Função de Envio
```python
# infrastructure/email/email_service.py

def enviar_meu_email(email: str, nome: str, dados: dict) -> Dict[str, Any]:
    """Envia email personalizado"""
    service = get_email_service()
    sender_config = EmailConfig.get_sender_config("default")

    remetente = EmailSender(
        email=sender_config["email"],
        name=sender_config["name"]
    )

    destinatario = EmailRecipient(email=email, name=nome)

    # Renderizar template
    conteudo_html = service.render_template(
        'meu_email.html',
        nome_usuario=nome,
        **dados
    )

    return service.enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Meu Assunto",
        conteudo_html=conteudo_html,
        tags=EmailConfig.get_tags("categoria")
    )
```

### 3. Usar nas Rotas
```python
from infrastructure.email.email_service import enviar_meu_email

try:
    resultado = enviar_meu_email(user.email, user.nome, dados)
    if resultado["sucesso"]:
        logger.info(f"Email enviado com sucesso para {user.email}")
    else:
        logger.error(f"Erro ao enviar email: {resultado['erro']}")
except Exception as e:
    logger.error(f"Exceção ao enviar email: {e}")
```

## 🔍 Tratamento de Erros

O serviço **sempre retorna um dict** com:
```python
{
    "sucesso": bool,           # True/False
    "message_id": str,         # ID da mensagem (se sucesso)
    "erro": str,              # Mensagem de erro (se falha)
    "data": dict              # Dados adicionais
}
```

**Sempre use try/except** ao enviar emails:
```python
try:
    resultado = enviar_email_boas_vindas(email, nome)
    if not resultado["sucesso"]:
        logger.error(f"Falha no envio: {resultado['erro']}")
except Exception as e:
    logger.error(f"Exceção no envio: {e}")
```

## 📊 Logs e Monitoramento

### Logs Automáticos
- ✅ Todos os envios são logados via `infrastructure.logging`
- ✅ Erros incluem contexto (email, erro, stacktrace)
- ✅ Sucessos incluem message_id para rastreamento

### Monitoramento no MailerSend
1. Acesse: https://app.mailersend.com
2. Navegue para **Analytics** > **Activity**
3. Veja métricas de entrega, abertura, cliques

## 🧪 Testes

### Ambiente de Desenvolvimento
```bash
# .env
EMAIL_SEND_EMAILS=false    # Não envia emails reais
EMAIL_FAKE_SEND=true       # Simula envio e loga
EMAIL_DEBUG=true           # Modo debug ativo
EMAIL_LOG_EMAILS=true      # Loga conteúdo dos emails
```

### Ambiente de Produção
```bash
# .env
EMAIL_SEND_EMAILS=true     # Envia emails reais
EMAIL_FAKE_SEND=false      # Desativa simulação
EMAIL_DEBUG=false          # Desativa debug
EMAIL_LOG_EMAILS=false     # Não loga conteúdo (privacidade)
```

## 📚 Referências

- [MailerSend Docs](https://developers.mailersend.com/)
- [mailersend-python GitHub](https://github.com/mailersend/mailersend-python)
- [Template Examples](./infrastructure/email/email_examples.py)

## 🚨 Importante

1. **NUNCA commite** o `MAILERSEND_TOKEN` real no git
2. **Use variáveis de ambiente** para produção
3. **Teste em desenvolvimento** antes de enviar para produção
4. **Monitore os logs** para identificar falhas
5. **Valide emails** antes de enviar para evitar bounces

---

**Última atualização:** Outubro 2025
**Mantido por:** Equipe CaseBem
