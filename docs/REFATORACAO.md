# Plano de Refatoração - Sistema CaseBem

## 1. Visão Geral

### Objetivo Principal
Refatorar o sistema de perfis de usuário de 5 tipos (ADMIN, NOIVO, FORNECEDOR, PRESTADOR, LOCADOR) para apenas 3 tipos (ADMIN, NOIVO, FORNECEDOR), onde FORNECEDOR consolida todas as capacidades profissionais.

### Principais Mudanças
- Unificação dos perfis profissionais em um único tipo FORNECEDOR
- Criação de modelo Fornecedor que herda de Usuario
- Sistema de verificação para fornecedores
- Dashboards específicos por perfil
- CRUD completo de itens (produtos, serviços, espaços)
- Criação automática de administrador

## 2. Modelos de Dados

### 2.1 Usuario (Base)
```python
@dataclass
class Usuario:
    id: int
    nome: str
    cpf: Optional[str]
    data_nascimento: Optional[str]
    email: str
    telefone: str
    senha: str
    perfil: TipoUsuario  # ADMIN, NOIVO, FORNECEDOR
    foto: Optional[str]
    token_redefinicao: Optional[str]
    data_token: Optional[str]
    data_cadastro: Optional[str]
```

### 2.2 Fornecedor (Herda de Usuario)
```python
@dataclass
class Fornecedor(Usuario):
    nome_empresa: Optional[str] = None
    cnpj: Optional[str] = None
    descricao: Optional[str] = None
    verificado: bool = False
    data_verificacao: Optional[str] = None
    prestador: bool = False  # Presta serviços
    vendedor: bool = False   # Vende produtos
    locador: bool = False    # Aluga espaços
```

### 2.3 Item (Produtos, Serviços e Espaços)
```python
class TipoItem(Enum):
    PRODUTO = "PRODUTO"
    SERVICO = "SERVICO"
    ESPACO = "ESPACO"

@dataclass
class Item:
    id: int
    id_fornecedor: int
    tipo: TipoItem
    nome: str
    descricao: str
    preco: float
    observacoes: Optional[str]
    ativo: bool = True
    data_cadastro: Optional[str] = None
```

### 2.4 FornecedorProduto (Tabela de Relacionamento)
```python
@dataclass
class FornecedorProduto:
    id_fornecedor: int
    id_produto: int
    observacoes: Optional[str]
    preco: float
```

### 2.5 PrestadorServico (Tabela de Relacionamento)
```python
@dataclass
class PrestadorServico:
    id_fornecedor: int  # Mudança de id_prestador
    id_servico: int
    observacoes: Optional[str]
    preco: float
```

## 3. Estrutura de Banco de Dados

### 3.1 Tabelas Principais
- **Usuario**: Dados base de todos os usuários
- **Fornecedor**: Dados específicos de fornecedores (FK para Usuario)
- **Item**: Produtos, serviços e espaços oferecidos
- **Casal**: Relacionamento entre noivos
- **Demanda**: Solicitações dos noivos
- **Orcamento**: Propostas dos fornecedores

### 3.2 Tabelas de Relacionamento
- **FornecedorProduto**: Produtos oferecidos por fornecedor
- **PrestadorServico**: Serviços oferecidos por fornecedor
- **ItemDemandaProduto**: Produtos solicitados em demanda
- **ItemDemandaServico**: Serviços solicitados em demanda
- **ItemOrcamentoProduto**: Produtos em orçamento
- **ItemOrcamentoServico**: Serviços em orçamento

## 4. Arquivos a Criar/Modificar

### 4.1 Modelos
- [x] `model/usuario_model.py` - Atualizado com 3 perfis e campos adicionais
- [x] `model/fornecedor_model.py` - Renomear de profissional_model.py
- [ ] `model/item_model.py` - Criar novo modelo unificado

### 4.2 SQL
- [x] `sql/usuario_sql.py` - Atualizado
- [x] `sql/fornecedor_sql.py` - Renomear de profissional_sql.py
- [ ] `sql/item_sql.py` - Criar queries para Item

### 4.3 Repositórios
- [x] `repo/usuario_repo.py` - Atualizado
- [x] `repo/fornecedor_repo.py` - Renomear de profissional_repo.py
- [ ] `repo/item_repo.py` - Criar CRUD completo

### 4.4 Rotas
- [ ] `routes/admin_routes.py` - Dashboard administrativo
- [ ] `routes/fornecedor_routes.py` - Dashboard do fornecedor
- [ ] `routes/noivo_routes.py` - Dashboard dos noivos
- [ ] `routes/public_routes.py` - Atualizar login e cadastro

### 4.5 Templates
- [ ] `templates/admin/dashboard.html`
- [ ] `templates/admin/usuarios.html`
- [ ] `templates/admin/verificacao.html`
- [ ] `templates/fornecedor/dashboard.html`
- [ ] `templates/fornecedor/itens.html`
- [ ] `templates/fornecedor/orcamentos.html`
- [ ] `templates/noivo/dashboard.html`
- [ ] `templates/noivo/demandas.html`

### 4.6 Testes
- [x] `tests/test_fornecedor_repo.py` - Renomear de test_profissional_repo.py
- [ ] `tests/test_item_repo.py` - Criar testes para Item
- [x] `tests/conftest.py` - Atualizar fixtures

### 4.7 Arquivos a Remover
- [ ] `routes/admin.py`
- [ ] `routes/administrador.py`
- [ ] `routes/cliente.py`
- [ ] `routes/fornecedor.py`
- [ ] `routes/prestador.py`
- [ ] `routes/locador.py`

## 5. Funcionalidades por Perfil

### 5.1 Administrador
- **Criação Automática**: Criar admin padrão se não existir
- **Gestão de Usuários**: Listar, visualizar, editar, excluir
- **Verificação de Fornecedores**: Aprovar/rejeitar fornecedores
- **Relatórios**: Estatísticas do sistema
- **Configurações**: Parâmetros gerais do sistema

### 5.2 Fornecedor
- **Cadastro Diferenciado**: Formulário específico com dados empresariais
- **Gestão de Itens**: CRUD completo (produtos, serviços, espaços)
- **Orçamentos**: Criar e gerenciar propostas
- **Perfil**: Editar dados pessoais e empresariais
- **Status de Verificação**: Visualizar status e requisitos

### 5.3 Noivo
- **Cadastro Simplificado**: Apenas dados pessoais básicos
- **Demandas**: Criar e gerenciar solicitações
- **Orçamentos**: Visualizar e aceitar propostas
- **Casal**: Gerenciar parceiro(a)
- **Histórico**: Acompanhar contratações

## 6. Fluxo de Autenticação

### 6.1 Login
```python
# Redirecionamento por perfil
if usuario.perfil == TipoUsuario.ADMIN:
    return RedirectResponse("/admin", status_code=303)
elif usuario.perfil == TipoUsuario.FORNECEDOR:
    return RedirectResponse("/fornecedor", status_code=303)
else:  # NOIVO
    return RedirectResponse("/noivo", status_code=303)
```

### 6.2 Middleware de Autenticação
- Verificar sessão em todas as rotas protegidas
- Validar perfil para acesso às áreas restritas
- Redirecionar para login se não autenticado

## 7. Sistema de Verificação

### 7.1 Processo
1. Fornecedor se cadastra com status `verificado = False`
2. Administrador revisa cadastro
3. Administrador aprova/rejeita
4. Fornecedor é notificado
5. Apenas verificados podem enviar orçamentos

### 7.2 Campos de Controle
- `verificado`: Boolean indicando status
- `data_verificacao`: Data da aprovação
- `observacoes_verificacao`: Comentários do admin

## 8. Implementação em Fases

### Fase 1: Refatoração Base ✅
- [x] Atualizar modelo Usuario
- [x] Criar modelo Fornecedor
- [x] Atualizar repositories
- [x] Ajustar testes

### Fase 2: Renomeação Profissional → Fornecedor
- [ ] Renomear todos os arquivos profissional_* para fornecedor_*
- [ ] Atualizar imports e referências
- [ ] Ajustar nomes de classes e variáveis
- [ ] Atualizar testes

### Fase 3: Sistema de Autenticação
- [ ] Criar admin automático
- [ ] Implementar redirecionamento por perfil
- [ ] Criar middleware de autenticação
- [ ] Proteger rotas por perfil

### Fase 4: Dashboards
- [ ] Dashboard administrativo
- [ ] Dashboard do fornecedor
- [ ] Dashboard dos noivos
- [ ] Templates base para cada área

### Fase 5: Gestão de Itens
- [ ] Criar modelo Item
- [ ] Implementar CRUD de itens
- [ ] Interface de gestão para fornecedor
- [ ] Visualização para noivos

### Fase 6: Sistema de Verificação
- [ ] Adicionar campos de verificação
- [ ] Interface de verificação para admin
- [ ] Notificações para fornecedor
- [ ] Restrições para não verificados

### Fase 7: Limpeza
- [ ] Remover rotas obsoletas
- [ ] Remover templates não utilizados
- [ ] Atualizar documentação
- [ ] Revisar e otimizar código

## 9. Considerações Técnicas

### 9.1 Migrações de Banco
- Preservar dados existentes
- Mapear fornecedores/prestadores/locadores antigos para novo modelo
- Criar scripts de migração SQL

### 9.2 Compatibilidade
- Manter compatibilidade com Casal existente
- Preservar relacionamentos existentes
- Atualizar foreign keys progressivamente

### 9.3 Segurança
- Validação de perfil em todas as rotas
- Hashing de senhas com bcrypt
- Tokens seguros para redefinição
- Proteção contra CSRF

### 9.4 Performance
- Índices adequados no banco
- Paginação em listagens
- Cache de consultas frequentes
- Otimização de queries JOIN

## 10. Testes

### 10.1 Unitários
- Modelos: Validação de campos e herança
- Repositórios: CRUD operations
- Utilitários: Hashing, validação

### 10.2 Integração
- Fluxo de cadastro completo
- Login e redirecionamento
- Verificação de fornecedor
- Criação de demandas e orçamentos

### 10.3 End-to-End
- Jornada do noivo
- Jornada do fornecedor
- Jornada do administrador

## 11. Cronograma Estimado

| Fase | Duração | Prioridade |
|------|---------|------------|
| Renomeação | 2 horas | Alta |
| Autenticação | 4 horas | Alta |
| Dashboards | 8 horas | Alta |
| Gestão de Itens | 6 horas | Média |
| Verificação | 4 horas | Média |
| Limpeza | 2 horas | Baixa |
| **Total** | **26 horas** | - |

## 12. Riscos e Mitigações

### Riscos
1. Perda de dados durante migração
2. Quebra de funcionalidades existentes
3. Problemas de compatibilidade

### Mitigações
1. Backup completo antes da migração
2. Testes extensivos em ambiente de desenvolvimento
3. Migração gradual com fallbacks

## 13. Checklist de Validação

- [ ] Todos os testes passando
- [ ] Login funcionando para os 3 perfis
- [ ] Redirecionamento correto por perfil
- [ ] Admin criado automaticamente
- [ ] Fornecedores podem gerenciar itens
- [ ] Sistema de verificação operacional
- [ ] Noivos podem criar demandas
- [ ] Orçamentos funcionando
- [ ] Rotas antigas removidas
- [ ] Documentação atualizada

## 14. Próximos Passos

1. **Imediato**: Renomear Profissional para Fornecedor em todo o sistema
2. **Seguinte**: Implementar criação automática de admin
3. **Depois**: Criar dashboards específicos por perfil
4. **Final**: Implementar sistema de verificação e gestão de itens

---

**Documento criado em**: 2025-09-18
**Última atualização**: 2025-09-18
**Versão**: 1.0