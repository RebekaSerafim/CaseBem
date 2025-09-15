# criar_admin.py
from util.security import criar_hash_senha
from repo import usuario_repo
from model.usuario_model import Usuario

def criar_admin_padrao():
    # Verificar se já existe admin
    admins = usuario_repo.obter_todos_por_perfil("admin")
    if not admins:
        senha_hash = criar_hash_senha("admin123")
        admin = Usuario(
            id=0,
            nome="Administrador",
            email="admin@admin.com",
            senha=senha_hash,
            perfil="admin"
        )
        usuario_repo.inserir(admin)
        print("Admin criado: admin@admin.com / admin123")

if __name__ == "__main__":
    criar_admin_padrao()