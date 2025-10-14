#!/usr/bin/env python3
"""
Script para exportar dados das tabelas demanda e item_demanda para JSON
"""
import sqlite3
import json
from pathlib import Path

# Caminhos
DB_PATH = Path(__file__).parent.parent / "dados.db"
SEEDS_PATH = Path(__file__).parent.parent / "data" / "seeds"

def export_table_to_json(db_path: Path, table_name: str, output_file: Path):
    """
    Exporta uma tabela SQLite para arquivo JSON

    Args:
        db_path: Caminho para o banco de dados SQLite
        table_name: Nome da tabela a ser exportada
        output_file: Caminho do arquivo JSON de saída
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    cursor = conn.cursor()

    # Buscar todos os dados da tabela
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Converter para lista de dicionários
    data = [dict(row) for row in rows]

    # Salvar como JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    conn.close()

    print(f"✅ Exportados {len(data)} registros de '{table_name}' para {output_file.name}")
    return len(data)

def main():
    """Executa a exportação das tabelas demanda e item_demanda"""
    print(f"📊 Exportando dados de {DB_PATH}")
    print(f"📁 Destino: {SEEDS_PATH}\n")

    # Verificar se o banco existe
    if not DB_PATH.exists():
        print(f"❌ Erro: Banco de dados não encontrado em {DB_PATH}")
        return

    # Criar pasta de seeds se não existir
    SEEDS_PATH.mkdir(parents=True, exist_ok=True)

    # Exportar tabelas
    total_demandas = export_table_to_json(
        DB_PATH,
        "demanda",
        SEEDS_PATH / "demanda.json"
    )

    total_itens = export_table_to_json(
        DB_PATH,
        "item_demanda",
        SEEDS_PATH / "item_demanda.json"
    )

    print(f"\n🎉 Exportação concluída!")
    print(f"   - {total_demandas} demandas")
    print(f"   - {total_itens} itens de demanda")

if __name__ == "__main__":
    main()
