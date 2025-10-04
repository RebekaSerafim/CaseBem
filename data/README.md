# Diretório de Dados

Este diretório contém os dados de seed para inicialização do sistema CaseBem.

## Estrutura

```
data/
├── seeds/          # Arquivos JSON para popular o banco de dados
│   ├── usuarios.json       # Usuários (admin + noivos)
│   ├── fornecedores.json   # Fornecedores e seus dados de usuário
│   ├── casais.json         # Casais cadastrados
│   ├── categorias.json     # Categorias de serviços/produtos
│   ├── itens.json          # Itens de fornecedores
│   └── fornecedores_base.json  # Template antigo (mantido para referência)
└── README.md       # Este arquivo
```

## Seeds Automáticos

Os arquivos JSON em `seeds/` são automaticamente importados quando o sistema é inicializado com um banco de dados vazio. A importação é gerenciada pelo `util/startup.py`.

### Arquivos de Seed

#### usuarios.json
Contém todos os usuários do sistema:
- 1 administrador (ID: 1)
- 20 noivos/noivas (IDs: 12-31, formando 10 casais)

**Campos:** id, nome, cpf, data_nascimento, email, telefone, senha (hash), perfil, data_cadastro

#### fornecedores.json
Contém os fornecedores e seus dados de usuário:
- 10 fornecedores (IDs: 2-11)

**Campos:** id, nome, cpf, data_nascimento, email, telefone, senha (hash), perfil, ativo, data_cadastro, nome_empresa, cnpj, descricao, verificado

**Importante:** Os fornecedores são inseridos tanto na tabela `usuario` quanto na tabela `fornecedor` (relacionamento 1:1 via foreign key).

#### casais.json
Contém os casais cadastrados:
- 10 casais (IDs: 1-10)

**Campos:** id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento_estimado, numero_convidados, data_cadastro

#### categorias.json
Contém as categorias de serviços/produtos:
- 20 categorias padrão

**Campos:** id, nome, tipo (SERVICO/PRODUTO/LOCAL), descricao

#### itens.json
Contém os itens/serviços oferecidos pelos fornecedores.

**Campos:** id, nome, descricao, preco, id_categoria

## Credenciais Padrão

### Administrador
- Email: `admin@casebem.com`
- Senha: `1234aA@#`

### Fornecedores e Noivos
Todos os usuários de teste usam a mesma senha padrão: `1234aA@#`

**⚠️ IMPORTANTE:** Altere todas as senhas padrão em ambiente de produção!

## Processo de Importação

O processo de seed é executado automaticamente por `util/startup.py` na seguinte ordem:

1. **Usuários** (`criar_usuarios_seed()`) - Importa admin e noivos
2. **Categorias** (`criar_categorias()`) - Importa categorias
3. **Fornecedores** (`criar_fornecedores_seed()`) - Importa fornecedores (usuario + fornecedor)
4. **Casais** (`criar_casais_seed()`) - Importa casais

Cada função verifica se os dados já existem antes de importar, evitando duplicações.

## Exportando Dados

Para exportar dados atuais do banco para os arquivos de seed:

```bash
# Usuários
sqlite3 dados.db "SELECT json_group_array(json_object(...)) FROM usuario" | python3 -m json.tool > data/seeds/usuarios.json

# Fornecedores (join usuario + fornecedor)
sqlite3 dados.db "SELECT json_group_array(...) FROM fornecedor f JOIN usuario u ON f.id = u.id" | python3 -m json.tool > data/seeds/fornecedores.json

# Casais
sqlite3 dados.db "SELECT json_group_array(...) FROM casal" | python3 -m json.tool > data/seeds/casais.json
```

## Observações

- Os IDs são preservados durante a importação para manter consistência com imagens e outros recursos
- As senhas são importadas já em formato hash (bcrypt)
- Foreign keys são respeitadas: usuários antes de fornecedores/casais
- A importação é idempotente: executar múltiplas vezes não cria dados duplicados
