# Como Resolver Problemas de Import no VS Code / Pylance

## ✅ Configurações Aplicadas

1. **util/__init__.py** - Criado para tornar `util` um pacote Python válido
2. **routes/__init__.py** - Criado para tornar `routes` um pacote Python válido
3. **pyrightconfig.json** - Configuração do Pylance/Pyright
4. **.vscode/settings.json** - Configurações do VS Code atualizadas

## 🔧 Passos para Resolver o Erro no VS Code

### Opção 1: Recarregar Janela (Mais Rápido)
1. Pressione `Cmd+Shift+P` (macOS) ou `Ctrl+Shift+P` (Windows/Linux)
2. Digite: `Developer: Reload Window`
3. Pressione Enter

### Opção 2: Reiniciar Python Language Server
1. Pressione `Cmd+Shift+P` (macOS) ou `Ctrl+Shift+P` (Windows/Linux)
2. Digite: `Python: Restart Language Server`
3. Pressione Enter

### Opção 3: Selecionar Interpretador Python Correto
1. Pressione `Cmd+Shift+P` (macOS) ou `Ctrl+Shift+P` (Windows/Linux)
2. Digite: `Python: Select Interpreter`
3. Selecione: `/Users/maroquio/.pyenv/versions/3.11.11/bin/python`

### Opção 4: Limpar Cache (Se nada funcionar)
1. Feche o VS Code completamente
2. No terminal, execute:
   ```bash
   cd /Volumes/Externo/Ifes/CaseBem
   rm -rf **/__pycache__
   rm -rf .pytest_cache
   ```
3. Reabra o VS Code

## ✓ Verificação

Após executar um dos passos acima, abra o arquivo `util/logger.py` e verifique:
- A linha 9 (`from .exceptions import CaseBemError, TipoErro`) NÃO deve mostrar erro
- O código deve ter autocompletar funcionando

## 💡 Explicação Técnica

O erro ocorria porque:
1. Faltava `__init__.py` no pacote `util/`
2. O VS Code estava configurado para usar um venv inexistente
3. O Pylance não sabia que o diretório raiz do projeto estava no PYTHONPATH

Todas essas questões foram resolvidas nas configurações aplicadas.