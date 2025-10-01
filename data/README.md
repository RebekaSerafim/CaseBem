# Data Directory

Este diretório contém dados e fixtures utilizados pelo sistema CaseBem.

## 📁 Estrutura

### seeds/
Dados iniciais para popular o banco de dados em ambiente de desenvolvimento.

**Arquivos**:
- `casais.json` - Casais de exemplo
- `categorias.json` - Categorias de produtos e serviços
- `fornecedores.json` - Fornecedores de exemplo
- `itens.json` - Itens/produtos de exemplo
- `itens_backup.json` - Backup dos itens (versão anterior)

**Uso**: Estes dados são carregados automaticamente por `util/startup.py` quando o banco de dados é criado pela primeira vez.

## 🔄 Uso

Os dados em `seeds/` são carregados na primeira execução da aplicação através do módulo `util/startup.py`:

```python
from util.startup import inicializar_sistema
inicializar_sistema()
```

## ⚠️ Importante

- **Não commitar dados sensíveis**: Este diretório deve conter apenas dados de exemplo
- **Formato JSON**: Todos os arquivos devem estar em formato JSON válido
- **Versionamento**: Arquivos de seed são versionados no Git para facilitar setup inicial

## 📝 Adicionando Novos Seeds

Para adicionar novos dados iniciais:

1. Crie um arquivo JSON em `seeds/`
2. Siga o formato dos arquivos existentes
3. Atualize `util/startup.py` para carregar os novos dados
4. Commit no Git

---

**Última atualização**: 2025-10-01
