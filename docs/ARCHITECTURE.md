# Arquitetura do Sistema CaseBem

## Visão Geral

O CaseBem segue os princípios da **Clean Architecture** e **Domain-Driven Design (DDD)**, organizando o código em camadas bem definidas com responsabilidades claras.

## Estrutura de Diretórios

```
CaseBem/
├── api/                      # Camada de API (Controllers)
│   └── dtos/                 # Data Transfer Objects
├── core/                     # Camada de Domínio
│   ├── models/               # Modelos de domínio
│   ├── repositories/         # Camada de acesso a dados
│   ├── services/             # Lógica de negócio
│   └── sql/                  # Queries SQL
├── routes/                   # Rotas FastAPI
├── middleware/               # Middlewares HTTP
├── util/                     # Utilitários e infraestrutura
├── tests/                    # Testes automatizados
├── templates/                # Templates Jinja2
└── static/                   # Arquivos estáticos
```

## Camadas da Arquitetura

### 1. **Camada de Apresentação (routes/)**
- **Responsabilidade**: Expor endpoints HTTP e gerenciar requisições/respostas
- **Tecnologia**: FastAPI
- **Regras**:
  - Recebe requisições HTTP
  - Valida dados de entrada via DTOs
  - Delega lógica de negócio para Services
  - Retorna respostas HTTP apropriadas
  - NÃO contém lógica de negócio

**Exemplo**:
```python
@router.post("/usuarios")
async def criar_usuario(usuario_dto: CriarUsuarioDTO):
    id_usuario = usuario_service.criar_usuario(usuario_dto.model_dump())
    return {"id": id_usuario, "mensagem": "Usuário criado com sucesso"}
```

### 2. **Camada de DTOs (api/dtos/)**
- **Responsabilidade**: Validação e transferência de dados
- **Tecnologia**: Pydantic
- **Regras**:
  - Define contratos de entrada/saída
  - Valida tipos e regras de formato
  - Transforma dados entre camadas
  - Agrupa DTOs por contexto de negócio

**Exemplo**:
```python
class CriarUsuarioDTO(BaseDTO):
    nome: str = Field(..., min_length=3)
    email: EmailStr
    senha: str = Field(..., min_length=6)

    @field_validator('nome')
    def validar_nome(cls, v):
        return validar_nome_pessoa(v)
```

### 3. **Camada de Serviços (core/services/)**
- **Responsabilidade**: Lógica de negócio centralizada
- **Regras**:
  - Concentra regras de negócio
  - Orquestra operações entre múltiplos repositórios
  - Valida regras de domínio complexas
  - É stateless (sem estado)
  - Retorna dados ou lança exceções de negócio

**Exemplo**:
```python
class UsuarioService:
    def criar_usuario(self, dados: dict) -> int:
        # Validar regra de negócio
        if self.repo.obter_usuario_por_email(dados['email']):
            raise RegraDeNegocioError("Email já cadastrado")

        # Hash da senha
        dados['senha'] = self.hash_password(dados['senha'])

        # Persistir
        usuario = Usuario(**dados)
        return self.repo.inserir_usuario(usuario)
```

### 4. **Camada de Repositórios (core/repositories/)**
- **Responsabilidade**: Acesso a dados
- **Pattern**: Repository Pattern
- **Regras**:
  - Abstrai acesso ao banco de dados
  - Converte entre modelos de domínio e registros do banco
  - Executa queries SQL
  - Lança exceções de infraestrutura
  - NÃO contém lógica de negócio

**Exemplo**:
```python
def obter_usuario_por_email(email: str) -> Usuario:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
        resultado = cursor.fetchone()
        if not resultado:
            raise RecursoNaoEncontradoError(recurso="Usuario", identificador=email)
        return Usuario(**resultado)
```

### 5. **Camada de Modelos (core/models/)**
- **Responsabilidade**: Representar entidades de domínio
- **Tecnologia**: Dataclasses Python
- **Regras**:
  - Representa conceitos de negócio
  - Contém apenas dados e validações básicas
  - É imutável sempre que possível
  - Usa enums para valores constantes

**Exemplo**:
```python
@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    cpf: str
    perfil: TipoUsuario
    ativo: bool = True
```

### 6. **Camada de Queries SQL (core/sql/)**
- **Responsabilidade**: Definir queries SQL reutilizáveis
- **Regras**:
  - Queries como constantes Python
  - Organizado por contexto (usuario_sql.py, item_sql.py, etc.)
  - Usa parametrização para segurança

## Fluxo de Dados

```
HTTP Request
    ↓
[Route/Controller]  ← Recebe requisição, valida com DTO
    ↓
[Service Layer]     ← Aplica lógica de negócio
    ↓
[Repository]        ← Acessa banco de dados
    ↓
[Database]          ← SQLite
    ↑
[Repository]        ← Retorna modelos de domínio
    ↑
[Service Layer]     ← Processa e retorna resultado
    ↑
[Route/Controller]  ← Converte para resposta HTTP
    ↑
HTTP Response
```

## Tratamento de Exceções

### Hierarquia de Exceções

```
Exception
└── CaseBemError                    # Exceção base do sistema
    ├── ValidacaoError              # Erro de validação de dados
    ├── RegraDeNegocioError         # Violação de regra de negócio
    ├── RecursoNaoEncontradoError   # Recurso não encontrado
    └── BancoDadosError             # Erro de banco de dados
```

### Onde Usar Cada Exceção

- **ValidacaoError**: DTOs e entrada de dados
- **RegraDeNegocioError**: Services (regras de negócio)
- **RecursoNaoEncontradoError**: Repositories (registro não existe)
- **BancoDadosError**: Repositories (erro de SQL)

## Padrões de Design Utilizados

### 1. **Repository Pattern**
Abstrai acesso a dados, permitindo trocar implementação sem afetar a lógica de negócio.

### 2. **Service Layer Pattern**
Centraliza lógica de negócio, tornando código reutilizável e testável.

### 3. **DTO Pattern**
Valida e transforma dados entre camadas.

### 4. **Factory Pattern**
Usado em testes para criar objetos de teste facilmente.

### 5. **Dependency Injection**
Services recebem repositórios via construtor (manual, não framework).

## Princípios SOLID Aplicados

### Single Responsibility Principle (SRP)
- Cada classe tem uma única responsabilidade
- Routes: HTTP
- Services: Lógica de negócio
- Repositories: Acesso a dados

### Open/Closed Principle (OCP)
- Sistema extensível sem modificar código existente
- Novos serviços podem ser adicionados sem afetar existentes

### Liskov Substitution Principle (LSP)
- Repositories podem ser substituídos por mocks em testes

### Interface Segregation Principle (ISP)
- DTOs específicos por operação (CriarUsuarioDTO, AtualizarUsuarioDTO)

### Dependency Inversion Principle (DIP)
- Services dependem de abstrações (repositórios), não implementações concretas

## Gerenciamento de Estado

- **Stateless**: Services e Repositories são stateless
- **Stateful**: Apenas o banco de dados mantém estado
- **Sessão HTTP**: Gerenciada pelo FastAPI via middleware

## Testes

### Estrutura de Testes

```
tests/
├── factories.py              # Factories para criar objetos de teste
├── conftest.py               # Fixtures compartilhadas
├── test_helpers.py           # Helpers de asserção
├── test_*_repo.py            # Testes de repositórios
└── test_*_service.py         # Testes de serviços (futuro)
```

### Estratégia de Testes

- **Testes de Repositório**: Testam SQL e conversão de dados
- **Testes de Serviço** (futuro): Testam lógica de negócio
- **Testes de Integração**: Testam fluxo completo
- **Factory Pattern**: Simplifica criação de dados de teste

## Logging e Monitoramento

- **Logging Estruturado**: JSON format para fácil parsing
- **Níveis**: DEBUG, INFO, WARNING, ERROR
- **Contexto**: Logs incluem contexto de operação (usuário, timestamps)

## Segurança

### Autenticação
- Sessões HTTP via middleware
- Hash de senhas com bcrypt
- Tokens para reset de senha

### Autorização
- Verificação de perfil (ADMIN, NOIVO, FORNECEDOR)
- Decorator `@auth_required` para rotas protegidas

### Validação de Entrada
- DTOs validam todos os dados de entrada
- Queries parametrizadas previnem SQL Injection

## Performance

### Otimizações Implementadas
- Paginação em todas as listagens
- Índices no banco de dados
- Reutilização de conexões
- Lazy loading quando apropriado

## Manutenibilidade

### Convenções de Código
- Type hints em todas as funções
- Docstrings em classes e funções públicas
- Nomes descritivos (sem abreviações)
- Organização por contexto de negócio

### Facilidade de Extensão
- Adicionar nova entidade:
  1. Criar model em `core/models/`
  2. Criar SQL em `core/sql/`
  3. Criar repository em `core/repositories/`
  4. Criar service em `core/services/`
  5. Criar DTOs em `api/dtos/`
  6. Criar routes em `routes/`

## Dependências Externas

### Principais Bibliotecas
- **FastAPI**: Framework web
- **Pydantic**: Validação de dados
- **SQLite**: Banco de dados
- **Jinja2**: Templates
- **bcrypt**: Hash de senhas
- **pytest**: Testes
- **Faker**: Dados de teste

## Considerações Futuras

### Próximas Melhorias
1. ✅ Implementar camada de serviços completa
2. Adicionar cache (Redis) para dados frequentes
3. Implementar event sourcing para auditoria
4. Adicionar filas de mensagens (Celery/RabbitMQ)
5. Migrar para PostgreSQL em produção
6. Implementar API versioning
7. Adicionar testes de carga

## Conclusão

A arquitetura do CaseBem é projetada para ser:
- **Escalável**: Fácil adicionar novos recursos
- **Testável**: Camadas desacopladas facilitam testes
- **Manutenível**: Código organizado e bem documentado
- **Performática**: Otimizações em pontos críticos
- **Segura**: Validações e autenticação em todas as camadas

---

**Última atualização**: Setembro 2025
**Versão da arquitetura**: 2.0 (após FASE 5)