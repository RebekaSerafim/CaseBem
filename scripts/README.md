# Scripts Utilitários

Este diretório contém scripts auxiliares para tarefas pontuais do projeto CaseBem.

## 📜 Scripts Disponíveis

### download_imagens.py
Script pontual para baixar imagens geradas via Runware AI.

**Propósito**: Usado uma única vez para popular banco de imagens inicial do projeto.

**URLs**: Contém URLs hardcoded do Runware AI para 11 itens específicos.

**Uso**:
```bash
python scripts/download_imagens.py
```

**Nota**: Este script foi executado apenas durante a configuração inicial.
As imagens já estão no diretório `static/img/itens/`. Executar novamente
sobrescreverá as imagens existentes.

## 📝 Adicionando Novos Scripts

Para adicionar novos scripts utilitários:

1. Crie o arquivo `.py` neste diretório
2. Adicione shebang no topo: `#!/usr/bin/env python3`
3. Documente o propósito e uso neste README
4. Se for um script CLI, adicione argparse para help

## 🔧 Convenções

- **Nome**: Use snake_case descritivo (ex: `migrar_dados.py`)
- **Documentação**: Adicione docstring no topo do arquivo
- **Dependências**: Liste dependências especiais no docstring
- **Uso único**: Scripts que rodam uma vez devem estar claramente marcados

---

**Última atualização**: 2025-10-01
