# 🌟 CaseBem - Sistema de Gestão para Casamentos

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)](https://sqlite.org)
[![Tests](https://img.shields.io/badge/Tests-126/126_Pass-brightgreen.svg)](#testes)
[![Coverage](https://img.shields.io/badge/Coverage-36%25-yellow.svg)](#testes)

Sistema web moderno para conectar noivos e fornecedores de serviços para casamentos, desenvolvido com arquitetura limpa e boas práticas de programação.

## 🎯 Características Principais

- **🏗️ Clean Architecture**: Separação clara entre camadas (Core, Routes, Infrastructure)
- **📋 Código Organizado**: Estrutura modular com repositories, services e DTOs
- **🧪 Testes Automatizados**: 126 testes unitários com 100% de aprovação
- **📊 Logs Estruturados**: Sistema de logging para debugging e monitoramento
- **✅ Validações Robustas**: DTOs com Pydantic e validações centralizadas
- **🚨 Exception Handling**: Sistema de exceções tipadas e padronizado
- **🔧 Padrões de Projeto**: Repository, Factory, Service Layer implementados

## 🏗️ Arquitetura do Projeto

```
📁 CaseBem/
├── 📁 core/                    # 🎯 Núcleo do sistema
│   ├── 📁 models/             # 📋 14 modelos de domínio
│   ├── 📁 repositories/       # 💾 14 repositórios (BaseRepo)
│   ├── 📁 services/           # 🧠 10 serviços de negócio
│   ├── 📁 sql/                # 📄 Queries SQL organizadas
│   └── 📁 validators/         # ✅ Validadores de negócio
├── 📁 infrastructure/          # ⚙️ Infraestrutura
│   ├── 📁 database/           # 💾 Conexão e adapters
│   ├── 📁 security/           # 🔒 Autenticação e autorização
│   ├── 📁 logging/            # 📊 Sistema de logs
│   └── 📁 email/              # 📧 Serviço de email
├── 📁 dtos/                   # 📝 6 DTOs com validação Pydantic
├── 📁 routes/                 # 🛣️  5 routers FastAPI
│   ├── 📄 public_routes.py    # Rotas públicas
│   ├── 📄 admin_routes.py     # Painel admin
│   ├── 📄 noivo_routes.py     # Área dos noivos
│   ├── 📄 fornecedor_routes.py # Área dos fornecedores
│   └── 📄 usuario_routes.py   # Rotas de usuário
├── 📁 util/                   # 🔧 13 utilitários
├── 📁 data/                   # 💾 Dados e seeds
│   └── 📁 seeds/              # 📦 10 arquivos JSON para seed
├── 📁 tests/                  # 🧪 126 testes automatizados
│   ├── 📄 factories.py        # 🏭 Factories para testes
│   ├── 📄 test_helpers.py     # 🛠️  Helpers de asserção
│   ├── 📄 conftest.py         # ⚙️  Fixtures compartilhadas
│   └── 📁 e2e/                # 🌐 Testes end-to-end
├── 📁 templates/              # 🎨 Templates Jinja2
│   ├── 📁 admin/              # Admin templates
│   ├── 📁 fornecedor/         # Fornecedor templates
│   ├── 📁 noivo/              # Noivo templates
│   ├── 📁 publico/            # Templates públicos
│   └── 📁 usuario/            # Templates de usuário
├── 📁 static/                 # 📦 Assets (CSS, JS, imagens)
├── 📁 scripts/                # 🔧 Scripts auxiliares
└── 📁 config/                 # ⚙️ Configurações
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- Git

### Instalação Rápida
```bash
# 1. Clonar o repositório
git clone https://github.com/ifes-serra/casebem.git
cd CaseBem

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente (Linux/Mac)
source .venv/bin/activate
# Ou Windows:
# .venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar aplicação
python main.py
```

### 🌐 Acessar o Sistema
Abra o navegador em: `http://localhost:8000`

### 🧪 Executar Testes
```bash
# Todos os testes unitários (126 testes)
pytest tests/ --ignore=tests/e2e

# Com cobertura detalhada
pytest tests/ --ignore=tests/e2e --cov=core --cov=routes --cov=util --cov-report=html

# Testes específicos de um módulo
pytest tests/test_usuario_repo.py -v

# Testes com relatório detalhado
pytest tests/ --ignore=tests/e2e -v
```

## 👤 Usuários Padrão do Sistema

| Perfil | Email | Senha | Funcionalidades |
|--------|-------|-------|-----------------|
| **Admin** | admin@casebem.com | 1234aA@# | Gerenciar sistema completo |
| **Noivo** | (ver data/seeds/usuarios.json) | 1234aA@# | Criar demandas, gerenciar orçamentos |
| **Fornecedor** | (ver data/seeds/fornecedores.json) | 1234aA@# | Oferecer serviços, responder demandas |

> ⚠️ **Importante**: Todos os usuários de seed usam a senha `1234aA@#`. Altere as senhas no primeiro login em ambiente de produção!

## 📊 Métricas de Qualidade

| Métrica | Valor | Status |
|---------|-------|--------|
| **📏 Linhas de código** | ~21.000 | ✅ Organizado |
| **🧪 Testes** | 126/126 passando | ✅ 100% |
| **📈 Cobertura** | 36% | 🟡 Em crescimento |
| **🏭 Serviços** | 10 implementados | ✅ Completo |
| **📦 Repositórios** | 14 padronizados | ✅ BaseRepo |
| **📋 Modelos** | 14 modelos | ✅ Completo |
| **🛣️  Routers** | 5 routers | ✅ Organizados |
| **🏷️ Type Hints** | 100% coverage | ✅ Total |
| **⚠️ Exception Handling** | Padronizado | ✅ Consistente |

## 📝 Funcionalidades

### Para Noivos
- ✅ Cadastro e gerenciamento de perfil de casal
- ✅ Busca de fornecedores por categoria e tipo
- ✅ Criação e gestão de demandas de casamento
- ✅ Recebimento e análise de orçamentos
- ✅ Sistema de favoritos para itens/fornecedores
- ✅ Chat integrado com fornecedores

### Para Fornecedores
- ✅ Cadastro diferenciado por tipo (produtos/serviços)
- ✅ Gestão completa de itens oferecidos
- ✅ Recebimento de demandas dos noivos
- ✅ Criação e envio de orçamentos
- ✅ Perfil público com verificação
- ✅ Sistema de categorias organizado

### Para Administradores
- ✅ Gestão completa de usuários
- ✅ Verificação de fornecedores
- ✅ Gestão de categorias (produtos e serviços)
- ✅ Ativação/desativação de registros
- ✅ Acesso total ao sistema

## 🔧 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI de alta performance
- **SQLite** - Banco de dados relacional
- **Pydantic** - Validação de dados com tipos
- **Jinja2** - Engine de templates
- **Passlib[bcrypt]** - Hash de senhas seguro
- **Python-JOSE** - JWT tokens

### Frontend
- **HTML5/CSS3** - Interface moderna
- **JavaScript** - Interatividade
- **Bootstrap** - Framework CSS responsivo

### Testes
- **pytest** - Framework de testes
- **pytest-asyncio** - Testes assíncronos
- **pytest-cov** - Cobertura de código
- **Faker** - Geração de dados fake (pt_BR)
- **Playwright** - Testes E2E

### Qualidade
- **Type Hints** - Tipagem estática (100%)
- **Dataclasses** - Modelos de domínio
- **Structured Logging** - Logs organizados
- **Clean Architecture** - Separação de responsabilidades

## 🎓 Conceitos Implementados

### 🧱 Padrões de Projeto (Design Patterns)
- **🏭 Repository Pattern**: Abstração do acesso a dados com `BaseRepo`
- **🔨 Factory Pattern**: Criação flexível de objetos para testes
- **⚙️ Service Layer**: Lógica de negócio centralizada (10 serviços)
- **📝 DTO Pattern**: Transferência segura de dados com Pydantic

### 🏗️ Arquitetura e Princípios
- **🔄 Separation of Concerns**: Cada camada tem responsabilidade específica
- **💉 Dependency Injection**: Baixo acoplamento entre componentes
- **🧹 Clean Architecture**: Independência entre camadas
- **🎯 SOLID Principles**: Single Responsibility, Open/Closed, etc.

### 🧪 Testes e Qualidade
- **🔬 Unit Tests**: 126 testes testando componentes isoladamente
- **🔗 Integration Tests**: Testando fluxos completos
- **🏭 Test Factories**: Criação de dados de teste flexíveis
- **🌐 E2E Tests**: Testes end-to-end com Playwright

### 🚨 Tratamento de Erros
- **⚠️ Custom Exceptions**: Hierarquia de exceções específicas
- **📋 Structured Logging**: Logs com contexto e metadata
- **🛡️ Error Handling**: Tratamento padronizado em todos os repos

## 💾 Sistema de Seeds

O projeto inclui um sistema completo de seeds para popular o banco de dados com dados de teste:

- **10 Fornecedores** com perfis completos
- **10 Casais** (20 noivos)
- **1 Administrador** do sistema
- **20+ Categorias** de serviços/produtos
- **Múltiplos Itens** de exemplo

Todos os dados são importados automaticamente na primeira execução. Veja [data/README.md](data/README.md) para mais detalhes.

## 🤝 Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Escreva testes para suas mudanças
4. Garanta que todos os testes passam (`pytest tests/ --ignore=tests/e2e`)
5. Commit suas mudanças (`git commit -am 'feat: adiciona nova feature'`)
6. Push para a branch (`git push origin feature/nova-feature`)
7. Abra um Pull Request

### Convenções de Commit
Usamos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `test:` Testes
- `refactor:` Refatoração
- `chore:` Manutenção

## 📈 Roadmap

### ✅ Concluído
- [x] Sistema de autenticação completo
- [x] CRUD de todas entidades
- [x] Sistema de orçamentos
- [x] Chat entre noivos e fornecedores
- [x] Sistema de favoritos
- [x] Painel administrativo
- [x] 126 testes unitários

### 🚧 Em Desenvolvimento
- [ ] Testes de integração completos
- [ ] Testes E2E completos
- [ ] Sistema de notificações em tempo real
- [ ] Upload de múltiplas imagens

### 📋 Planejado
- [ ] Migrar para PostgreSQL
- [ ] API REST documentada (OpenAPI)
- [ ] Sistema de pagamentos
- [ ] App mobile
- [ ] Internacionalização (i18n)

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos no **IFES - Campus Serra**.

---

<div align="center">

**🚀 Desenvolvido para o ensino de programação de qualidade**

> *"Código bom não é apenas código que funciona. É código que é organizado, testado e mantível."*

**Status**: ✅ Em Desenvolvimento | **Versão**: 2.0 | **Última Atualização**: Outubro 2025

[Reportar Bug](https://github.com/ifes-serra/casebem/issues) • [Solicitar Feature](https://github.com/ifes-serra/casebem/issues)

</div>
