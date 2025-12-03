# CaseBem - Sistema de Gestão para Casamentos

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

## Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Pré-requisitos](#pré-requisitos)
3. [Guia de Instalação Passo a Passo](#guia-de-instalação-passo-a-passo)
4. [Executando o Projeto no VS Code](#executando-o-projeto-no-vs-code)
5. [Usuários Padrão do Sistema](#usuários-padrão-do-sistema)
6. [Estrutura do Projeto](#estrutura-do-projeto)
7. [Tecnologias Utilizadas](#tecnologias-utilizadas)
8. [Configurações Opcionais](#configurações-opcionais)
9. [Executando os Testes](#executando-os-testes)
10. [Solução de Problemas Comuns](#solução-de-problemas-comuns)

---

## Sobre o Projeto

**CaseBem** é uma plataforma web que conecta **casais de noivos** com **fornecedores de serviços para casamentos**. O sistema permite que:

- **Noivos** criem demandas do que precisam para o casamento e recebam orçamentos de fornecedores
- **Fornecedores** cadastrem seus produtos/serviços e enviem orçamentos para as demandas dos noivos
- **Administradores** gerenciem a plataforma, verifiquem fornecedores e moderem o conteúdo
- **Visitantes** naveguem pelo marketplace público de produtos, serviços e espaços

### Instituição

Desenvolvido pelo **IFES - Instituto Federal do Espírito Santo, Campus Cachoeiro de Itapemirim**, como projeto educacional.

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

### 1. Python 3.11 ou superior

**Verificar se já está instalado:**
```bash
python --version
# ou
python3 --version
```

**Se não tiver instalado:**

- **Windows**: Baixe em [python.org/downloads](https://www.python.org/downloads/) e marque a opção "Add Python to PATH" durante a instalação
- **macOS**: `brew install python@3.13` (com Homebrew) ou baixe em [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3.11 python3.11-venv python3-pip`

### 2. Git

**Verificar se já está instalado:**
```bash
git --version
```

**Se não tiver instalado:**

- **Windows**: Baixe em [git-scm.com](https://git-scm.com/download/win)
- **macOS**: `xcode-select --install` ou `brew install git`
- **Linux**: `sudo apt install git`

### 3. Visual Studio Code

Baixe e instale em: [code.visualstudio.com](https://code.visualstudio.com/)

**Extensão obrigatória:**
- **Python** (da Microsoft) - ID: `ms-python.python`

Para instalar a extensão, abra o VS Code, vá em Extensions (Ctrl+Shift+X) e busque por "Python".

---

## Guia de Instalação Passo a Passo

### Passo 1: Clonar o Repositório

Abra o terminal (ou Git Bash no Windows) e execute:

```bash
git clone https://github.com/RebekaSerafim/CaseBem.git
```

Entre na pasta do projeto:

```bash
cd CaseBem
```

### Passo 2: Abrir o Projeto no VS Code

Você pode abrir o VS Code de duas formas:

**Opção A - Pelo terminal:**
```bash
code .
```

**Opção B - Pelo VS Code:**
1. Abra o VS Code
2. Vá em `File > Open Folder` (ou `Arquivo > Abrir Pasta`)
3. Navegue até a pasta `CaseBem` e clique em `Selecionar Pasta`

### Passo 3: Criar o Ambiente Virtual

No VS Code, abra o terminal integrado:
- Menu: `Terminal > New Terminal`
- Ou atalho: `` Ctrl+` `` (Ctrl + crase)

Execute os comandos abaixo conforme seu sistema operacional:

**Windows (PowerShell ou CMD):**
```powershell
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### Passo 4: Ativar o Ambiente Virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

> Se der erro de permissão no PowerShell, execute primeiro:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Você saberá que o ambiente está ativo quando aparecer `(venv)` no início da linha do terminal.

### Passo 5: Instalar as Dependências

Com o ambiente virtual ativo, execute:

```bash
pip install -r requirements.txt
```

Aguarde a instalação de todos os pacotes. Isso pode levar alguns minutos.

### Passo 6: Configurar o VS Code para usar o Ambiente Virtual

O VS Code pode pedir para selecionar o interpretador Python. Se isso acontecer:

1. Clique em `Select Interpreter` na notificação que aparecer
2. Ou pressione `Ctrl+Shift+P`, digite "Python: Select Interpreter" e pressione Enter
3. Selecione o interpretador que mostra `./venv/bin/python` ou `.\venv\Scripts\python.exe`

### Passo 7: Criar o Arquivo de Configuração (Opcional)

Copie o arquivo de exemplo de variáveis de ambiente:

**Windows:**
```powershell
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

O arquivo `.env` contém configurações como banco de dados e email. Para uso básico de desenvolvimento, as configurações padrão funcionam perfeitamente.

---

## Executando o Projeto no VS Code

### Método 1: Usando Ctrl+F5 (Recomendado)

O projeto já vem configurado para execução no VS Code. Basta:

1. Abrir o arquivo `main.py` no editor (clique nele no painel lateral)
2. Pressionar `Ctrl+F5` (Run Without Debugging)

O VS Code irá:
- Usar a configuração "Python: FastAPI" do arquivo `.vscode/launch.json`
- Iniciar o servidor na porta 8001
- Mostrar os logs no terminal integrado

### Método 2: Usando F5 (Com Debugging)

Se quiser executar com debugging ativado (para usar breakpoints):

1. Abrir o arquivo `main.py`
2. Pressionar `F5`
3. Selecionar "Python: FastAPI" na lista de configurações

### Método 3: Pelo Terminal

Com o ambiente virtual ativo, execute:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### Acessando o Sistema

Após iniciar o servidor, abra o navegador e acesse:

| URL | Descrição |
|-----|-----------|
| http://127.0.0.1:8001 | Página inicial pública |
| http://127.0.0.1:8001/login | Tela de login |
| http://127.0.0.1:8001/docs | Documentação da API (Swagger) |

### Parando o Servidor

- No terminal: pressione `Ctrl+C`
- No VS Code com debugging: clique no botão vermelho de parar ou pressione `Shift+F5`

---

## Usuários Padrão do Sistema

Na primeira execução, o sistema cria automaticamente um banco de dados SQLite (`dados.db`) com dados de exemplo. Os usuários disponíveis são:

### Administrador

| Campo | Valor |
|-------|-------|
| **Email** | `admin@casebem.com` |
| **Senha** | `1234aA@#` |
| **Perfil** | Administrador |
| **URL de acesso** | http://127.0.0.1:8001/admin/dashboard |

### Fornecedores de Teste

Todos os fornecedores usam a **mesma senha**: `1234aA@#`

| Email | Empresa |
|-------|---------|
| `ana@casamentosperfeitos.com` | Casamentos Perfeitos |
| `carlos@eventosmagicos.com` | Eventos Mágicos |
| `mariana@belezaperfeita.com` | Beleza & Estilo |
| `pedro@espacoseletos.com` | Espaços Seletos |
| `julia@fornecedorpremium.com` | Premium Fornecedores |
| `fernanda@docesesabores.com` | Doces & Sabores |
| `roberto@flashfotografias.com` | Flash Fotografias |
| `patricia@decoracoeselegantes.com` | Decorações Elegantes |
| `lucas@someluzeventos.com` | Som & Luz Eventos |
| `beatriz@espacosdossonhos.com` | Espaços dos Sonhos |

### Noivos de Teste

Todos os noivos usam a **mesma senha**: `1234aA@#`

| Email | Nome |
|-------|------|
| `joao.silva@email.com` | João Silva |
| `maria.santos@email.com` | Maria Santos |
| `pedro.oliveira@email.com` | Pedro Oliveira |
| `ana.costa@email.com` | Ana Costa |
| *...e outros casais de teste* | |

### Resumo de Acesso Rápido

```
ADMINISTRADOR:
  Email: admin@casebem.com
  Senha: 1234aA@#

FORNECEDOR (exemplo):
  Email: ana@casamentosperfeitos.com
  Senha: 1234aA@#

NOIVO (exemplo):
  Email: joao.silva@email.com
  Senha: 1234aA@#
```

---

## Estrutura do Projeto

```
CaseBem/
├── main.py                 # Arquivo principal - ponto de entrada da aplicação
├── requirements.txt        # Lista de dependências Python
├── .env.example           # Exemplo de configurações de ambiente
├── dados.db               # Banco de dados SQLite (criado automaticamente)
│
├── .vscode/               # Configurações do VS Code
│   └── launch.json        # Configurações de execução/debug
│
├── core/                  # Núcleo da aplicação
│   ├── models/            # Modelos de dados (Usuario, Fornecedor, etc.)
│   ├── repositories/      # Acesso ao banco de dados
│   └── sql/               # Consultas SQL organizadas
│
├── routes/                # Rotas da aplicação (URLs)
│   ├── public_routes.py   # Rotas públicas (home, login, cadastro)
│   ├── admin_routes.py    # Rotas do administrador
│   ├── fornecedor_routes.py # Rotas do fornecedor
│   └── noivo_routes.py    # Rotas dos noivos
│
├── templates/             # Páginas HTML (Jinja2)
│   ├── publico/           # Páginas públicas
│   ├── admin/             # Páginas do admin
│   ├── fornecedor/        # Páginas do fornecedor
│   └── noivo/             # Páginas dos noivos
│
├── static/                # Arquivos estáticos
│   ├── css/               # Folhas de estilo
│   ├── js/                # JavaScript
│   └── img/               # Imagens
│
├── dtos/                  # Objetos de transferência de dados
├── infrastructure/        # Infraestrutura (banco, email, segurança)
├── util/                  # Utilitários diversos
├── data/seeds/            # Dados de exemplo em JSON
└── tests/                 # Testes automatizados
```

---

## Tecnologias Utilizadas

| Categoria | Tecnologia | Descrição |
|-----------|------------|-----------|
| **Backend** | Python 3.11+ | Linguagem de programação |
| **Framework** | FastAPI | Framework web moderno e rápido |
| **Servidor** | Uvicorn | Servidor ASGI para FastAPI |
| **Banco de Dados** | SQLite | Banco de dados relacional |
| **Templates** | Jinja2 | Engine de templates HTML |
| **Frontend** | Bootstrap 5 | Framework CSS responsivo |
| **Autenticação** | Passlib + Bcrypt | Hash seguro de senhas |
| **Validação** | Pydantic | Validação de dados |

---

## Configurações Opcionais

### Configurando Envio de Emails

O sistema pode enviar emails de boas-vindas e recuperação de senha. Para ativar:

1. Crie uma conta em [Resend](https://resend.com/) (serviço de email)
2. Gere uma API Key
3. Edite o arquivo `.env`:

```env
RESEND_API_KEY=sua_chave_api_aqui
SENDER_EMAIL=seu-email@seudominio.com
SENDER_NAME="Case Bem"
```

Sem essa configuração, o sistema funciona normalmente, apenas não envia emails.

### Resetando o Banco de Dados

Se quiser recomeçar do zero:

1. Pare o servidor
2. Delete o arquivo `dados.db`
3. Inicie o servidor novamente

O sistema recriará automaticamente o banco com os dados de exemplo.

---

## Executando os Testes

O projeto possui testes automatizados. Para executá-los:

### Todos os testes:
```bash
pytest
```

### Com mais detalhes:
```bash
pytest -v
```

### Um arquivo específico:
```bash
pytest tests/test_usuario_repo.py
```

### Com relatório de cobertura:
```bash
pytest --cov=. --cov-report=html
```

O relatório HTML será gerado na pasta `htmlcov/`. Abra `htmlcov/index.html` no navegador.

---

## Solução de Problemas Comuns

### Erro: "python não é reconhecido como comando"

**Windows**: O Python não foi adicionado ao PATH. Reinstale marcando "Add Python to PATH".

**Solução alternativa**: Use `py` em vez de `python`:
```powershell
py -m venv venv
py -m pip install -r requirements.txt
```

### Erro: "Execution Policy" no PowerShell

Execute como administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Port 8001 already in use"

Outro processo está usando a porta. Opções:

1. Pare o outro processo
2. Ou altere a porta no `.vscode/launch.json`:
   ```json
   "args": ["main:app", "--port", "8002"]
   ```

### Erro: "ModuleNotFoundError"

O ambiente virtual não está ativo ou as dependências não foram instaladas:

1. Ative o ambiente virtual (veja Passo 4)
2. Execute `pip install -r requirements.txt`

### Erro ao criar ambiente virtual no Linux

Instale o pacote venv:
```bash
sudo apt install python3.11-venv
```

### O VS Code não reconhece o ambiente virtual

1. Pressione `Ctrl+Shift+P`
2. Digite "Python: Select Interpreter"
3. Selecione o interpretador dentro da pasta `venv`

### O banco de dados não está sendo criado

Verifique se você tem permissão de escrita na pasta do projeto. No Linux/macOS:
```bash
chmod 755 .
```

---

## Contribuindo

Este é um projeto educacional. Contribuições são bem-vindas!

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b minha-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona minha feature'`)
4. Push para a branch (`git push origin minha-feature`)
5. Abra um Pull Request

---

## Licença

Projeto educacional do IFES - Instituto Federal do Espírito Santo, Campus Cachoeiro de Itapemirim.

Todos os direitos reservados.

---

## Contato

- **Instituição**: IFES Campus Cachoeiro de Itapemirim
- **Site**: https://cachoeiro.ifes.edu.br
- **Repositório**: https://github.com/RebekaSerafim/CaseBem

---

*Última atualização: Dezembro de 2025*
