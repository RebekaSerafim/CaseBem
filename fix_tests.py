#!/usr/bin/env python3
"""
Script para corrigir testes que esperam None mas agora recebem exceções do BaseRepo
"""
import re
import os

def fix_test_file(filepath):
    """Corrige um arquivo de teste"""
    print(f"Processando {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = 0

    # Padrão 1: Testes que verificam se retorno é None quando ID inexistente
    # assert.*is None.*ID inexistente
    pattern1 = r'(\s+)(.*?)\s*=\s*([\w_]+\.obter_\w+_por_id\(\d+\))\s*\n(\s+)# Assert\s*\n(\s+)assert\s+\2\s+is\s+None'

    def replace1(match):
        nonlocal changes
        changes += 1
        indent = match.group(1)
        var_name = match.group(2)
        call = match.group(3)
        return (f'{indent}# Act & Assert\n'
                f'{indent}import pytest\n'
                f'{indent}from util.exceptions import RecursoNaoEncontradoError\n'
                f'{indent}with pytest.raises(RecursoNaoEncontradoError):\n'
                f'{indent}    {call}')

    content = re.sub(pattern1, replace1, content, flags=re.MULTILINE)

    # Padrão 2: Testes de exclusão que tentam obter depois
    # excluir + assert ... is None
    pattern2 = r'(\s+)(\w+_excluido)\s*=\s*([\w_]+\.obter_\w+_por_id\([^)]+\))\s*\n(\s+)assert\s+\2\s+is\s+None'

    def replace2(match):
        nonlocal changes
        changes += 1
        indent = match.group(1)
        var_name = match.group(2)
        call = match.group(3)
        return (f'{indent}import pytest\n'
                f'{indent}from util.exceptions import RecursoNaoEncontradoError\n'
                f'{indent}with pytest.raises(RecursoNaoEncontradoError):\n'
                f'{indent}    {call}')

    content = re.sub(pattern2, replace2, content, flags=re.MULTILINE)

    # Se mudou, salva
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {changes} alterações feitas")
        return True
    else:
        print(f"  - Nenhuma alteração necessária")
        return False

def main():
    test_files = [
        'tests/test_demanda_repo.py',
        'tests/test_fornecedor_repo.py',
        'tests/test_item_repo.py',
        'tests/test_orcamento_repo.py',
        'tests/test_usuario_repo.py',
    ]

    total_fixed = 0
    for filepath in test_files:
        if os.path.exists(filepath):
            if fix_test_file(filepath):
                total_fixed += 1
        else:
            print(f"Arquivo não encontrado: {filepath}")

    print(f"\n✓ Total de arquivos corrigidos: {total_fixed}")

if __name__ == '__main__':
    main()