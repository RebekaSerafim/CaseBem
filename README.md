# Case Bem - Sistema de Gestão para Casamentos

Sistema web para conectar noivos e fornecedores de serviços para casamentos, desenvolvido com FastAPI e SQLite.

## 🚀 Tecnologias

- **Backend:** FastAPI, Python 3.13
- **Banco de dados:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Testes:** Pytest
- **Autenticação:** Sessões com middleware

## 📁 Estrutura do Projeto

```
CaseBem/
├── model/          # Modelos de dados
├── repo/           # Repositórios (acesso a dados)
├── sql/            # Queries SQL organizadas
├── routes/         # Rotas da API (controllers)
├── templates/      # Templates HTML
├── static/         # Arquivos estáticos (CSS, JS, imagens)
├── tests/          # Testes unitários
├── util/           # Utilitários (auth, database, etc.)
└── main.py         # Ponto de entrada da aplicação
```

## 🔧 Instalação e Execução

1. **Clone o repositório:**
```bash
git clone [url-do-repositorio]
cd CaseBem
```

2. **Crie o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação:**
```bash
python main.py
```

5. **Acesse no navegador:**
```
http://127.0.0.1:8000
```

## 👤 Usuário Padrão

- **Email:** admin@casebem.com
- **Senha:** admin123

⚠️ **Importante:** Altere a senha no primeiro login!

## 🧪 Executar Testes

```bash
pytest
```

## 📝 Funcionalidades

### Para Noivos
- Cadastro e gerenciamento de perfil
- Busca de fornecedores por categoria
- Criação e gestão de demandas
- Sistema de orçamentos

### Para Fornecedores
- Cadastro diferenciado por tipo (produtos, serviços, espaços)
- Gestão de itens oferecidos
- Sistema de categorias
- Recebimento e resposta a demandas

### Para Administradores
- Gestão de usuários e fornecedores
- Verificação de fornecedores
- Gestão de categorias de itens
- Relatórios e estatísticas

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas:

- **Presentation Layer:** Templates e rotas
- **Business Layer:** Lógica de negócio nos repositories
- **Data Layer:** Models e SQL queries
- **Utility Layer:** Autenticação, segurança, database

## 📊 Status do Projeto

- ✅ Sistema de autenticação completo
- ✅ CRUD de usuários, fornecedores e itens
- ✅ Sistema de categorias
- ✅ Templates responsivos
- ✅ Testes unitários
- 🔄 Em desenvolvimento: Sistema de orçamentos
- 📋 Planejado: Sistema de pagamentos

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos no IFES.
