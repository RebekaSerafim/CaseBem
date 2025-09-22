# Serviço de E-mail MailerSend - Case Bem

## Visão Geral

O serviço de e-mail do Case Bem utiliza a API do **MailerSend** para envio de e-mails transacionais e de marketing. O sistema oferece uma interface Python simples e robusta para envio de e-mails com suporte a templates, anexos, personalização e muito mais.

## Arquivos Implementados

### Arquivos Principais:
- `/util/email_service.py` - Serviço principal de envio de e-mails
- `/util/email_config.py` - Configurações centralizadas
- `/util/email_examples.py` - Exemplos de uso e testes

### Dependências:
- `mailersend` - Biblioteca oficial do MailerSend
- `pydantic` - Para validação de dados
- `requests` - Para requisições HTTP

## Configuração

### 1. Variáveis de Ambiente

Adicione no arquivo `.env`:

```env
# Token MailerSend para envio de emails
MAILERSEND_TOKEN=mlsn.seu_token_aqui

# URL base da aplicação (para links nos e-mails)
BASE_URL=https://casebem.com.br

# Templates do MailerSend (opcional)
MAILERSEND_TEMPLATE_WELCOME=template_id_boas_vindas
MAILERSEND_TEMPLATE_PASSWORD_RESET=template_id_recuperacao
MAILERSEND_TEMPLATE_NEW_QUOTE=template_id_novo_orcamento
```

### 2. Instalação da Dependência

```bash
pip install mailersend
```

## Como Usar

### 1. Importações

```python
from util.email_service import (
    MailerSendService,
    EmailRecipient,
    EmailSender,
    EmailAttachment,
    enviar_email_boas_vindas,
    enviar_email_recuperacao_senha,
    enviar_notificacao_orcamento,
)
```

### 2. Envio de E-mail Simples

```python
# Criar instância do serviço
service = MailerSendService()

# Definir remetente
remetente = EmailSender(
    email="noreply@casebem.com.br",
    name="Case Bem"
)

# Definir destinatário
destinatario = EmailRecipient(
    email="cliente@exemplo.com",
    name="João Silva"
)

# Enviar e-mail
resultado = service.enviar_email_simples(
    remetente=remetente,
    destinatarios=[destinatario],
    assunto="Bem-vindo ao Case Bem!",
    conteudo_html="<h1>Olá!</h1><p>Bem-vindo ao nosso serviço!</p>",
    conteudo_texto="Olá! Bem-vindo ao nosso serviço!",
    tags=["boas-vindas"]
)

if resultado["sucesso"]:
    print(f"E-mail enviado! ID: {resultado['message_id']}")
else:
    print(f"Erro: {resultado['erro']}")
```

### 3. Usando Funções de Conveniência

```python
# E-mail de boas-vindas
resultado = enviar_email_boas_vindas(
    email_destinatario="novo@usuario.com",
    nome_destinatario="Maria Silva"
)

# E-mail de recuperação de senha
resultado = enviar_email_recuperacao_senha(
    email_destinatario="usuario@exemplo.com",
    nome_destinatario="João Santos",
    token_reset="abc123def456"
)

# Notificação de orçamento
resultado = enviar_notificacao_orcamento(
    email_noivo="casal@exemplo.com",
    nome_noivo="Ana e Pedro",
    nome_fornecedor="Buffet Delícias",
    item_nome="Buffet completo",
    valor_orcamento=15000.00
)
```

### 4. E-mail com Anexos

```python
import base64

# Preparar anexo
with open("documento.pdf", "rb") as arquivo:
    conteudo_base64 = base64.b64encode(arquivo.read()).decode()

anexo = EmailAttachment(
    content=conteudo_base64,
    filename="contrato.pdf",
    disposition="attachment"
)

# Enviar com anexo
resultado = service.enviar_email_simples(
    remetente=remetente,
    destinatarios=[destinatario],
    assunto="Documentos do Casamento",
    conteudo_html="<p>Seguem os documentos em anexo.</p>",
    anexos=[anexo]
)
```

## Classes e Modelos

### EmailSender
```python
@dataclass
class EmailSender:
    email: str              # E-mail do remetente
    name: Optional[str]     # Nome do remetente (opcional)
```

### EmailRecipient
```python
@dataclass
class EmailRecipient:
    email: str              # E-mail do destinatário
    name: Optional[str]     # Nome do destinatário (opcional)
```

### EmailAttachment
```python
@dataclass
class EmailAttachment:
    content: str            # Conteúdo em Base64
    filename: str           # Nome do arquivo
    disposition: str        # "attachment" ou "inline"
    id: Optional[str]       # ID para referenciar no HTML (opcional)
```

## Métodos Principais

### MailerSendService.enviar_email_simples()

Envia um e-mail simples com suporte completo a recursos.

**Parâmetros:**
- `remetente: EmailSender` - Dados do remetente
- `destinatarios: List[EmailRecipient]` - Lista de destinatários
- `assunto: str` - Assunto do e-mail
- `conteudo_html: str` - Conteúdo em HTML
- `conteudo_texto: Optional[str]` - Conteúdo em texto plano
- `reply_to: Optional[EmailSender]` - E-mail para resposta
- `cc: Optional[List[EmailRecipient]]` - Destinatários em cópia
- `bcc: Optional[List[EmailRecipient]]` - Destinatários em cópia oculta
- `anexos: Optional[List[EmailAttachment]]` - Lista de anexos
- `tags: Optional[List[str]]` - Tags para categorização

**Retorno:**
```python
{
    "sucesso": bool,
    "message_id": str,      # ID da mensagem (se sucesso)
    "status_code": int,     # Código de status HTTP
    "erro": str,            # Mensagem de erro (se falha)
    "data": dict            # Dados completos da resposta
}
```

### MailerSendService.enviar_email_template()

Envia e-mail usando templates do MailerSend.

**Parâmetros:**
- `remetente: EmailSender` - Dados do remetente
- `destinatarios: List[EmailRecipient]` - Lista de destinatários
- `template_id: str` - ID do template no MailerSend
- `personalizacao: Optional[List[Dict]]` - Dados de personalização
- `tags: Optional[List[str]]` - Tags para categorização

## Configurações (EmailConfig)

### Remetentes Predefinidos

```python
# Remetente padrão
EmailConfig.get_sender_config("default")
# {"email": "noreply@casebem.com.br", "name": "Case Bem"}

# Suporte
EmailConfig.get_sender_config("support")
# {"email": "suporte@casebem.com.br", "name": "Case Bem - Suporte"}

# Notificações
EmailConfig.get_sender_config("notifications")
# {"email": "notificacoes@casebem.com.br", "name": "Case Bem - Notificações"}
```

### URLs e Links

```python
# URL base
EmailConfig.build_url("dashboard")
# "https://casebem.com.br/dashboard"

# URL com parâmetros
EmailConfig.build_url("perfil", {"tab": "configuracoes"})
# "https://casebem.com.br/perfil?tab=configuracoes"
```

### Tags Padrão

```python
# Tags por categoria
EmailConfig.get_tags("boas_vindas")
# ["sistema", "case-bem", "boas-vindas", "novo-usuario"]

EmailConfig.get_tags("seguranca")
# ["sistema", "case-bem", "seguranca", "autenticacao"]
```

## Funções de Conveniência

### enviar_email_boas_vindas()
Envia e-mail de boas-vindas personalizado para novos usuários.

### enviar_email_recuperacao_senha()
Envia e-mail com link para recuperação de senha.

### enviar_notificacao_orcamento()
Notifica noivos sobre novos orçamentos recebidos.

## Tratamento de Erros

O serviço possui tratamento robusto de erros:

```python
resultado = service.enviar_email_simples(...)

if resultado["sucesso"]:
    # E-mail enviado com sucesso
    message_id = resultado["message_id"]
    print(f"E-mail enviado: {message_id}")
else:
    # Erro no envio
    erro = resultado["erro"]
    print(f"Falha no envio: {erro}")
```

## Limitações e Considerações

### Limitações do MailerSend:
- **Destinatários por e-mail**: Máximo 50
- **CC/BCC**: Máximo 10 cada
- **Tamanho do conteúdo**: Máximo 2MB (HTML + texto)
- **Anexos**: Máximo 25MB por anexo
- **Tags**: Máximo 5 por e-mail

### Domínios Verificados:
- O domínio do remetente deve estar verificado no MailerSend
- Use apenas e-mails de domínios verificados como remetente

### Ambientes:
- **Desenvolvimento**: E-mails podem ser simulados (fake_send)
- **Produção**: E-mails são enviados normalmente

## Monitoramento

### Logs de E-mail
Os e-mails são automaticamente logados para auditoria.

### Status de Entrega
Use o `message_id` retornado para consultar o status via API do MailerSend.

### Métricas
Configure tags apropriadas para monitorar:
- Taxa de entrega
- Taxa de abertura
- Taxa de clique
- Bounces e reclamações

## Exemplo Completo

```python
from util.email_service import MailerSendService, EmailSender, EmailRecipient
from util.email_config import EmailConfig

# Configurar serviço
service = MailerSendService()

# Usar configurações predefinidas
sender_config = EmailConfig.get_sender_config("notifications")
remetente = EmailSender(**sender_config)

# Destinatário
destinatario = EmailRecipient(
    email="cliente@exemplo.com",
    name="João Silva"
)

# Links dinâmicos
link_dashboard = EmailConfig.build_url("dashboard")
link_perfil = EmailConfig.build_url("perfil", {"edit": "true"})

# Tags categorizadas
tags = EmailConfig.get_tags("notificacoes")

# Conteúdo HTML responsivo
html_content = f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #28a745; padding: 20px; text-align: center;">
        <h1 style="color: white;">Case Bem</h1>
    </div>

    <div style="padding: 20px;">
        <h2>Olá, João!</h2>
        <p>Você tem atualizações importantes na sua conta.</p>

        <div style="text-align: center; margin: 30px 0;">
            <a href="{link_dashboard}"
               style="background-color: #28a745; color: white; padding: 15px 30px;
                      text-decoration: none; border-radius: 5px;">
               Ver Dashboard
            </a>
        </div>

        <p>Você também pode <a href="{link_perfil}">atualizar seu perfil</a>.</p>
    </div>

    <div style="background-color: #f8f9fa; padding: 15px; text-align: center;">
        <small>Case Bem - Conectando sonhos, criando memórias</small>
    </div>
</div>
"""

# Enviar e-mail
resultado = service.enviar_email_simples(
    remetente=remetente,
    destinatarios=[destinatario],
    assunto="Atualizações da sua conta - Case Bem",
    conteudo_html=html_content,
    tags=tags
)

# Verificar resultado
if resultado["sucesso"]:
    print(f"✅ E-mail enviado com sucesso!")
    print(f"   Message ID: {resultado['message_id']}")
else:
    print(f"❌ Erro no envio: {resultado['erro']}")
```

## Integração com Rotas

### Exemplo em Rota de Cadastro:

```python
from util.email_service import enviar_email_boas_vindas

@router.post("/cadastro")
async def post_cadastro(request: Request, ...):
    # ... lógica de cadastro ...

    if usuario_criado:
        # Enviar e-mail de boas-vindas
        resultado_email = enviar_email_boas_vindas(
            email_destinatario=usuario.email,
            nome_destinatario=usuario.nome
        )

        if resultado_email["sucesso"]:
            informar_sucesso(request, "Cadastro realizado! Verifique seu e-mail.")
        else:
            # Log do erro, mas não falha o cadastro
            print(f"Erro ao enviar e-mail: {resultado_email['erro']}")
            informar_sucesso(request, "Cadastro realizado com sucesso!")

        return RedirectResponse("/login", status_code=303)
```

O serviço está pronto para uso em produção e oferece todas as funcionalidades necessárias para um sistema robusto de e-mails transacionais!