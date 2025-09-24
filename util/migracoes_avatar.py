"""
Script de migração para remover a coluna 'foto' da tabela usuario
e criar o diretório de avatares.
"""

from util.database import obter_conexao
from util.avatar_util import criar_diretorio_usuarios
import os

def migrar_sistema_avatar():
    """
    Executa a migração para o novo sistema de avatar baseado em ID.
    Remove a coluna 'foto' da tabela usuario se existir.
    """
    print("Iniciando migração do sistema de avatar...")

    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Verificar se a coluna 'foto' existe
            cursor.execute("PRAGMA table_info(usuario)")
            colunas = cursor.fetchall()
            tem_coluna_foto = any(col[1] == 'foto' for col in colunas)

            if tem_coluna_foto:
                print("Coluna 'foto' encontrada. Removendo...")

                # Criar nova tabela sem a coluna foto
                cursor.execute("""
                    CREATE TABLE usuario_temp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT,
                        data_nascimento TEXT,
                        email TEXT NOT NULL UNIQUE,
                        telefone TEXT,
                        senha TEXT NOT NULL,
                        perfil TEXT NOT NULL DEFAULT 'NOIVO',
                        token_redefinicao TEXT,
                        data_token TIMESTAMP,
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ativo BOOLEAN NOT NULL DEFAULT 1
                    )
                """)

                # Copiar dados (excluindo a coluna foto)
                cursor.execute("""
                    INSERT INTO usuario_temp (
                        id, nome, cpf, data_nascimento, email, telefone, senha, perfil,
                        token_redefinicao, data_token, data_cadastro, ativo
                    )
                    SELECT
                        id, nome, cpf, data_nascimento, email, telefone, senha, perfil,
                        token_redefinicao, data_token, data_cadastro,
                        COALESCE(ativo, 1)
                    FROM usuario
                """)

                # Remover tabela original
                cursor.execute("DROP TABLE usuario")

                # Renomear tabela temporária
                cursor.execute("ALTER TABLE usuario_temp RENAME TO usuario")

                print("Coluna 'foto' removida com sucesso!")
            else:
                print("Coluna 'foto' não encontrada. Migração não necessária.")

        # Criar diretório de avatares
        if criar_diretorio_usuarios():
            print("Diretório de avatares criado/verificado com sucesso!")
        else:
            print("Erro ao criar diretório de avatares!")

        print("Migração do sistema de avatar concluída!")
        return True

    except Exception as e:
        print(f"Erro durante a migração: {e}")
        return False

if __name__ == "__main__":
    migrar_sistema_avatar()